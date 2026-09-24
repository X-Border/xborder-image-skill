# TikTok Shop US image-set self-test

Synthetic capability test of the repository skill. TikTok Shop US is an explicit test assumption because the current profile contains US rules only.

## Gallery plan

1. Main image — pure white background, complete item, no overlay.
2. Alternate side view — one distinct camera angle.
3. Open storage state — demonstrates the lid/storage state.
4. Detail — lid and side seam close-up.
5. Use scene — stool beside a living-room sofa.
6. Package contents — `1 Stool Included` based on a test-only assumption; confirm actual shipped quantity.

Dimensions, alternate colors/SKUs, strength or material claims, and trust/after-sales slides were omitted because the test data does not substantiate them.

## Test limitations

- **Production readiness: blocked.** TikTok Shop US listing images disallow digital renderings; these six files were generated for a capability test, so they are not uploadable product assets. The package also lacks a real identity-anchor photo, verified facts, resolved category fields, a current Seller Center check, and final human review.
- The identity-anchor image was generated for this test and is not a photograph of a real sellable product. Replace it with the actual product photo before any listing use.
- The skill's X-Border renderer and `analyzeProductImage` drift-audit tool were unavailable. The images were generated with built-in `image_gen`; they remain pending review and product consistency was not formally audited.
- Visual review found the first alternate-angle attempt cropped the product. It was regenerated once with full-product framing; the saved side-view is the corrected attempt.
- Listing schema, package quantity, required category fields, and live Seller Center checks remain unresolved.
