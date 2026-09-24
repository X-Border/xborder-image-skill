# Research and open-source design notes

Reviewed 2026-09-24. This note records inspiration and how it was adapted; no third-party
source code or platform-policy text is copied into the implementation.

## Open-source image-skill patterns

- [motiful/product-shots](https://github.com/motiful/product-shots) (MIT): a set of focused
  product-shot workflows rather than one giant prompt. Adapted here as platform profiles
  plus a shared render/evidence pipeline, and as separate image story beats for cover,
  details, angles and marketing modules.
- [Gayaya999/ecommerce-detail-page-generator](https://github.com/Gayaya999/ecommerce-detail-page-generator):
  policy-aware detail-page generation, explicit fact provenance, structured intermediate
  data and deterministic preflight. Adapted as the facts ledger, normalized listing
  manifest, source-scoped machine-readable rules and a validator/export path. The project
  is cited as architectural inspiration only; no files were copied.

The shared skill principles also preserve product identity across a generated image set,
keep source facts and design choices separate, and require a source sample/metadata before
adding new platform constraints. Platform data here remains original, with source URLs
and market scopes recorded beside each rule.

## How to read the platform snapshot

- A source published by a seller center may be market-specific and may change. The access
  date here is a research checkpoint, not a freshness guarantee.
- A help-center article or Ads/PDP guide may be a recommendation, not an upload contract.
- When public official documentation does not expose category fields or image limits,
  the profile records the required Seller Center/API lookup instead of fabricating a
  numeric limit.
- Mercado Libre CBT rules do not automatically apply to local listings. Walmart Canada
  image limits do not automatically apply to the US. Shopee Singapore PDP advice does not
  automatically apply to other Shopee sites.

The machine-readable source register and rule status are in `platform-rules.json`.
