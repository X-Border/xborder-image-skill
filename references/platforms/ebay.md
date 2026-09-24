# eBay profile

## Scope and listing model

- Default researched market: US. Require the actual eBay site, category and condition before finalizing specifics.
- Keep product facts separate from the offer: title, description, item specifics/aspects and image URLs belong to the inventory item; price, quantity, marketplace and policy belong to the offer.
- Category aspects and variation rules are dynamic. Use the category's current item-specifics/API metadata when available.
- The skill produces a listing package; it does not create inventory items or publish offers.

## Content and photo plan

- Build a concise factual title from brand (when authorized), product type, model, differentiating attribute and size/quantity.
- Item specifics: preserve exact brand, MPN/GTIN, condition, material, dimensions, color, compatibility and variation values when provided. Flag missing required aspects rather than guessing.
- Image story: exact item/primary view, opposite or alternate angle, detail, scale, use context, and what's included. For used/damaged/defective goods, use photos of the actual item.
- eBay guidance snapshot: minimum 500 px on the longest side; 1600×1600 is recommended; up to 24 listing photos, with variation/category exceptions; 12 MB max per image. Supported upload formats listed in the source include JPG/JPEG, PNG, GIF, TIFF, BMP, WEBP, HEIC and AVIF.
- Picture policy disallows misleading images and added borders, text/artwork or watermarks. A semantic image check remains manual.

## Preflight

1. Select marketplace site, category, condition, and whether the item has variations.
2. Resolve category aspects/required specifics and variation-specific values.
3. Check each image file and the current listing editor/API limits; do not assume every format works in every upload path.
4. Separate inventory content from offer price, quantity, shipping and return settings.

Sources and review dates are recorded in [`platform-rules.json`](platform-rules.json).
