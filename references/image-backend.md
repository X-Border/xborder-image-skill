# Image generation backend — X-Border MCP tools

**Reusable, platform-agnostic.** Every platform profile (`references/platforms/*.md`)
points here for image rendering. This skill builds image briefs; X-Border's private
`api-server` holds provider credentials, billing, routing, and prompt safety controls.

## Availability

The tools exist only when the host chat has the **`x-border` MCP** connected. If they are
not present, output the image prompt text in chat and still write prompts into Excel when
requested. Never claim an image was generated when no tool was called.

## Input images are URLs, never base64

Uploaded product photos arrive as URLs (`<image ref="..." url="https://...">`). Pass
those URLs directly to `referenceImageUrl` / `referenceImageUrls` / `imageUrls`. If no
public URL is available, ask the user to upload the image first.

## Risky-edit preflight

Apply `SKILL.md` STEP 0A to the **original user request** before rewriting a prompt. For a
product-instance quantity edit involving multiple variants, visual references, relative
changes, or conflicting totals, ask one confirmation question and wait. Do not call a
billable image tool in the same turn as the question.

After confirmation, the tool prompt must explicitly repeat every confirmed fact, for
example: `black variant = exactly 1; white variant = exactly 2; total = exactly 3;
horizontal layout; change image text to "3pcs"`. Never silently swap variant counts.

Keep output-image count separate from product-instance count: five listing slots means
five tool calls; it does not mean five products inside each image.

## Source-image hygiene (1688 / supplier photos)

Supplier photos often contain watermarks, shop logos, promo badges, price tags, and
Chinese marketing overlays. These are not product facts. Add a removal clause when
needed:

> Remove any watermark, overlay/promo text, shop or marketplace logo, price tag, and
> Chinese marketing graphics from the source image; reconstruct that area cleanly and
> keep only the real product. All visible text uses the target marketplace language.

For a heavily marked source, use two `generateImage` calls only when the user accepts the
extra image-generation cost:

1. Clean the source while preserving the exact product on a clean background.
2. Use the returned clean image URL as the reference for the requested slot.

Edit models cannot always erase large marks or text printed on the product. If cleaning
is unreliable, say so and recommend a clean source photo.

## Which tool to use

1. **Reference-image edit or listing slot — `generateImage`.** Use one call per output
   image. Pass the detailed slot brief as `prompt`, the product URL as
   `referenceImageUrl`, the requested aspect ratio as `scale`, and an optional model.
2. **Full image set.** Plan the selected slots and tell the user how many output images
   will be generated, then call `generateImage` once per slot. The current MCP has no
   batch preset tool.
3. **Pure text-to-image — `generateImageFromText`.** Use when there is no product photo,
   or for a scene/background/concept generated from text. References are optional.
4. **Product analysis — `analyzeProductImage`.** Use when product attributes or selling
   points must be extracted before planning. If it fails or returns no analysis, treat
   that as no visual evidence: do not guess from URLs, filenames, memory, or similar
   products.

## Tool reference (current public MCP schema)

### `generateImage`

Synchronous reference-image edit. Returns exactly one image and bills for one image.

| param | type | notes |
|---|---|---|
| `prompt` | string <=2000 | required edit/slot brief |
| `referenceImageUrl` | URL | required product/reference image |
| `style` | string <=120 | optional |
| `scale` | `1:1` \| `16:9` \| `9:16` | optional; default `1:1` |
| `model` | `nano-banana-pro` \| `seedream-4.5` \| `qwen-edit-multiangle` | optional |
| `claimedProductId` | UUID | optional X-Border product association |

There is no public `outputNum`, `waitSeconds`, or image task polling parameter. To create
multiple output images, call once per confirmed slot.

### `generateImageFromText`

Synchronous text-to-image; reference images are optional. Returns exactly one image and
bills for one image.

| param | type | notes |
|---|---|---|
| `prompt` | string <=2000 | required generation prompt |
| `referenceImageUrls` | URL[] 1-4 | optional references |
| `scale` | `1:1` \| `16:9` \| `9:16` | optional; default `1:1` |
| `model` | `seedream-4.5` \| `nano-banana-pro` \| `qwen-edit-multiangle` | optional; default `seedream-4.5` |
| `claimedProductId` | UUID | optional X-Border product association |

### `analyzeProductImage`

Reads 1-4 product images and returns structured e-commerce attributes plus a generation
prompt. Bills one analysis credit.

| param | type | notes |
|---|---|---|
| `imageUrls` | URL[] 1-4 | required product images |
| `focus` | string <=200 | optional emphasis |
| `model` | supported vision-model enum | optional |
| `claimedProductId` | UUID | optional X-Border product association |

On success, use only facts present in `analysis` or explicitly supplied by the user. On
failure, ask for another accessible image or continue only with explicit user facts.

## Tool error contracts

- `IMAGE_EDIT_CLARIFICATION_REQUIRED`: no image was generated or billed. Ask the returned
  clarification question once, wait for confirmation, then include every per-variant
  quantity and the total in the next prompt.
- `IMAGE_INTENT_REJECTED`: terminal for that requested operation. Do not weaken or remove
  the rejected operation and retry automatically. Explain the limitation and wait for a
  new user instruction.

## After rendering

Surface returned image markdown/URLs clearly. Treat every generated product image as a
preview. Ask the user to compare product identity, shape, construction, colours,
materials, texture, pattern, logo, existing text, quantity, and accessories against the
reference before publishing.
