# Platform profiles — multi-marketplace listing image skill

This skill creates platform-adapted listing content, image plans/prompts, preflight reports,
and a structured export. Supported profiles: Amazon, Temu, Noon, Walmart Marketplace,
eBay, Etsy, TikTok Shop, Ozon, Shopee, and Mercado Libre. The depth of publicly verifiable
rules differs by market. A platform name alone is not enough: country/site and category
are required inputs before claiming an output is ready to publish.

## What is SHARED (write once, all platforms reuse)

- **Execution modes** — full kit / image-set-only / copy-only / single-slot / A+ /
  preview (SKILL.md STEP 0).
- **Product & selling-point reading** and current-state protection (STEP 0).
- **Image backend** — how a brief becomes a rendered image via the current X-Border MCP
  tools (`references/image-backend.md`).
- **Image-craft principles** — thumbnail legibility, one message per image, real
  product match, no AI-poster artifacts (SKILL.md STEP 3 + `amazon-image-strategy.md`).
- **Structured listing manifest** (`listing-manifest.schema.json`): normalized content,
  market/category, product evidence, images, and provenance.
- **Excel export** (`scripts/generate_excel.py`): workbook tabs for listing fields, media,
  product facts, and platform checks, all driven by the same manifest.
- **Rule preflight** (`scripts/validate_listing.py`): deterministic checks only for
  machine-verifiable rules with a source and explicit market scope, plus clearly labeled
  project defaults that produce warnings rather than policy violations.

## What is PER-PLATFORM (one file in this folder)

1. **Copy rules** — title format/length, bullet/highlight count & format, description
   length, keyword/search-term budget, language(s).
2. **Image slot taxonomy** — the slot ids and meaning for that marketplace.
3. **Compliance** — main-image rules, banned content, cultural/localisation notes.

## Files

| file | platform / scope |
|---|---|
| `amazon.md` | Amazon; detailed image strategy remains in `SKILL.md` |
| `temu.md` | Temu; public-policy gaps are marked for Seller Center verification |
| `noon.md` | Noon; UAE/Saudi/Egypt localization and official image guidance |
| `walmart.md` | Walmart; Canada numeric guide, US schema-driven/manual image check |
| `ebay.md` | eBay US snapshot; item specifics and condition-aware imagery |
| `etsy.md` | Etsy; exact-item photography, mockup exceptions and AI disclosure distinction |
| `tiktok-shop.md` | TikTok Shop US snapshot; country/category rules remain dynamic |
| `ozon.md` | Ozon; Seller API/category schema required at runtime |
| `shopee.md` | Shopee; shared initial image baseline with per-market localization, Singapore recommendations separately scoped |
| `mercado-libre.md` | Mercado Libre; CBT/site/category-specific flow |
| `platform-rules.json` | Machine-readable sourced constraints, scope and verification status |
| `listing-manifest.schema.json` | Canonical input/output shape |

## Resolution at runtime (SKILL.md STEP 0)

Detect the platform and **require the destination market** when specs/localization differ.
If no platform is named, use Amazon only as a drafting default and label the market
assumption. For unsupported markets, preserve the structured content but mark platform
limits `seller_center_check_required`; do not borrow another country's numeric limits.

## Rules and evidence model

- `platform-rules.json` distinguishes `enforced`, `official_guidance` and
  `recommendation` for sourced numeric rules. Shopee's `shared_image_baseline` is an
  explicitly unverified project default and can only produce warnings. Dynamic schemas
  and Seller Center checks are listed separately under each scoped market's `manual_checks`.
- Each numeric rule carries a source key, and each source records URL, scope, and review
  date. Never use a value outside its country/site or listing-flow scope.
- Category attributes, max photo count, restricted-product approvals and visual/content
  truthfulness can require a live Seller Center/API check. The validator reports those
  checks; it cannot prove them from a manifest.
- Refresh the source and review date before changing a published profile. A source with
  no valid market scope is not a hard rule.

## Adding a new platform (checklist)

1. Research official country/site-specific listing and media sources.
2. Add a focused profile and sourced machine-readable rules with status and scope.
3. Map the platform's fields to the canonical manifest; keep category-specific fields
   dynamic where their source schema is dynamic.
4. Define recommended image story beats separately from actual platform constraints.
5. Add the platform and market to the schema/validator, then update the skill router.
