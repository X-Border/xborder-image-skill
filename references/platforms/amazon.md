# Platform profile — Amazon (reference implementation)

Amazon is the fully-detailed platform. Its copy rules and per-slot image briefs live in
`SKILL.md` (STEP 1 copy, STEP 3 AS slots, STEP 3B AD modules) and
`references/amazon-image-strategy.md`. Other platforms have their own market-scoped
profiles; do not apply Amazon's slot ids, field layout or visual policy to them.

## Rendering defaults
- Render each selected AS/AD slot with one `generateImage` call.
- Use `scale: "1:1"` for carousel images unless the user requests another ratio.
- See `references/image-backend.md` for the current tool contract.

## Copy rules
- **Title (US snapshot)** ≤200 characters including spaces; category validation can add
  constraints. Avoid unsupported promotional wording and repetitive keyword stuffing.
- Amazon's current title guidance limits most words to two repetitions (excluding common
  articles/prepositions/conjunctions) and restricts special characters such as
  `! $ ? _ { } ^ ¬ ¦`, with a brand-name exception; the preflight warns on these for
  human review.
- **Bullets**: 5 is a useful drafting pattern in many categories, not a universal copy
  length rule. Use concise, evidence-backed points and check the current item-type fields.
- **Description**: write for the category and item type. No universal 1500–2000 character
  limit is asserted here; check the current submission schema.
- **Backend search terms (US)**: under 250 UTF-8 bytes; use spaces, do not repeat terms,
  and omit brand/product identifiers or temporary/promotional claims. Add relevant
  synonyms, abbreviations and alternate names; don't pad with misspellings or stop words.
- Cover ≥8 COSMO dimensions across the copy when helpful; this is an internal writing aid,
  not an Amazon attribute or compliance rule.
- Language: target-marketplace language; don't assume English for non-US sites.

## Image slot taxonomy
- **AM-01** — main image. Real white-background product photo; the skill never
  generates it, only reminds the user.
- **AS-02 … AS-09** — carousel/secondary images (核心卖点 / 功能 / 尺寸 / 场景 /
  细节 / 对比 / 步骤 / 包装). Default recommended set = 5–7 by buyer value.
- **AD-01 … AD-07** — detail-page / A+ modules (editorial, wider). Default 5–7.
- **AV-01** — optional video slot (prompt only).

## Compliance
- Amazon US main image: accurate photo on pure white, exact product/accessories shown,
  product occupies at least 85% of the frame, no added text/graphics except narrow
  category/swatches exceptions. Generated secondary visuals must still accurately depict
  the item.
- No competitor brand names in comparison images.
- Check category, image-count, zoom/aspect and variation rules in Seller Central before
  upload. Market-specific language follows the selected site.

Source snapshots and scopes are recorded in `platform-rules.json`.
