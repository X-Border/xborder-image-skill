#!/usr/bin/env python3
"""Preflight a normalized listing manifest against scoped, sourced marketplace rules.

The validator checks metadata and declared facts. It cannot decide whether an image
visually shows the true item, whether a claim is legally acceptable, or whether a seller
account's live category schema has changed; those are returned as manual checks.
"""

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "references" / "platforms" / "platform-rules.json"
RELEASE_REVIEW_FIELDS = (
    "product_identity",
    "claim_evidence_match",
    "sku_and_package_match",
    "visual_assets_and_text",
    "localization_and_policy",
    "files_and_upload_specs",
)
URL_BACKED_FACT_TYPES = {"manufacturer_page", "seller_page", "marketplace_listing"}


def load_json(path):
    with Path(path).open(encoding="utf-8") as stream:
        return json.load(stream)


def resolve_market(platform, market):
    platforms = RULES["platforms"]
    profile = platforms[platform]
    selected = profile.get("markets", {}).get(market)
    if selected is None:
        return profile, None
    if "inherit" in selected:
        parent = profile["markets"].get(selected["inherit"], {})
        combined = {**parent, **selected}
        combined.pop("inherit", None)
        combined["title"] = {**parent.get("title", {}), **selected.get("title", {})}
        combined["images"] = selected.get("images", parent.get("images", []))
        combined["manual_checks"] = parent.get("manual_checks", []) + selected.get("manual_checks", [])
        return profile, combined
    return profile, selected


def add(findings, level, code, message, source=None):
    finding = {"level": level, "code": code, "message": message}
    if source:
        finding["source"] = source
    findings.append(finding)


def source_for(profile, key):
    if not key:
        return None
    source = profile.get("sources", {}).get(key)
    if not source:
        return None
    return {"key": key, "url": source.get("url"), "scope": source.get("scope"), "accessed": source.get("accessed")}


def image_value(image, field, all_images):
    width = image.get("width")
    height = image.get("height")
    if field == "width":
        return width
    if field == "height":
        return height
    if field == "short_side":
        return min(width, height) if width and height else None
    if field == "long_side":
        return max(width, height) if width and height else None
    if field == "primary_short_side":
        primary = next((asset for asset in all_images if asset.get("role") == "primary"), None)
        pw, ph = (primary or {}).get("width"), (primary or {}).get("height")
        return min(pw, ph) if pw and ph else None
    if field == "bytes":
        return image.get("bytes")
    if field == "resolution_ppi":
        return image.get("resolution_ppi", image.get("ppi"))
    if field == "color_space":
        value = image.get("color_space")
        return str(value).lower() if value is not None else None
    if field == "format":
        fmt = image.get("format")
        if not fmt:
            path = image.get("path") or image.get("url") or ""
            fmt = Path(path.split("?", 1)[0]).suffix.lstrip(".")
        return str(fmt).lower()
    if field == "width_height_ratio":
        return width / height if width and height else None
    if field == "dimensions":
        return [width, height] if width and height else None
    if field == "one_of":
        return str(image.get("format") or Path((image.get("path") or image.get("url") or "").split("?", 1)[0]).suffix.lstrip(".")).lower()
    return None


def violates(actual, op, expected):
    if actual is None:
        return None
    if op == "min":
        return actual < expected
    if op == "max":
        return actual > expected
    if op == "one_of":
        return actual not in {str(item).lower() for item in expected}
    if op == "equals":
        return abs(actual - expected) > 0.01
    if op == "recommended_exact":
        return actual != expected
    return None


def text_objects(manifest):
    listing = manifest.get("listing", {})
    result = []
    for key in ("title", "description"):
        item = listing.get(key)
        if isinstance(item, dict):
            result.append((f"listing.{key}", item))
    for key in ("highlights", "disclosures"):
        for index, item in enumerate(listing.get(key, []), start=1):
            if isinstance(item, dict):
                result.append((f"listing.{key}[{index}]", item))
    for index, item in enumerate(manifest.get("claims", []), start=1):
        if isinstance(item, dict):
            result.append((f"claims[{index}]", item))
    for index, item in enumerate(listing.get("attributes", []), start=1):
        if isinstance(item, dict):
            result.append((f"listing.attributes[{index}]", item))
    return result


