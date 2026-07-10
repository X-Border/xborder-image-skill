# Platform profile — Noon

Noon is the leading Middle East marketplace (UAE, KSA, Egypt). It is catalog- and
attribute-driven, bilingual **English + Arabic**, and culturally sensitive. Reuse the
shared flow (SKILL.md STEP 0 modes, image backend, Excel) and image-craft principles;
only the copy rules, slot taxonomy, backend knob, and compliance below are Noon-specific.

## Backend knob (for `generateListingImageSet`)
- `marketplace: "noon"`
- `preset: "noon_standard"` (1 seller / 2 scene / 2 close-up / 1 white close-up /
  3 white-bg) — Noon leans on clean white-background gallery shots.
- `language: "英语阿拉伯语"` (English + Arabic) and `salesRegion: "中东"` when the user
  targets the GCC; adjust `language` to `"英语"` only when Arabic is not needed.
- Per-slot renders: `generateImage`. See `references/image-backend.md`.

## Copy rules (Noon)
- **Title**
  - Format: `[Brand] [Product type] [Key attributes: model · size · color · material]`.
  - Concise, English primary; provide an Arabic title when the listing targets Arabic
    buyers. Practical length ≈ 150–200 chars.
  - No promo text, no ALL-CAPS spam, no competitor names.
- **Highlights / key features**: 3–5 short highlight lines (Noon "Overview"/highlights),
  one concrete benefit each.
- **Description**: concise rich description; bilingual EN / AR is a plus for GCC.
- **Category attributes**: fill Noon's required category fields (brand, model number,
  material, dimensions, etc.) — Noon is attribute-strict and rejects incomplete catalog data.
- **Search keywords**: relevant EN + AR search terms.
- **Language**: English + Arabic (Arabic is RTL). Default English; add Arabic for GCC.

Adjust STEP 2 display: header `🛒  NOON LISTING · [Product]`, show Title (EN, + AR if
provided) / Highlights (3–5) / Description / Attributes / Keywords.

## Image slot taxonomy (Noon)
- **NM-01 主图 (main)** — pure white background, product centered, meets Noon's minimum
  resolution (~1000px+ on the long edge), no text / logo / watermark. Real photo strongly
  preferred; the skill reminds and does not generate a fake main.
- **NS-02 核心卖点图 (key benefit)** — one strong buying reason; EN or EN+AR text.
- **NS-03 场景使用图 (lifestyle)** — culturally-appropriate Middle-East setting (see
  compliance): modest attire, region-appropriate interior.
- **NS-04 细节/材质图 (detail / material)** — macro of material, mechanism, or key part.
- **NS-05 白底多角度 (white-bg multi-angle)** — 2–3 clean white-background angles (Noon
  gallery favours these).
- **NS-06 尺寸/规格图 (dimensions / spec)** — dimension lines + mini spec; bilingual size
  chart for apparel / shoes.
- **NS-07 包装/配件 (what's in the box)** — optional.

Default recommended set: **5–7** (real main + generated).

## Compliance (Noon) — Middle East cultural rules (IMPORTANT)
- **Cultural imagery**: keep imagery modest and region-appropriate — appropriate model
  attire (covered arms/legs; women's fashion shown modestly), no alcohol, pork, gambling,
  or religiously sensitive content. For food / cosmetics, respect halal considerations.
- **Arabic text**: Arabic is right-to-left. If you add Arabic overlays, ensure correct RTL
  rendering and native, natural phrasing — do not ship literal machine-translation text.
- **Main image**: pure white background, no text / logo / watermark; meet Noon resolution
  minimums.
- **Bilingual**: provide EN + AR where the target market expects it.
- No competitor brand names, no misleading claims.
