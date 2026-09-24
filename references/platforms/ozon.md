# Ozon profile

## Scope and listing model

- Default researched market and language: Russia / Russian. Ask for the destination country, language, account flow and category before producing publish-ready data.
- Ozon's Seller API and Seller Center schemas are versioned. Required attributes and accepted media fields depend on product type/category and API method; retrieve those definitions at runtime or from the user's current category template.
- The standard content package should preserve offer ID/SKU, product name, category, product attributes, price/stock/shipping as separate fields, images, 360 media/color image where relevant, and each variation as a separate sellable configuration.
- No universal image count or static attribute list is encoded here because public docs did not establish one across Ozon markets/API versions.

## Image and content workflow

- Keep listing name factual and localized; use the exact Russian product/category terminology supplied by Ozon's category and attribute dictionary.
- Suggested image story: primary exact product, detail, dimensions, use, package contents and variants. This is a planning suggestion, not Ozon's upload-count rule.
- Require the current category schema and image upload result before calling any output compliant. Keep API version, source method and fetch date with the export.
- Do not infer certificates, composition, compatibility or regulatory attributes from a rendered image.

## Preflight

1. Choose country, language, category and API/Seller Center flow.
2. Fetch or import current Ozon category tree/attribute definitions and required fields.
3. Check image methods, maximum count, dimensions and file rules from the selected current method/version.
4. Validate variations, offer IDs, localization and product-specific restrictions in Seller Center before upload.

Official Seller API entry point and review date are recorded in [`platform-rules.json`](platform-rules.json).