def validate_shared_image_baseline(findings, profile, market, manifest):
    """Apply a configurable project baseline without presenting it as policy."""
    baseline = profile.get("shared_image_baseline", {})
    defaults = baseline.get("export_defaults", {})
    if baseline.get("status") != "initial_project_default_unverified_per_market" or not defaults:
        return

    note = "initial Shopee shared project default; verify against the destination Seller Centre"
    images = manifest.get("media", [])
    listing_images = [item for item in images if item.get("role") in {"primary", "gallery"}]
    minimum = defaults.get("min_gallery_images")
    maximum = defaults.get("max_gallery_images")
    if minimum is not None and len(listing_images) < minimum:
        add(findings, "warning", "shared_image_count_default", f"Shopee {market}: {len(listing_images)} primary/gallery image(s); the shared project baseline plans at least {minimum}. This is a content workflow default, not a verified upload minimum.")
    if maximum is not None and len(listing_images) > maximum:
        add(findings, "warning", "shared_image_count_default", f"Shopee {market}: {len(listing_images)} primary/gallery image(s); the shared project baseline plans at most {maximum}. This is not a verified upload maximum.")

    min_dimensions = defaults.get("minimum_dimensions_px", {})
    min_side = min(min_dimensions.values()) if min_dimensions else None
    max_bytes = defaults.get("max_file_bytes")
    formats = defaults.get("formats")
    aspect_ratio = defaults.get("aspect_ratio")
    for asset in listing_images:
        label = asset.get("id", "Image")
        missing = []
        checks = []
        if min_side is not None:
            checks.append(("short_side", "min", min_side))
        if aspect_ratio == "1:1":
            checks.append(("width_height_ratio", "equals", 1.0))
        if formats:
            checks.append(("format", "one_of", formats))
        if max_bytes is not None:
            checks.append(("bytes", "max", max_bytes))

        for field, op, expected in checks:
            actual = image_value(asset, field, images)
            if actual is None:
                missing.append(field)
                continue
            if violates(actual, op, expected):
                add(findings, "warning", "shared_image_default", f"{label}: {field}={actual!r} is outside the Shopee {market} {note} ({op} {expected!r}).")
        if missing:
            add(findings, "warning", "shared_image_metadata_missing", f"{label}: missing {', '.join(missing)} metadata, so the Shopee {market} shared project baseline could not be fully checked.")


