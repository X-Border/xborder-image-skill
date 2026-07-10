# Image generation backend — X-Border MCP tools

**Reusable, platform-agnostic.** Every platform profile (`references/platforms/*.md`)
points here for the actual image rendering. Do not duplicate this contract inside a
platform file — only override the `marketplace` / `preset` values.

This skill builds image *briefs* (the `$imagegen [...]` blocks in the platform flow).
This file explains how a brief becomes a rendered image via the X-Border image MCP
tools. The skill itself never holds any provider API key — X-Border's `api-server`
holds the image credentials server-side and exposes these tools over MCP.

## Availability

These tools exist only when the host chat has the **`x-border` MCP** connected
(auto-installed on SSO login; auto-enabled once installed). If the tools are **not**
present, fall back: output the `$imagegen` prompt text in chat and still write prompts
into Excel when Excel was requested. Never claim an image was generated when no tool
was called.

## Input images are URLs, never base64

In X-Border chat, uploaded product photos arrive as URLs (rendered as
`<image ref="..." url="https://...">`). Pass those URLs directly to
`referenceImageUrl` / `imageUrls`. If a user pasted a local/base64 image and no URL
is available, ask them to upload it so it becomes a public URL first.

## Source-image hygiene (1688 / supplier photos)

The `generateImage` models (nano-banana-pro / seedream-4.5 / qwen-edit-multiangle) are
**edit models** — they use the reference photo as a base and preserve regions they are
not told to change. Sourcing photos from 1688 / Taobao / suppliers routinely carry
baked-in watermarks, shop/marketplace logos, promo badges, price tags, and Chinese
marketing text. Left alone (and especially with a "match the reference exactly"
instruction), those marks get **carried into the output** — which fails Amazon/Temu/Noon.

Every slot brief you send to `generateImage` must include a removal clause, e.g.:

> "Remove any watermark, overlay/promo text, shop or marketplace logo, price tag, and
> Chinese marketing graphics from the source image; reconstruct that area cleanly and
> keep only the real product. All visible text in the output is <marketplace language>."

**Two-pass for dirty sources.** When the photo has a heavy watermark or lots of baked-in
Chinese, do it in two passes:

1. **Clean pass** — call `generateImage` with `prompt` = "Remove all watermarks, overlay
   text, logos, price tags and Chinese marketing text; keep the exact product on a clean
   white background, no added text." Use the returned clean image URL as the new reference.
2. **Slot pass** — run the normal per-slot briefs using the cleaned image as
   `referenceImageUrl`.

**Honest limit:** edit models cannot always fully erase large watermarks or text printed
on the product itself. If a clean result isn't achievable, tell the user and recommend a
clean white-background source photo — do not claim a perfectly clean output.

## Which tool to use (decision tree)

1. **Per-slot art direction — DEFAULT for this skill.** The skill's value is the
   detailed per-slot brief (key benefit, dimensions, lifestyle, detail …). Render each
   selected slot with **`generateImage`**, one call per slot:
   - `prompt` = the slot's `$imagegen` brief (strip the leading `$imagegen`, ≤2000 chars)
   - `referenceImageUrl` = the product photo URL (required on the default provider)
   - `scale` = slot aspect (`1:1` marketplace carousel, `16:9`/`9:16` for wide/mobile)
   - `outputNum` = 1 unless the user wants variants
   - `model` (optional) = `nano-banana-pro` (default) / `seedream-4.5` (higher quality,
     honours aspect) / `qwen-edit-multiangle` (angle changes). Pass when the user names
     a model or a slot benefits from one.
   - Default provider (x-border-ai) returns the image directly. Only when the deployment
     uses the `linkfox` provider do you poll `getImageTaskResult({ taskToken })` on a
     returned `taskToken`.

2. **One-click full set — fast path.** When the user just wants "整套上架图 / 快 / 一把出"
   and does not need per-slot control, call **`generateListingImageSet`** once with the
   active platform's `preset`/`marketplace` (Amazon → `amazon_standard`/`amazon`, Noon →
   `noon_standard`/`noon`, Temu → `marketplace_basic`/`temu`). Counts come from the
   preset, NOT the slot selection — say so before generating.

