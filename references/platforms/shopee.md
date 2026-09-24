# Shopee profile

## Scope and listing model

- Shopee is a multi-country marketplace. Ask for destination site and listing language; do not reuse Singapore's advice as a global policy.
- Destination-specific categories, mandatory attributes, title rules, image upload limits, size/weight units, variation model and restricted-product rules must come from that country's Seller Centre or current API/template.
- Prepare one localized listing record per country. Keep source facts and local-language copy side by side so human review can compare them.

## Singapore image guidance snapshot

Shopee Singapore Ads' product-detail guidance recommends actual, realistic product photos; a product occupying more than half the image; at least 1024×1024; square 1:1; a clean simple background and white cover image. It permits informative images such as size charts/how-to images, but says not to show accessories outside the purchase and advises against watermarks or distracting graphics. These are **official recommendations from an Ads/PDP guide**, not a universal upload contract for every Shopee country.

## Initial shared image baseline

For the first release, reuse the supplied image workflow across all supported Shopee markets. Localize the listing language, image text, units and market-specific product facts; do not create separate image limits per country until Seller Centre research justifies that split. Keep this as a configurable project baseline, because country/category upload checks can still override it.

- Export square 1:1 images, normally at 1024×1024 px or larger; use 800×800 px as the initial minimum-dimension preflight threshold.
- Use JPG/JPEG or PNG and target no more than 2 MB per image.
- Plan at least 3 distinct images, with up to 9 gallery slots; aim for 6–8 useful images on a typical listing and do not pad the gallery.
- These format, threshold, size and count values are the initial shared project defaults from the supplied Shopee workflow, not claims that every country's live Seller Centre enforces identical limits. Preserve the defaults while allowing later per-market overrides.

## Gallery planning template

Use these as shared content slots, not as a reason to fill every gallery. Plan for 6–8 distinct images for an ordinary product, omit slots that add no new information, and do not fill all nine just to reach a number.

| Slot | Purpose | Evidence and accuracy check |
| --- | --- | --- |
| 1. Cover | Clean white or simple solid background; show the complete, exact item being sold | Keep the product unobstructed and uncropped. Use 60%+ of the frame as the shared composition target; the Shopee SG guide separately recommends more than half. |
| 2. Angles/states | Front, side, back, opened, folded or other useful states | Use real product views; do not repeat the cover with only a layout change. |
| 3. Key benefits | Explain 2–4 short, factual benefits | Support each claim with supplied product facts or visible evidence; avoid unsupported superlatives and guarantees. |
| 4. Detail | Show interfaces, texture, seams, zipper, buttons or workmanship | Match the actual SKU and avoid magnification that misrepresents scale. |
| 5. Size/capacity | Label dimensions, capacity, fit or weight | Use verified values, correct arrow direction and units; disclose measurement tolerance only when known. |
| 6. Use scene | Show a plausible use and environment | Keep props from appearing included and do not imply performance the product cannot support. |
| 7. Colors/specs | Show available colors, models or variants | Match each image to its actual SKU; exclude unavailable colors and combinations. |
| 8. Package contents | Show quantity, included accessories, gifts and box contents | Include only items actually shipped, and label set quantities clearly. |
| 9. Trust/notes | Explain verified material, inspection, installation or after-sales information | Include only claims supported by documentation or confirmed seller policy; never invent certifications or service promises. |

For the cover, use realistic product imagery on a clean white or simple solid background. Keep contact details, QR codes, external links, promotional badges, borders, collage layouts and large text out of the cover by default; verify destination and seller-program rules before making exceptions. Shopee Mall rules may differ from standard shops; the supplied Mall PDF remains unverified as to current version, so confirm its applicability before treating Mall-only details as platform policy. Pippit's article is a third-party content-planning reference, not a source of platform policy.

## Listing/story structure

- Localized title with product type, brand/model if authorized, key attribute, size/quantity and intended use where useful.
- Category attributes first; complete required attributes before polishing long descriptions.
- Use the gallery template above to map each image to a buyer question; prefer distinct information over repeated angles or text-heavy variants.
- Use local units, currency/country-specific labels, and natural native copy. Do not machine-translate claim-heavy image text without review.

## Preflight

1. Select country code and native language; resolve category and current Seller Centre upload rules.
2. Confirm the actual product, bundle contents and variation-specific images.
3. Apply the shared image baseline, then check current title, image dimensions/file limits, prohibited content and required attributes in that market. Record any verified market-specific override instead of silently changing the shared profile.
4. Confirm whether the shop is a standard seller or Shopee Mall before applying program-specific image rules.
5. Record the Seller Centre/template or Mall-guideline version and review date if the public guidance is incomplete.

Source and review date are recorded in [`platform-rules.json`](platform-rules.json).
