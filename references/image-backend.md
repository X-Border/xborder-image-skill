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
changes, or conflicting totals, ask one confirmation question before calling a billable
image tool. This is a helpful warning rather than a hard approval gate: if the user asks
to proceed with the current interpretation, generate without asking again.

After confirmation, the tool prompt must explicitly repeat every confirmed fact, for
example: `black variant = exactly 1; white variant = exactly 2; total = exactly 3;
horizontal layout; change image text to "3pcs"`. Never silently swap variant counts.
If the user chooses direct generation without resolving the ambiguity, preserve the
original wording instead of inventing a per-variant allocation and present the output as
a preview requiring quantity and variant review.

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
   will be generated. Build one evidence-backed shared product baseline, then call
   `generateImage` once per slot with that same baseline and reference image. The current
   MCP has no batch preset tool.
3. **Pure text-to-image — `generateImageFromText`.** Use when there is no product photo,
   or for a scene/background/concept generated from text. References are optional.
4. **Product analysis — `analyzeProductImage`.** Use when product attributes or selling
   points must be extracted before planning. For a multi-image set, wait for required
   analysis to complete before starting generation; do not run it in parallel with
   billable image calls. If it fails or returns no analysis, treat that as no visual
   evidence: do not guess from URLs, filenames, memory, or similar products. Ask for a
   usable image or explicit permission to proceed using only user-provided facts. Report
   only that analysis was rejected or unavailable; do not infer a policy violation,
   provider, safety category, or workaround that the tool did not explicitly establish.

## Shared baseline and claim integrity for image sets

Before a multi-image set, create one shared baseline from successful analysis and explicit
user facts. Copy it unchanged into every slot prompt. Lock product identity, count,
variant allocation, colours, construction, Logo/text, and accessories. When exact count
is not verified, instruct the model to preserve exactly the instances visible in the
reference and never add, remove, or duplicate one.

Only evidence-backed claims may appear as visible image text. Qualitative input does not
authorize an exact number: for example, `quiet` must not become `28 dB`. Omit unsupported
dimensions, performance numbers, certifications, material grades, percentages,
warranties, rankings, and comparison claims.

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

- `IMAGE_INTENT_REJECTED`: terminal for that requested operation. Do not weaken or remove
  the rejected operation and retry automatically. Explain the limitation and wait for a
  new user instruction.
- Other failed generation calls: retry the failed slot at most once, only when no image or
  usable output was returned. Never regenerate a successful slot automatically. After a
  second failure, report the slot and wait for the user before spending another attempt.

## After rendering

Surface returned image markdown/URLs clearly. Treat every generated product image as a
preview. Ask the user to compare product identity, shape, construction, colours,
materials, texture, pattern, logo, existing text, quantity, and accessories against the
reference before publishing. Unless output images were successfully analyzed, do not
claim those properties passed inspection; report only the tool status and a comparison
checklist.