3. **Custom counts.** When the user names specific quantities, call
   **`generateProductMarketingImages`** with explicit `sellerTypeNum` / `sceneTypeNum` /
   `closeUpTypeNum` / `closeUpWhiteTypeNum` / `whiteBgTypeNum` / `aPlusNum` / `aPlusProNum`.

4. **Single slot / "参考这张重做".** Use `generateImage` (tool 1) for that one slot.

## Tool reference (exact params)

### `generateImage` (returns image directly, or a `taskToken` to poll)
Default provider **x-border-ai** is synchronous and requires a `referenceImageUrl`.
| param | type | notes |
|---|---|---|
| `prompt` | string ≤2000 | required; the slot brief |
| `referenceImageUrl` | url | product/reference photo (required for x-border-ai) |
| `model` | `nano-banana-pro` \| `seedream-4.5` \| `qwen-edit-multiangle` | x-border-ai only; default `nano-banana-pro`. Ignored by linkfox. |
| `style` | string ≤120 | optional, e.g. 场景素材 / 写实 |
| `scale` | `1:1` \| `16:9` \| `9:16` | default `1:1` (aspect honoured on seedream-4.5) |
| `outputNum` | 1–4 | default 1; bills per image |
| `waitSeconds` | 0–180 | linkfox only: sync wait; on timeout returns `taskToken` |

### `getImageTaskResult`
| param | type | notes |
|---|---|---|
| `taskToken` | string | from a linkfox `generateImage` / timed-out set call |
| `format` | string | LinkFox currently jpg only |

### `generateProductMarketingImages` (batch, custom counts — LinkFox)
| param | type | notes |
|---|---|---|
| `imageUrls` | url[] 1–5 | required product photos |
| `sellerPoint` | string ≤2500 | required unless `autoExtractSellerPoint: true` |
| `sellerTypeNum` / `sceneTypeNum` / `closeUpTypeNum` / `closeUpWhiteTypeNum` / `whiteBgTypeNum` / `aPlusNum` / `aPlusProNum` | int 0–12 | per-type counts |
| `aspectRatio` | `1:1`,`4:5`,`16:9`,`9:16`,… | default `1:1` |
| `noText` | bool | text-free layout |

### `generateListingImageSet` (batch, preset-driven — platform aware, LinkFox)
| param | type | notes |
|---|---|---|
| `imageUrls` | url[] 1–5 | required |
| `sellerPoint` | string ≤2500 | required unless `autoExtractSellerPoint` |
| `preset` | `marketplace_basic`\|`white_background_pack`\|`amazon_standard`\|`noon_standard`\|`premium_marketing` | default `marketplace_basic` |
| `marketplace` | `amazon`\|`noon`\|`temu`\|`shein`\|`tiktok`\|`generic` | writes platform/salesRegion; does NOT set counts |
| `language` | string | e.g. 英语 / 阿拉伯语 / 英语阿拉伯语 |
| `salesRegion` | string | e.g. 中东 / 北美 |
| `brandColor` | `#RRGGBB` | optional |

## Platform → preset / marketplace map (the only per-platform knob)

| platform | `marketplace` | `preset` | preset composition (seller/scene/closeUp/closeUpWhite/whiteBg/aPlus/aPlusPro) |
|---|---|---|---|
| Amazon | `amazon` | `amazon_standard` | 3 / 2 / 1 / 1 / 2 / 1 / 0 |
| Noon | `noon` | `noon_standard` | 1 / 2 / 2 / 1 / 3 / 0 / 0 |
| Temu | `temu` | `marketplace_basic` | 2 / 1 / 1 / 1 / 1 / 0 / 0 |
| TikTok Shop | `tiktok` | `marketplace_basic` | 2 / 1 / 1 / 1 / 1 / 0 / 0 |
| Shein | `shein` | `white_background_pack` | 0 / 0 / 0 / 2 / 3 / 0 / 0 (noText) |
| generic | `generic` | `marketplace_basic` | 2 / 1 / 1 / 1 / 1 / 0 / 0 |

`premium_marketing` (4 / 3 / 2 / 1 / 2 / 1 / 1) is an upsell preset available to any
platform when the user asks for a richer set.

## After rendering

Surface the returned image markdown / URLs to the user clearly. Keep the main-image
(real white-background photo) reminder that the platform flow specifies. If a linkfox
call timed out and only a `taskToken` came back, tell the user it is still processing
and poll `getImageTaskResult` before declaring the slot done.
