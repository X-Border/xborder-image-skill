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
   A style/competitor reference image never replaces the product photo in
   `referenceImageUrl`; it contributes extracted style DNA in the prompt, or rides the
   dual-reference exception in item 3.
2. **Full image set.** Plan the selected slots and tell the user how many output images
   will be generated. Build one evidence-backed shared product baseline, then call
   `generateImage` once per slot with that same baseline and reference image. The current
   MCP has no batch preset tool.
3. **Pure text-to-image — `generateImageFromText`.** Use when there is no product photo,
   or for a scene/background/concept generated from text. References are optional. Do not
   use it for a slot that must preserve an existing product's identity — identity
   preservation requires the reference-edit path (`generateImage` with the product photo
   as `referenceImageUrl`) — with one exception: when a slot genuinely needs two images
   at generation time (product photo + style reference), `generateImageFromText` may
   carry `referenceImageUrls = [product photo, style reference]`, product photo first,
   with the prompt naming which URL is the identity anchor and which is style-only. That
   output must pass the output drift audit before any consistency claim.
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

## Output drift audit (product consistency verification)

Prompt-side reference clauses request consistency; they do not verify it. To guarantee
that a generated image matches the provided product photo, call `analyzeProductImage`
on the generated image URLs (1-4 per call, one analysis credit per call) with `focus`
set to a baseline-comparison instruction, then compare the returned attributes against
the shared product baseline: shape/construction, proportions, colour/finish, Logo and
printed text, component placement, accessory set, and product-instance count/variant
allocation.

Default the audit **on** for multi-image sets and for product-instance quantity or
variant edits; run it elsewhere on request. State the audit's credit cost the first
time it applies. Skip it only when the user explicitly declines the cost — results then
remain pending-review previews and the completion message must not claim consistency
was checked.

For sets of 5+ slots, generate the 2 highest-value slots first, audit them, and only
then spend credits on the remaining slots. A passing sample audit continues the run
without pausing; a failing one is fixed via revision routing below before the rest of
the set is generated.

## Revision routing (smallest responsible layer)

When the audit or the user's review finds a failure, fix the smallest layer; never
regenerate the whole set by default:

| Failure | Fix | Regenerate |
|---|---|---|
| On-image copy wrong or garbled | revise that slot's exact text lines | that slot only |
| Product drift: shape, colour, Logo, count, component placement | strengthen the reference clause, naming the exact drifted attribute | that slot only, at most once |
| One slot's layout or hierarchy weak | revise that slot's layout decision | that slot only |
| Same defect across most slots | revise the shared baseline or style direction | affected slots, after the shared fix |
| Wrong slot plan or narrative | return the shot plan to the user for review | only what the new plan changes |

A drift-triggered regeneration is bounded like an error retry: one attempt per slot,
then report the audited difference and wait for the user.

## After rendering

Surface returned image markdown/URLs clearly. Treat every generated product image as a
preview. Ask the user to compare product identity, shape, construction, colours,
materials, texture, pattern, logo, existing text, quantity, and accessories against the
reference before publishing. Unless output images were successfully analyzed, do not
claim those properties passed inspection; report only the tool status and a comparison
checklist. Run the output drift audit above whenever consistency must be verified
rather than assumed.
