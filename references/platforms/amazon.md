# Platform profile — Amazon (reference implementation)

Amazon is the fully-detailed platform. Its copy rules and per-slot image briefs live in
`SKILL.md` (STEP 1 copy, STEP 3 AS slots, STEP 3B AD modules) and
`references/amazon-image-strategy.md`. This file is the concise profile that Temu / Noon
are modeled on.

## Backend knob (for `generateListingImageSet`)
- `marketplace: "amazon"`
- `preset: "amazon_standard"` (3 seller / 2 scene / 1 close-up / 1 white close-up /
  2 white-bg / 1 A+)
- Per-slot renders use `generateImage` with the AS/AD brief — see `references/image-backend.md`.

## Copy rules
- **Title** ≤150 chars; primary keyword within first 80; Capitalise Every Main Word;
  no ALL-CAPS words, no promo words (Best/Free/Sale), no special chars.
- **Bullets** exactly 5, each 150–200 chars, leading `【ALL-CAPS LABEL】`, one COSMO
  pairing per bullet.
- **Description** 1500–2000 chars, 5 paragraphs (hook → solution → features → use-cases → close).
- **Backend search terms** ≤250 bytes, space-separated, no repeats; synonyms + misspellings + ES variants (US).
- Cover ≥8 COSMO dimensions across the copy.
- Language: target-marketplace language (default English / en-US).

## Image slot taxonomy
- **AM-01** — main image. Real white-background product photo; the skill never
  generates it, only reminds the user.
- **AS-02 … AS-09** — carousel/secondary images (核心卖点 / 功能 / 尺寸 / 场景 /
  细节 / 对比 / 步骤 / 包装). Default recommended set = 5–7 by buyer value.
- **AD-01 … AD-07** — detail-page / A+ modules (editorial, wider). Default 5–7.
- **AV-01** — optional video slot (prompt only).

## Compliance
- Main image: real photo on pure white; re-check Amazon's current image policy before upload.
- No competitor brand names in comparison images.
- Visible image-text language follows the target marketplace (default English).
