# Mercado Libre profile

## Scope and listing model

- Always specify the site: for example MLM (Mexico), MLB (Brazil), MLC (Chile), MCO (Colombia) or another supported destination. Global Selling CBT and local seller listings are distinct flows.
- Resolve category and required attributes from the target site's current category API/template. Required fields and the maximum number of photos vary by category/listing type.
- For Global Selling CBT, the researched listing flow uses English source content; the destination site still affects category values, buyer-facing localization and compliance. Preserve source language and destination copy separately.
- This skill produces listing data and preflight; it does not authenticate, upload photos or publish an item.

## Image and listing guidance

- CBT image API snapshot: 500 px minimum, 1920 px maximum for the full (F) version, up to 10 MB, JPG/JPEG/PNG. RGB is recommended; photos larger than 800 px can activate zoom. Category-level maximum image count is dynamic.
- Official listing guidance recommends more than three useful images and discusses square/1200×1200 as a strong default, but category-specific background and image rules can override generic advice. Never make a square aspect ratio a hard acceptance rule.
- Suggested image slots: principal product, alternate sides, detail, scale/dimensions, use, and included parts; vary by category and product evidence.
- Avoid watermarks, logos, promotional text and visual claims unless the current site's category rules specifically allow the content. Preserve exact package contents and model/variation.

## Preflight

1. Select site code, listing flow (CBT/local), category, condition and language.
2. Load required/category-required attributes and site restrictions.
3. Check dimensions, format and file size; confirm category max photo count using the current API/listing UI.
4. Validate item title, attributes, images and variants together so all describe the same sellable item.

Sources and review dates are recorded in [`platform-rules.json`](platform-rules.json).