def validate(manifest):
    findings = []
    required = ("manifest_version", "platform", "market", "locale", "product", "category", "facts", "listing", "media")
    missing = [key for key in required if key not in manifest]
    if missing:
        add(findings, "error", "missing_manifest_fields", f"Required manifest field(s) missing: {', '.join(missing)}.")
    if not isinstance(manifest.get("product"), dict) or not manifest.get("product", {}).get("name"):
        add(findings, "error", "invalid_product", "product must be an object with a non-empty name.")
    if not isinstance(manifest.get("category"), dict) or not manifest.get("category", {}).get("name"):
        add(findings, "error", "invalid_category", "category must be an object with a name.")
    if not isinstance(manifest.get("listing"), dict):
        add(findings, "error", "invalid_listing", "listing must be an object.")
    if not isinstance(manifest.get("facts"), list):
        add(findings, "error", "invalid_facts", "facts must be an array.")
    if not isinstance(manifest.get("media"), list):
        add(findings, "error", "invalid_media", "media must be an array.")
    if any(item["level"] == "error" for item in findings):
        return findings

    platform = manifest.get("platform")
    market = manifest.get("market")
    if platform not in RULES["platforms"]:
        add(findings, "error", "unknown_platform", f"Unknown platform: {platform!r}.")
        return findings
    profile, market_rules = resolve_market(platform, market)
    snapshot = manifest.get("policy_snapshot", {})
    live_check_recorded = (
        snapshot.get("manual_check_status") == "checked"
        and bool(snapshot.get("seller_center_checked_at"))
    )
    if snapshot.get("rules_reviewed_on") != RULES.get("reviewed_on"):
        add(findings, "warning", "rule_snapshot_stale", f"Manifest rules_reviewed_on is {snapshot.get('rules_reviewed_on')!r}; current local rule snapshot is {RULES.get('reviewed_on')!r}. Recheck the selected market before release.")
    if platform == "shopee":
        validate_shared_image_baseline(findings, profile, market, manifest)
    if market_rules is None:
        add(findings, "warning", "market_not_profiled", f"No numeric policy profile for {profile['name']} market {market!r}; do not reuse another country's limits. Verify in the target Seller Center/API.")
    else:
        title_obj = manifest.get("listing", {}).get("title")
        title = title_obj.get("text", "") if isinstance(title_obj, dict) else (title_obj or "")
        title_policy = market_rules.get("title", {}) if title else {}
        for key, rule in title_policy.items():
            if not isinstance(rule, dict) or "value" not in rule:
                continue
            value = rule["value"]
            source = source_for(profile, rule.get("source"))
            status = rule.get("status", "recommendation")
            if key == "max_word_repetitions":
                ignored = {word.casefold() for word in rule.get("exclude", [])}
                words = [word.casefold() for word in re.findall(r"[^\W_]+", title, flags=re.UNICODE) if word.casefold() not in ignored]
                repeated = sorted({word for word in words if words.count(word) > value})
                if repeated:
                    add(findings, "error" if status == "enforced" else "warning", "title_repeated_words", f"Title repeats these non-exempt word(s) more than {value} times: {', '.join(repeated)}.", source)
                continue
            if key == "restricted_characters":
                found = [character for character in value if character in title]
                if found:
                    add(findings, "warning", "title_restricted_characters", f"Title contains restricted character(s) {', '.join(found)}. Verify whether each is permitted as part of the registered brand name. {rule.get('exception', '')}", source)
                continue
            is_min = key.endswith("min_chars")
            is_max = key.endswith("max_chars")
            if not (is_min or is_max):
                continue
            bad = len(title) < value if is_min else len(title) > value
            if bad:
                level = "error" if status == "enforced" else "warning"
                relation = "at least" if is_min else "at most"
                add(findings, level, "title_length", f"Title has {len(title)} characters; {profile['name']} {market} {key.replace('_', ' ')} is {relation} {value} ({status}).", source)

        if title and market_rules.get("title_excludes_brand"):
            brand = manifest.get("product", {}).get("brand")
            if brand and str(brand).casefold() in title.casefold():
                add(findings, "warning", "title_contains_brand", f"The {profile['name']} {market} title guide says to keep the brand name in its separate brand field, not the title.", source_for(profile, market_rules.get("title_policy_source")))

        search_policy = market_rules.get("search_terms", {})
        backend_terms = manifest.get("listing", {}).get("platform_fields", {}).get("backend_search_terms")
        if backend_terms is not None and "max_bytes" in search_policy:
            rule = search_policy["max_bytes"]
            byte_count = len(str(backend_terms).encode("utf-8"))
            if byte_count > rule["value"]:
                add(findings, "error" if rule.get("status") == "enforced" else "warning", "search_terms_bytes", f"Backend search terms use {byte_count} UTF-8 bytes; limit is {rule['value']} bytes.", source_for(profile, rule.get("source")))

        images = manifest.get("media", [])
        listing_images = [item for item in images if item.get("role") in {"primary", "gallery"}]
        primary = next((item for item in listing_images if item.get("role") == "primary"), None)
        allowed_primary_types = market_rules.get("primary_source_types")
        if primary and primary.get("status") != "planned" and allowed_primary_types and primary.get("source_type") not in allowed_primary_types:
            add(findings, "error", "primary_source_type", f"Primary asset source_type is {primary.get('source_type')!r}; {profile['name']} {market} allows {', '.join(allowed_primary_types)} for the primary slot according to this profile.")
        disallowed_listing_types = set(market_rules.get("disallowed_listing_source_types", []))
        manual_review_listing_types = set(market_rules.get("manual_review_listing_source_types", []))
        for asset in listing_images:
            if asset.get("status") == "planned":
                continue
            if asset.get("source_type") in disallowed_listing_types:
                add(findings, "error", "listing_image_source_type", f"{asset.get('id', 'Image')} is declared as {asset.get('source_type')}; this source type is disallowed for {profile['name']} {market} listing images by the scoped profile.", source_for(profile, market_rules.get("media_policy_source")))
            elif asset.get("source_type") in manual_review_listing_types:
                add(findings, "manual", "listing_image_source_type_review", f"Verify that {asset.get('id', 'Image')} is a photograph of the actual product; {asset.get('source_type')} imagery is not cleared as a Noon product photo by metadata alone.", source_for(profile, market_rules.get("media_policy_source")))
        if market_rules.get("disallow_added_text"):
            for asset in listing_images:
                if asset.get("status") == "planned":
                    continue
                if asset.get("contains_added_text") is True:
                    add(findings, "error", "added_text_disallowed", f"{asset.get('id', 'Image')} is declared as containing added text, which is disallowed for {profile['name']} {market} listing images.", source_for(profile, market_rules.get("media_policy_source")))
                elif asset.get("contains_added_text") is not False and manifest.get("release_review", {}).get("visual_assets_and_text") != "passed":
                    add(findings, "manual", "added_text_unverified", f"Verify whether {asset.get('id', 'Image')} contains added text before release.", source_for(profile, market_rules.get("media_policy_source")))
        for rule in market_rules.get("images", []):
            source = source_for(profile, rule.get("source"))
            field, op, expected = rule.get("field"), rule.get("op"), rule.get("value")
            if field == "count":
                bad = len(listing_images) > expected if op == "max" else (len(listing_images) < expected if op == "min" else False)
                if bad:
                    level = "error" if rule.get("status") == "enforced" else "warning"
                    add(findings, level, "image_count", f"Listing has {len(listing_images)} primary/gallery images; limit is {op} {expected} ({rule.get('status')}).", source)
                continue
            for asset in listing_images:
                if asset.get("status") == "planned":
                    continue
                if field == "primary_short_side" and asset.get("role") != "primary":
                    continue
                actual = image_value(asset, field, images)
                if actual is None:
                    if asset.get("role") in {"primary", "gallery"}:
                        add(findings, "warning", "image_metadata_missing", f"{asset.get('id', 'Image')} is missing metadata for {field}; this rule could not be checked.", source)
                    continue
                bad = violates(actual, op, expected)
                if bad:
                    level = "error" if rule.get("status") == "enforced" else "warning"
                    label = asset.get("id", "Image")
                    add(findings, level, "image_rule", f"{label}: {field}={actual!r} violates {op} {expected!r} ({rule.get('status')}).", source)

        if not live_check_recorded:
            for note in market_rules.get("manual_checks", []):
                add(findings, "manual", "seller_center_check", note)

    facts = manifest.get("facts", [])
    fact_id_values = [fact.get("id") for fact in facts if isinstance(fact, dict) and isinstance(fact.get("id"), str) and fact.get("id")]
    fact_ids = set(fact_id_values)
    if any(not isinstance(fact, dict) for fact in facts):
        add(findings, "error", "invalid_fact", "Each facts entry must be an object.")
    if len(fact_id_values) != len(facts) or len(fact_ids) != len(fact_id_values):
        add(findings, "error", "duplicate_fact_id", "Fact IDs must be unique and non-empty.")
    referenced_fact_ids = set()
    for location, item in text_objects(manifest):
        refs = item.get("fact_ids", [])
        referenced_fact_ids.update(refs)
        unknown = sorted(set(refs) - fact_ids)
        if unknown:
            add(findings, "error", "unknown_fact_reference", f"{location} references missing fact id(s): {', '.join(unknown)}.")
        if location.startswith("claims[") and not refs:
            add(findings, "warning", "claim_without_evidence", f"{location} has no fact_ids; substantiate or remove this claim before publishing.")
        elif location.startswith("listing.") and item.get("text") and not refs:
            add(findings, "warning", "copy_without_evidence", f"{location} has no fact_ids; map its factual wording to the evidence ledger before release.")

    for asset in manifest.get("media", []):
        refs = asset.get("fact_ids", [])
        referenced_fact_ids.update(refs)
        unknown = sorted(set(refs) - fact_ids)
        if unknown:
            add(findings, "error", "unknown_media_fact_reference", f"Media {asset.get('id', '<unknown>')!r} references missing fact id(s): {', '.join(unknown)}.")

    for fact in facts:
        if not isinstance(fact, dict):
            continue
        if fact.get("source_type") in URL_BACKED_FACT_TYPES and not fact.get("source_url"):
            add(findings, "error", "fact_source_url_missing", f"Fact {fact.get('id')!r} is sourced from a web page but has no source_url.")
        if fact.get("id") in referenced_fact_ids and fact.get("source_type") in {"derived", "unverified"}:
            add(findings, "warning", "fact_needs_review", f"Fact {fact.get('id')!r} is {fact.get('source_type')}; do not present it as a verified product claim.")
        if (
            fact.get("id") in referenced_fact_ids
            and fact.get("source_type") in {"seller_page", "marketplace_listing"}
            and manifest.get("release_review", {}).get("claim_evidence_match") != "passed"
        ):
            add(findings, "manual", "seller_page_claim_review", f"Verify seller-page claim {fact.get('id')!r} against the actual SKU or manufacturer evidence before release.")
        if (
            fact.get("id") in referenced_fact_ids
            and fact.get("source_type") == "product_image"
            and manifest.get("release_review", {}).get("claim_evidence_match") != "passed"
        ):
            add(findings, "manual", "visual_fact_review", f"Review image-derived fact {fact.get('id')!r} against the product label or source photo before using exact technical/regulated claims.")

    listing_images = [item for item in manifest.get("media", []) if item.get("role") in {"primary", "gallery"}]
    provenance = manifest.get("provenance", {})
    if listing_images:
        if provenance.get("example_only") is True:
            add(findings, "error", "example_manifest_not_releasable", "This manifest is marked as an example/self-test and cannot be a production upload candidate.")
        anchor_type = provenance.get("identity_anchor_source_type")
        if anchor_type in {"generated", "composite", "illustration"}:
            add(findings, "error", "synthetic_identity_anchor", "The identity-anchor image is synthetic or illustrative; provide a real product source image before a production release.")
        elif anchor_type != "photograph":
            add(findings, "manual", "identity_anchor_unverified", "Record and verify that the identity-anchor source is a photograph of the actual sellable product.")
    if len(listing_images) > 1 and not manifest.get("selling_point_sheet"):
        add(findings, "warning", "selling_point_sheet_missing", "A multi-image set has no saved selling-point sheet / buyer-concern map.")
    for asset in listing_images:
        if asset.get("status") == "planned":
            continue
        label = asset.get("id", "Image")
        missing_metadata = [key for key in ("width", "height", "bytes", "format") if not asset.get(key)]
        if not (asset.get("path") or asset.get("url")):
            missing_metadata.append("path_or_url")
        if missing_metadata:
            add(findings, "warning", "asset_metadata_incomplete", f"{label}: missing {', '.join(missing_metadata)}; the output file and upload constraints cannot be verified from this manifest.")
        for key in ("buyer_question", "visual_proof", "why_gallery_slot"):
            if not asset.get(key):
                add(findings, "warning", "shot_plan_incomplete", f"{label}: shot plan is missing {key}; state the distinct buyer value and visible proof before generation.")

    category = manifest.get("category", {})
    if not category.get("id") or not category.get("required_attributes_resolved", False):
        add(findings, "manual", "category_schema_unresolved", "A category ID and current required-attribute schema have not both been recorded; resolve them for the selected site before publishing.")
    if snapshot.get("manual_check_status") != "checked" or not snapshot.get("seller_center_checked_at"):
        add(findings, "manual", "live_policy_not_checked", "The manifest does not record a completed, dated Seller Center/API policy check.")
    if not any(item.get("role") == "primary" for item in manifest.get("media", [])):
        add(findings, "warning", "primary_image_missing", "No primary image is recorded in this manifest.")
    if not manifest.get("listing", {}).get("title") and manifest.get("delivery_mode") != "image_set_only":
        add(findings, "warning", "title_missing", "No listing title is recorded.")

    release_review = manifest.get("release_review", {})
    failed_gates = [field for field in RELEASE_REVIEW_FIELDS if release_review.get(field) == "failed"]
    for field in failed_gates:
        add(findings, "error", "release_gate_failed", f"Human release gate {field!r} is marked failed; correct the issue and review again.")
    for field in RELEASE_REVIEW_FIELDS:
        if release_review.get(field) != "passed":
            add(findings, "manual", "release_gate_incomplete", f"Human release gate {field!r} is not marked passed after reviewing the final files.")
    if not release_review.get("reviewed_by") or not release_review.get("reviewed_at"):
        add(findings, "manual", "release_reviewer_missing", "Record the operator role and review timestamp for the completed release checklist.")

    return findings


