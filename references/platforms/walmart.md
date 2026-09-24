# Walmart Marketplace profile

## Scope and listing model

- Always ask for the target market and item/product type. Walmart's US setup uses product-type feed specifications and product-type attributes; variants must share a variant group and carry SKU-level values.
- Prepare the common product facts once, then map them into the selected market's Walmart item-spec template. Do not invent a universal field list.
- This repository has numeric image data for **Canada**. The US profile is supported for structured content planning, but US image dimensions and upload rules must be checked in Seller Center before release.
- A listing kit is an export/preflight artifact. This skill does not publish to Walmart or read an authenticated seller catalog.

## Listing content and images

- Keep the title factual and scannable. Use the current category template and avoid promotional/unsupported claims.
- Map product identity, brand, identifiers, item type, attributes, variant group/SKU, and media URLs into the template. Keep one record per sellable SKU.
- Suggested image plan: primary product image, alternate angle, detail/material, scale/dimensions, in-use context, package contents. Treat this as a content plan, not a required slot count.
- Walmart Canada guide snapshot: JPG/JPEG/PNG/BMP, sRGB, square images, 2200×2200 recommended, 1000×1000 minimum for zoom, and file size ≤5 MB. 2200 is a recommendation; image/category eligibility and exact URL/feed behavior still need live checking.
- Do not apply the Canada numeric values to Walmart US without checking its current US item-type and image requirements.

## Preflight

1. Select country + item type and download/use its current Seller Center feed schema.
2. Match each listing field and each variant SKU to the schema; do not flatten variant-specific dimensions, color or identifiers into the parent.
3. Check live image rules, identifiers, required attributes, URL accessibility and product type.
4. Confirm price, inventory, shipping and fulfillment in Seller Center. They are outside this image/listing-content generator.

Sources and review dates are recorded in [`platform-rules.json`](platform-rules.json).
