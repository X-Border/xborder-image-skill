# Platform profile — Temu

Temu is a cross-border discount marketplace (US-first, expanding globally), mobile-first
and price-driven. Listings are cleaner and shorter than Amazon: concise title, a few
punchy selling points, attribute-heavy specs, and clean square images. Reuse the shared
flow (SKILL.md STEP 0 modes, image backend, Excel) and the image-craft principles; only
the copy rules and slot taxonomy below are Temu-specific.

## Rendering defaults
- Temu is mobile-first: render each selected slot with `generateImage`, `scale: "1:1"`.
- See `references/image-backend.md` for the current tool contract.

## Copy rules (Temu)
Temu ≠ Amazon: no fixed 5×(150–200) bullets, no 1500-char description, no 250-byte
backend field. Keep it short, scannable, attribute-rich.

- **Product name / title**
  - Format: `[Core noun] [key attributes: material · size · color] [primary use]`.
  - Keyword-front-loaded, mobile-legible. Practical length ≈ 100–130 chars (Temu allows
    more, but concise converts on mobile).
  - No ALL-CAPS spam, no promo text (SALE / % OFF / FREE), no brand/competitor names,
    no emoji.
- **Selling points**: 3–6 short benefit lines, one concrete idea each (function, material,
  fit/size, care, package). Not the Amazon bullet formula.
- **Description**: ~300–800 chars, scannable — what it is, key specs, main use cases,
  care/warranty. Front-load the buying reason.
- **Attributes / specs**: fill category attributes thoroughly (material, dimensions,
  weight, capacity, care, compatibility) — Temu is attribute-driven and this feeds
  search + filters.
- **Search keywords**: a handful of relevant search terms/tags (no byte budget); include
  synonyms and common buyer phrasing.
- **Language**: English (US) default; localise to the target region when specified.

Adjust STEP 2 display: header `🛒  TEMU LISTING · [Product]`, show Title / Selling
points (3–6) / Description / Specs / Keywords instead of the Amazon 5-bullet + backend layout.

## Image slot taxonomy (Temu) — square 1:1, mobile-first
- **TM-01 主图 (main)** — clean product on pure white, fills the frame, no text / logo /
  watermark / border / promo badge. Real photo strongly preferred; the skill reminds and
  does not generate a fake main.
- **TS-02 核心卖点图 (key benefit)** — one strong buying reason, big product, ≤1 headline
  + 2–3 short badges.
- **TS-03 场景使用图 (lifestyle / in-use)** — real setting, product in use.
- **TS-04 细节/材质图 (detail / material)** — macro of the material, mechanism, or key part.
- **TS-05 尺寸/规格图 (dimensions / spec)** — dimension lines + mini spec. **Apparel /
  shoes: a clear size chart here is effectively mandatory.**
- **TS-06 白底多角度 (white-bg multi-angle)** — 1–2 extra clean angles on white.
- **TS-07 包装/配件 (what's in the box)** — optional, when accessories/packaging matter.

Default recommended set: **5–6** (real main + 4–5 generated). Temu carousels typically
run 5–10 images; do not pad weak slots.

## Compliance (Temu)
- **Main image is strict**: pure white background, product only, no text / logo /
  watermark / borders / collage / promo badges. This is the most common rejection cause.
- No misleading claims, no competitor brand names or logos, no price / discount text in images.
- Apparel / shoes / accessories: include a size chart image.
- Strong thumbnail hierarchy — Temu buyers browse on small mobile screens.