def production_readiness(manifest, findings):
    """Return the strongest honest asset-package status; never claim platform approval."""
    counts = {level: sum(item["level"] == level for item in findings) for level in ("error", "warning", "manual")}
    listing_images = [item for item in manifest.get("media", []) if item.get("role") in {"primary", "gallery"}]
    planned_only = bool(listing_images) and all(item.get("status") == "planned" for item in listing_images)
    if planned_only:
        status = "concept_preview"
    elif counts["error"]:
        status = "blocked"
    elif not any(item.get("role") in {"primary", "gallery"} for item in manifest.get("media", [])):
        status = "concept_preview"
    elif counts["warning"] or counts["manual"]:
        status = "human_review_required"
    else:
        status = "candidate_for_manual_upload"
    return {
        "status": status,
        "counts": counts,
        "note": "Candidate status means the manifest declares all required checks complete and local scoped checks found no open findings. It is not marketplace approval and cannot guarantee acceptance.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="Path to a listing manifest JSON file")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    parser.add_argument("--require-candidate-for-manual-upload", action="store_true", help="Return exit code 3 unless production_readiness is candidate_for_manual_upload")
    args = parser.parse_args()
    try:
        manifest = load_json(args.manifest)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Cannot read manifest: {exc}", file=sys.stderr)
        return 2
    if not isinstance(manifest, dict):
        print("Manifest root must be a JSON object.", file=sys.stderr)
        return 2
    findings = validate(manifest)
    counts = {level: sum(item["level"] == level for item in findings) for level in ("error", "warning", "manual")}
    snapshot = manifest.get("policy_snapshot", {})
    live_check_recorded = snapshot.get("manual_check_status") == "checked" and bool(snapshot.get("seller_center_checked_at")) and bool(manifest.get("category", {}).get("required_attributes_resolved"))
    readiness = production_readiness(manifest, findings)
    result = {"platform": manifest.get("platform"), "market": manifest.get("market"), "rules_reviewed_on": RULES.get("reviewed_on"), "counts": counts, "automated_checks_pass": counts["error"] == 0, "live_check_recorded": live_check_recorded, "preflight_status": "automated_errors_found" if counts["error"] else "manual_review_required", "production_readiness": readiness, "findings": findings}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Preflight · {manifest.get('platform')} / {manifest.get('market')} · rules reviewed {RULES.get('reviewed_on')}")
        print(f"Errors: {counts['error']} · Warnings: {counts['warning']} · Manual checks: {counts['manual']}")
        print(f"Production readiness: {readiness['status']}")
        for item in findings:
            source = f" — {item['source']['url']}" if item.get("source", {}).get("url") else ""
            print(f"[{item['level'].upper()}] {item['code']}: {item['message']}{source}")
        print("Status: " + ("AUTOMATED CHECKS PASS · LIVE POLICY REVIEW STILL REQUIRED" if counts["error"] == 0 else "AUTOMATED ERRORS FOUND · NOT VERIFIED FOR PUBLISHING"))
    if counts["error"]:
        return 1
    if args.require_candidate_for_manual_upload and readiness["status"] != "candidate_for_manual_upload":
        return 3
    return 0


RULES = load_json(RULES_PATH)


if __name__ == "__main__":
    raise SystemExit(main())
