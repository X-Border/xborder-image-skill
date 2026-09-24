# Noon profile

## Scope and market inputs

- Require the destination country (AE, SA, EG or another active Noon market), content
  language and category. English/Arabic needs and category attributes vary by site/product.
- Load current Noon Seller Lab fields for the seller SKU; this profile is not a replacement
  for that live schema.
- The listing package covers content and images. It does not create the SKU, price,
  inventory or shipping offer.

## Copy structure

- Title: concise product type plus identifying, category-relevant details. Noon’s title
  guide says to exclude the brand name, avoid promotional/search-stuffed wording and
  repeated words, and use title case (while allowing appropriate acronyms such as LED).
  The article gives conflicting length guidance: its main section says 5–200 characters,
  while rejection examples say 20–160. The profile uses 20–160 as a warning-only,
  conservative working range; confirm the live Seller Lab field and category behavior.
- Keep the brand in the separate brand field, exactly matching the actual product/brand
  record; do not copy an uncertain logo from a marketing render into listing data.
- Highlights: 3–5 useful, evidence-backed points as an editorial recommendation.
- Description and category attributes: preserve exact specifications, care, compatibility
  and required warnings. Include Arabic only when the selected site/content flow needs it;
  any Arabic on-image copy should receive native review.

## Gallery and image requirements

- Noon’s public image guide specifies JPG/JPEG only, width ≥660 px, width-to-height ratio
  ≥0.5, resolution ≥72 PPI, RGB/sRGB, and ≤10 MB per image. It recommends at least three
  high-quality images. These rules are recorded in the AE profile; verify the destination
  country and live upload flow before release.
- For non-fashion items, the primary image should be a full front view on pure white,
  outside packaging; lifestyle primary images are not permitted, and only light shadows
  are accepted. Do not crop product parts or add packaging, tags, borders, watermarks,
  seller names or seller logos.
- Additional images must still be photographs of the actual product. Noon expressly
  disallows CAD drawings, thumbnails and illustrations. Keep the item clear and occupying
  about 70–80% of each additional frame; do not show accessories not included. Short,
  relevant text can be added, but avoid poster-like infographic compositions and inspect
  every exact output against the current Seller Lab review.
- Recommended sequence: primary front, back, side, other angle, details, usage. Three is
  the public recommendation minimum; add more only when each image answers a distinct
  buyer question.
- Noon’s image guide includes framing guidance (vertical shots: top/bottom margins;
  horizontal shots: side margins). Use safe breathing room and do not stretch the photo.
- A+ / A+ content has separate sizing and asset rules; do not validate those banners with
  the product-gallery image profile. See the official A+ source listed in
  `platform-rules.json`.
- Suggested story beats: primary product, distinct angle, detail, dimensions/size chart,
  use scene and package contents. Treat count as guidance, not a universal fixed quota.

## Localization

- Keep imagery locally appropriate without adding unsupported cultural prohibitions.
  Product, content and legal restrictions must be checked for the target market/category.
- Use correct RTL layout and human-reviewed Arabic when Arabic is requested or required.

Before publishing, resolve current Seller Lab category fields, market-specific image
exceptions and content language. The public title page contains inconsistent title-length
benchmarks; this profile intentionally treats 20–160 as a warning range, not a verified hard
limit. Sources and review date are in `platform-rules.json`.
