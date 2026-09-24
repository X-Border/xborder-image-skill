---
name: xborder-image-skill
description: >
  Build marketplace listing kits from product photos, accessible product-page facts and
  selling points: listing copy, evidence-led selling-point sheets, platform-appropriate
  image plans/assets, a normalized manifest and (when requested) Excel for Amazon, Temu,
  Noon, Walmart, eBay, Etsy, TikTok Shop, Ozon, Shopee and Mercado Libre. Use when a user
  asks for listings, listing images, main/secondary images, product claims, localization,
  or listing-image audit/editing: 上架, 主图, 副图, 卖点图, 场景图, 尺寸图, 详情图, A+,
  listing, product images, generate/edit/review images, or provides a product photo or URL.
  Supports product photo and direct-image URL inputs; image generation follows each
  market's rules and may be preview-only where synthetic images are not allowed.
metadata:
  version: "1.6.0"
---

# X-Border Listing Image Skill

From product evidence and a target marketplace, create a listing kit: structured copy,
selling-point and image plans, images where the selected market permits them, and (when
requested) an Excel summary.
Supported profiles are **Amazon**, **Temu**, **Noon**, **Walmart Marketplace**, **eBay**,
**Etsy**, **TikTok Shop**, **Ozon**, **Shopee**, and **Mercado Libre**. Amazon keeps its
deep image workflow in this file; every platform's market-scoped rules and workflow are
in `references/platforms/`.
Images render through the X-Border image tools (`references/image-backend.md`) — this
skill holds no image keys.

This produces content and a preflight package; it does not upload, publish, price, or
manage inventory in seller accounts. Never claim marketplace approval from a local
check alone.

## Production release standard

Use four explicit delivery states in the manifest, workbook, and final response:

- **Blocked** — an enforced rule failed, a release gate failed, or core manifest data is
  invalid. Do not deliver the package as a candidate until corrected.
- **Concept / preview** — product identity, facts, market rules, or image review are
  incomplete. These files are for direction and must not be sent to a listing operator
  as final assets.
- **Human review required** — automated checks ran, but at least one evidence, image,
  category, localization, file, or live-policy gate is unresolved.
- **Candidate for manual upload** — all listed review gates are recorded as passed,
  scoped automated checks have no errors or warnings, required category fields and the
  dated live Seller Center/API check are recorded, and an operator has reviewed the
  exact files. This is the strongest status this skill can assign; it is not platform
  approval and it does not guarantee acceptance.

Never use “100% compliant”, “approved”, or “ready to publish” based only on generation
or a local validator. Missing evidence, a synthetic test identity image, inaccessible
source URLs, an unavailable analyzer/auditor without an equivalent human comparison, or
unresolved live category rules keep the package at **human review required**. A real
source image can still produce a draft; it does not by itself verify claims or prove
every generated angle matches the item.

For multi-image production work, save a selling-point sheet and a locked shot plan in the
manifest before rendering. Every image slot must state its buyer question, evidenced
message, visual proof, layout, and exact on-image text (or explicitly “no text”). A slot
without new buyer value is omitted. Keep the clean-background/no-overlay constraints
scoped to the platform's primary image. Gallery images can use stronger scenes,
contrast, callouts, and short localized copy when that market's rules permit it.

When exact text matters, render the product/scene with clean reserved text areas and add
copy using deterministic typesetting or a verified design/compositing step. Do not treat
AI-rendered letters as accurate. If no deterministic text step is available, label the
image as a visual draft and require a human text proof. Inspect every final file at
thumbnail and full size for product identity, quantity, variant, claims, text, cropping,
artifacts, localization, and platform-specific main-image treatment.

---

## Execution contract (non-negotiable)

The detailed rules live in the steps below and in `references/image-backend.md`; when
they seem to conflict with convenience or speed, this contract wins.

- **Evidence lock.** Never invent numeric specs, dimensions, certifications,
  performance claims, or comparison results. Qualitative input never authorizes a
  number ("quiet" ≠ "28 dB").
- **Honest tooling.** Never claim an image was generated, analyzed, or inspected
  without a successful tool result. Never write code or placeholder files to simulate
  generation or fake a deliverable.
- **Identity anchor.** The user's product photo is the identity anchor. On the edit
  path it fills `referenceImageUrl`, and a style/competitor reference image may never
  take its place. Reference images contribute style only — never their product, brand,
  person, or text.
- **Bounded spend.** At most one error retry and one drift regeneration per slot.
  Never regenerate a successful slot unasked. State billable audit calls the first
  time they apply and let the user decline.
- **Soft gates.** Ambiguity confirmations and sample checkpoints are bypassable
  warnings, not approval walls. When the user says to proceed, generate without
  re-asking; never loop the same question.
- **Plan lock.** Once the shot plan is set, prompt writing must not re-plan slots or
  rewrite the plan's exact on-image text lines. A needed change goes back through the
  plan, not into an ad-hoc prompt edit.
- **Internal vocabulary stays internal.** Slot ids (AS-04, AD-03, TS-02), module
  types, and planning field names never appear as visible text on generated images.
- **Scope stability.** Deliver the requested assets only; do not add websites,
  scripts, videos, extra formats, or unrequested image counts.
- **Market-scoped rules.** Require country/site and category when they affect fields,
  language or limits. Use `references/platforms/platform-rules.json`; never apply one
  country's rule to another. Distinguish sourced requirements, official guidance and
  recommendations. Dynamic category schemas and Seller Center rules remain live checks.
- **Structured evidence.** Normalize content and claims with
  `references/platforms/listing-manifest.schema.json`. Every factual claim must trace to
  a fact record; derived/unverified facts stay labeled and cannot become technical,
  numeric, safety or certification claims.

### Product-page URL and direct-image URL inputs

Treat a product-page URL and a direct image URL as different sources. For a public
product-page URL, inspect the page only if it is accessible; record each usable product
fact with the exact source URL and whether the page is the manufacturer, brand, seller,
or a marketplace listing. Manufacturer specifications and seller-written marketing
claims are not equally strong evidence. Do not treat reviews, inferred dimensions,
search snippets, variant menus, or a similarly named product as verified facts. A
marketplace page may describe a different seller's bundle or SKU.

For a direct image URL, pass the image URL to the image-analysis tool and wait for a
successful result before recording visual observations. A product-page URL is never an
image identity anchor: extract an accessible product-image URL first. If the page or
image is blocked, ask for an uploaded image, a direct image URL, or a spec sheet; do not
pretend the URL was read. Keep the URL and extracted fact provenance in the manifest.

---

## STEP 0 — Choose execution mode and read inputs

### STEP 0A — Preflight risky edits before any image tool call

Apply this gate to the **user's original request**, before rewriting it into a polished
image prompt. Do not treat your own inferred prompt as user confirmation.

First distinguish two different meanings of count:

- **Output image count**: "出 5 张副图" means five separate generated files/slots.
- **Product instance count**: "改成 3pcs" means three sellable product instances inside
  one image. Never translate one count into the other.

Ask one concise confirmation question before calling an image tool when a
product-instance count edit contains any of the following:

- multiple colours, variants, sizes, or SKUs;
- visual references such as 左边/右边/这款/那款/前者/后者;
- relative changes such as 再放一个/多放一个/另加一个/one more/add another;
- a conflict between the stated total and the sum of per-variant quantities.

Treat common Chinese measure words such as 个, 件, 只, 顶, and 台 as product-instance
counts. When the user already provides a consistent total and complete per-variant
allocation, for example `深灰色 1 台、白色 2 台、共 3 台`, the request is unambiguous:
do not ask for confirmation. Copy the total, every variant quantity, and the requested
layout into the image-tool prompt exactly.

This is a helpful ambiguity warning, not a mandatory approval gate. If the user confirms
or corrects the quantities, use those facts. If the user instead says to proceed, submit,
generate directly, or use your current interpretation, respect that instruction and call
the image tool without asking again. Do not loop on the same clarification or treat a
tool-side retry as a reason to ask again.

The confirmation must state each variant quantity, total quantity, layout, and image-text
change. Example:

> 我理解为保留黑色款 1 个，将白色款增加到 2 个，共 3 个横向排列，并把文字改为
> “3pcs”。是否正确？

After the user confirms the interpretation, copy all confirmed facts into the tool prompt
explicitly: `black = 1`,
`white = 2`, `total = 3`, horizontal layout, and the exact text change. Never silently
substitute a different variant. If the user corrects any value, use the correction.

If the user explicitly chooses direct generation without resolving the ambiguity, keep
the original wording, state the single most reasonable interpretation once, and avoid
inventing an exact per-variant allocation that the user did not provide. Present the
result as a preview that needs quantity and variant review.

Do **not** add confirmation to ordinary unambiguous requests such as replacing a
background, changing a scene, adding an external shadow, or editing text without changing
the number of sellable products.

If `analyzeProductImage` fails or returns no analysis, treat that as no visual evidence.
Do not guess product facts from the URL, filename, model memory, or similar products. Ask
for another accessible image or continue only with facts the user explicitly supplied.
Describe the failure conservatively as an upstream rejection or unavailable analysis.
Do not infer that the image violated a content policy, name a provider, diagnose a safety
category, or tell the user how to evade a policy unless the tool returned that exact,
user-actionable explanation.

For every multi-image set, build one **shared product baseline** before writing any slot
prompt. The baseline may contain only user-provided facts and successful image-analysis
facts. Record the SKU/variant, product-instance count, colour allocation, shape and
construction, Logo/text, included accessories, and any exact claims that must remain
constant. Copy the same baseline into every slot prompt; never let each slot infer its own
product facts.

Treat claims as evidence-locked. A qualitative phrase such as "quiet" does not authorize a
numeric claim such as "28 dB". Do not invent dimensions, capacity, performance numbers,
certifications, material grades, percentages, warranties, rankings, or comparison results.
When an exact value is not supplied by the user or successful analysis, omit it or use
non-numeric wording that does not strengthen the claim.

**Platform first.** Detect the platform, then resolve the **country/site and category**.
Supported targets: Amazon, Temu, Noon, Walmart Marketplace, eBay, Etsy, TikTok Shop,
Ozon, Shopee, Mercado Libre. A platform without a market is not publish-ready. The flow
below — modes, product reading, image backend, structured export — is shared. Copy
fields, localization, image story and policy checks are market/category-specific:

- **Amazon** — rules are inlined in this file: STEP 1 copy, STEP 3 AS slots, STEP 3B AD
  modules.
- **Temu / Noon / Walmart / eBay / Etsy / TikTok Shop / Ozon / Shopee / Mercado Libre** —
  read that platform profile in `references/platforms/` before drafting. Do not reuse
  Amazon's bullet count, keyword byte budget, slot ids, or visual style as a marketplace
  rule. For Shopee and Mercado Libre, resolve the destination country/site. For Ozon,
  Walmart, TikTok Shop and other category-driven flows, obtain current category fields.

If the user does not name a marketplace, Amazon can be used as a **drafting default**;
label the assumption and do not infer a market or claim compliance. If country/site is
unknown, use only market-neutral product facts and mark platform limits for live review.
Image craft and the X-Border backend are shared, but each marketplace's main-image,
overlay, AI/mockup, language, and gallery rules take precedence. See
`references/platforms/README.md` for the evidence model.

**Category second.** Detect the product category from the photo, analysis, and
request. When `references/categories/` contains a matching profile, load it and apply
its buyer-concern priority order, carousel patterns, and scene/persona language on top
of the shared craft rules. Category-specific wording anywhere in this skill (fitness
equipment is the worked example) applies only when the product is actually in that
category — never transplant one category's props, scenes, or personas onto another
category's product. With no matching profile, derive category norms from the product
and competitor scan.

Infer the mode from the user request:

- **Full kit**: Generate listing copy, image prompts, a recommended secondary
  image set, and Excel.
- **Image set only**: If the user asks for "副图", "对应副图", "生成产品图",
  "secondary images", "Amazon images", or similar without asking for listing
  copy, generate a recommended secondary-image set, usually **5-7 separate
  production images**. Choose the count by image value, not by filling slots.
  Skip listing copy and Excel unless explicitly requested.
- **Copy only**: If the user says "只生成Listing文案", "不需要图片", "copy only",
  or similar, generate only the listing copy in chat. Skip image prompts, image
  generation, and Excel unless the user explicitly asks to export, save, or
  generate an Excel/table file.
- **One image slot**: If the user asks to regenerate AS-02 through AS-09, generate
  only that slot using the existing product/listing context.
- **Detail page / A+ image set**: If the user says "详情图", "详情页",
  "A+页面", "A+ Content", "EBC", "产品详情长图", or similar, treat it as a
  separate detail-page module set, not Amazon secondary images. Generate AD
  modules rather than AS slots.
- **Full 8-image set**: Generate all AS-02 through AS-09 only when the user says
  "完整8张", "全套8张", "AS-02到AS-09都要", or "full set".
- **Preview batch**: Generate only 1-4 secondary images when the user explicitly
  asks for a preview, a first batch, "先出几张", "先来4张", or names only those
  specific slots.
- **Image audit / 诊断**: If the user provides existing listing images and asks to
  review, diagnose, or improve them ("看看我这套副图有什么问题", "诊断一下我的
  listing图", "老图帮我优化"), audit instead of generating. Check each image against
  the quality gates: buyer-concern coverage, thumbnail hierarchy, AI-poster
  artifacts, claim evidence, text language — and, with the user's consent to the
  analysis cost, drift against the provided main/product photo. Report per-image
  findings, set-level findings, and fixes routed per `references/image-backend.md` →
  "Revision routing". Generate replacements only for slots the user approves.

Map natural-language image type requests to slots:

- 卖点图 / 核心卖点 / benefits: **AS-02**
- 功能图 / 功能拆解 / callouts / feature breakdown: **AS-03**
- 尺寸图 / 尺寸参数 / dimension: **AS-04**
- 场景图 / lifestyle / 使用场景: **AS-05**
- 细节图 / 局部放大图 / 特写 / macro / close-up: **AS-06**
- 对比图 / comparison / 竞品对比: **AS-07**
- 步骤图 / how to use / 安装步骤 / 使用步骤: **AS-08**
- 包装图 / 全家福 / what's in the box: **AS-09**

Do not map "详情图" to AS-06. "详情图" means detail-page/A+ content modules.
AS-06 is only for secondary-image close-ups or local detail magnification.

When a user asks for one type, generate only that mapped slot unless they
explicitly request the full set.

When a user says "副图" without a specific type, create a recommended production
set. Default to 5-7 images:

- Use 5-6 images when the product story is complete and low-value slots such as
  installation, comparison, or packaging would feel forced.
- Use 7 images when one optional proof or process image adds real buyer value.
- Use 8 images only when each slot has a distinct buyer question, or when the
  user explicitly asks for the full set.

Do not silently generate only 3-4 images unless the user asked for a preview or
named only those specific slots.

Common single-image commands users may give:

- "只生成AS-04尺寸图"
- "生成一张场景图，家庭暖色"
- "重新生成AS-07对比图"
- "只要卖点图"
- "把AS-05改成户外场景"
- "生成单张防滑底座细节图"
- "生成详情页6张模块图"
- "只生成AD-03卖点详情模块"
- "参考这张图的感觉重新做AS-04"
- "给你一张竞品副图参考，不要照抄，按我们的产品改"

Examine the uploaded product photo. Extract: product category, materials,
colours, size, brand markings, key design features, and the **current product
state** shown in the image: folded, unfolded, extended, collapsed, open, closed,
assembled, packed, filled, empty, on/off, locked, unlocked, or in-use.

Protect the observed product state. Do not invent a more extreme state just to
make a visual claim stronger. If the product photo already shows a folded or
stored state, do not compress, narrow, shorten, flatten, or create a "more
folded" version. If it shows an unfolded state and no folding mechanism is
visible or provided by the user, do not invent a folded version. Preserve the
product's real proportions, width, height, tube spacing, hinge/lock positions,
and structural relationships.

**Source-image hygiene (shared, all platforms).** Sourcing photos (1688, Taobao,
supplier images) often have baked-in marks that must NOT appear on a marketplace
listing. Inspect the uploaded photo and classify any baked-in text/graphics:

- **Overlay marks — always remove.** Watermarks, shop/marketplace logos (1688 / 淘宝 /
  拼多多 / store 水印), promo badges (促销角标 / 满减 / 包邮), price tags, and Chinese
  marketing overlays are NOT part of the product. Instruct the image model to remove
  them and reconstruct the area cleanly.
- **Text physically on the product / packaging — preserve it accurately.** Do not
  fabricate or silently translate a real label. For packaging or "what's in the box"
  imagery, select a destination-appropriate package and add a reviewed translation only
  where policy and the real product support it.
- **Output image text = selected site's buyer language.** Use the market profile locale
  (for example, Shopee TW → Traditional Chinese, Mercado Libre MLB → Brazilian
  Portuguese, Noon GCC → English/Arabic when requested). Never carry Chinese marketing
  overlays into a non-CN marketplace unless the user requests them.
- **Two-pass when the source is dirty.** If the photo has a heavy watermark or lots of
  baked-in Chinese, first render a cleaned base image (remove watermark/overlay text,
  keep the product on a clean background), then use that cleaned image as the reference
  for the actual slots. See `references/image-backend.md` → "Source-image hygiene".
- **Honest limit:** edit models cannot always fully erase large watermarks or text
  printed on the product. When it can't be cleaned reliably, say so and recommend a
  clean white-background source photo. Do not promise a perfectly clean result.

### Selling-point extraction

Read user-provided selling points verbatim. Identify: core benefit, material
claim, target user, any specs or numbers.

When the user provides no selling points, or only a product photo plus a thin
phrase, build a **selling-point sheet** from five evidence tiers before
planning any image:

1. **User facts** — statements from the user, quoted verbatim. Highest
   authority; never rewrite their meaning.
2. **Manufacturer sources** — model-matched labels, manuals, official product pages,
   and technical documents. Record the exact URL/file and the matching model/SKU.
3. **Observed facts** — attributes returned by a successful
   `analyzeProductImage` call: category, material, colour, construction,
   visible features, accessories, printed text. Cite only what the analysis
   actually returned.
4. **Seller-page claims** — product-page wording from a seller or marketplace listing.
   Capture the source URL, but treat its performance claims as unverified until they
   match the user's exact SKU or manufacturer evidence.
5. **Inferred selling points** — category-level buyer appeals derived from the
   product type. Always label these as AI-inferred. They may drive scene,
   emotion, and composition choices, but must never introduce numbers,
   certifications, or performance claims into visible image text.

Alongside the sheet, list the **unknowns that must not be invented**: exact
dimensions, capacity, wattage, battery life, load ratings, certifications,
warranty terms.

Turn the sheet into a ranked conversion brief before slot selection. For each candidate
selling point record: buyer concern, evidence IDs and strength, practical consequence,
best visual proof, and any claim risk. Rank points by buyer importance, evidence
strength, and whether a clear visual can prove them. Prefer demonstrated construction,
real usage, fit, or package clarity over generic adjectives. Do not elevate an inferred
category appeal into a product fact. If source facts are too thin for a numerical or
performance slide, choose a truthful use/fit/detail slide and state the limits.

Before a multi-image set, give the user one concise chance to confirm or
supplement the sheet ("可补充卖点或纠正我提取的卖点，也可以直接生成"). This is
one soft invitation, not a questionnaire and not an approval gate: if the user
declines or says to proceed, continue with the sheet, keep AI-inferred points
labeled as inferred in the shot plan, and keep them out of on-image numeric
claims. Feed the confirmed sheet into the selling-point classification below.

Before planning images, understand the product and buyer concerns. For any
secondary-image or detail-page image request, read
`references/amazon-image-strategy.md`. If the user asks for Amazon-style images,
competitor direction, or says "看看别人怎么弄", "参考竞品", or "参考Amazon前几名",
also inspect 3-5 current Amazon top-result or user-supplied Amazon competitor
examples when browsing is available, and extract patterns without copying them.
Use non-Amazon examples only as fallback or supplementary category context. If
browsing is unavailable, infer category norms from the product.

If the user provides a reference image, competitor image, or says "参考图",
"参考图片", "照这个风格", "按这个感觉", use it as inspiration, not a template.
Analyze and transfer only the underlying design decisions:

- Core viewpoint/headline logic
- Visual proof type: action, range, before/after, detail inset, comparison, scale
- Composition structure: product placement, foreground/middle/background,
  headline area, support labels, whitespace
- Colour mood and contrast level
- Text density and hierarchy
- Dynamic devices such as arrows, trails, silhouettes, zoom windows, or split
  states
- Character/mascot language: a 3D cartoon host, brand mascot, hand-held product
  reveal, or model-pose device is style DNA — preserve its abstract visual language
  when it fits the request, but never copy the reference's brand, person identity,
  text, or product

Do not copy exact layout, exact wording, icons, brand elements, model pose,
background, colours, or proprietary visual devices. Adapt the reference to the
current product, buyer concern, user-provided specs, and brand/style direction.
When the reference conflicts with product truth or buyer value, prioritize the
current product and explain the adaptation briefly before generation.

Reference images can suggest how to express a benefit, but they must not
override the current product state. Transfer the communication method, such as
home corner placement, floor footprint highlight, folding arrow, or mechanism
zoom, without forcing the current product into a different or exaggerated shape.
For foldable/storage claims, express compactness with environment and proof
devices: wall/corner placement, furniture-scale comparison, floor footprint
highlight, clearance shadow, measuring grid, storage path arrow, or lock/hinge
close-up. Do not show compactness by shrinking or distorting the product body.

Build a buyer-concern map before writing image prompts. Identify what a buyer
would worry about first: fit, stability, capacity, adjustability, use cases,
material strength, comfort, assembly, safety, and home space. Each secondary
image should answer one concern visually.

Classify and merge selling points before assigning image slots. Do not make one
image per raw parameter. Group specs by buyer decision logic:

- **Claim**: buyer-facing promise/result, e.g. load capacity, waterproof,
  long battery life, fast heating.
- **Proof**: structural/material reason that supports the claim, e.g. tube
  thickness, motor wattage, battery capacity, fabric density, certification.
- **Mechanism**: how the product works, e.g. adjustable holes, locking pin,
  foldable hinge, suction base, remote control.
- **Fit/size**: dimensions, height range, capacity, room or body fit.
- **Use case**: what the customer does with it, e.g. pull-ups, storage,
  cooking, cleaning, travel.
- **Comfort/safety detail**: grip, anti-slip pad, rounded edge, cushion,
  insulation, guard rail.
- **Included/installation**: package contents, assembly steps, accessories,
  maintenance.

Merge related points into one image when one explains or proves another:

- Proof + claim: "1.2 mm steel" supports "150 kg load capacity", so they belong
  in one strength/stability image.
- Mechanism + fit: "10-level adjustable" supports "155-210 cm height range",
  so they belong in one adjustment/user-fit image.
- Fit + scene: "82 x 78 cm footprint" supports home-space suitability, so show
  it in one dimension/home-fit image.
- Detail + safety: "anti-slip suction base" supports stability under training,
  so show it with base contact and anti-wobble proof.
- Use cases together: related exercises belong in one multi-function image
  unless one exercise is the primary lifestyle hero. Multi-use images must plan
  each body pose around a real contact point on the product before generation:
  hands on the pull-up bar, hands on dip handles, feet/hands near base support,
  or body hanging from the correct bar. If the actions cannot all fit cleanly
  around one product, use separated vignettes, split panels, or ghosted
  same-person motion states instead of crowding multiple full people onto one
  distorted product.

If a spec is only a proof point, avoid making it the headline alone. Use it as a
badge, callout, close-up, or secondary label under the buyer-facing claim.

Design images by buyer journey and visual event, not by rigid slot templates.
AS slot ids are output labels; they must not force weak or repetitive images.
For every proposed image, answer these checks before generating:

- **What is the one-sentence core viewpoint?** Write it first as the image's
  big headline claim. If it cannot be expressed as one clear buyer-facing
  sentence or phrase, the image is not ready.
- **What changes in the buyer's mind after this image?** If the answer is
  unclear, merge it into another image or skip it.
- **What is moving, changing, comparing, or being proven visually?** Static
  product + badges is not enough for a production asset unless the product
  itself is the proof.
- **Which point is unique to this image?** Do not repeat the same base, grip,
  steel, or training claim across multiple images unless each use is serving a
  different buyer question.
- **What is the visual hook before text?** A viewer should understand the core
  idea from action, arrows, ghosted positions, contrast, close-up context, or
  scale before reading labels.

Every production secondary image needs a clear communication hierarchy. A
headline is a design choice, not a required decoration:

1. **Core selling point / viewpoint**: one buyer-facing claim. It should answer
   "why should I care?" not merely name the slot. This can be expressed through
   a headline, a large spec, a dimension line, a before/after split, a product
   detail, or a clear action scene.
2. **Visual proof**: product in action, range, comparison, mechanism, scale, or
   environment that proves the claim.
3. **Support labels**: 0-3 short badges/callouts with exact specs or proof.
   Use no support labels when the photo or detail already proves the point.

Before writing any image prompt, make a **layout decision**, the way a human
designer would:

- Text role: no headline / small caption / large headline / large spec number /
  callout-only. Do not force a headline on lifestyle, macro, or clean dimension
  images when the visual proof is stronger without it.
- Text placement: choose a reserved text zone such as top-left, side band, lower
  strip, open wall area, or no text zone. Do not place text over the user's body,
  product contact points, adjustment holes, handles, feet, or key details.
- Typography treatment: define font weight, relative size, line breaks, and
  hierarchy. Use colour only to separate meaning, such as a key number, material,
  or action word; avoid styling every word equally.
- Text background: decide whether text needs a subtle translucent panel,
  solid block, white space, or no background. Use a background only to improve
  readability, not as decoration.
- Visual text system: choose a varied treatment across the set. Do not make
  three or more images in a row use the same black-text-on-white small labels.
  Mix appropriate treatments such as large two-tone headline, small caption,
  side ribbon, colour band, circular detail label, dimension label, icon + text,
  or text-free lifestyle scene.
- Product/person relationship: decide whether the product is unobstructed hero,
  action partner, background context, or macro source. People must support the
  selling point and must not hide structural proof.
- Detail expression: decide whether the detail should be a real close-up,
  connected inset, crop, cutaway, or callout point. Details must point to real
  visible parts and answer a buyer concern.
- Dynamic expression: choose the physical effect to show: correct user contact,
  base pressure, adjustment range, footprint, comparison state, hand scale,
  opened/closed state, pour/flow, load, texture, or usage sequence. Avoid adding
  motion devices that do not prove the selling point.

Amazon secondary-image headline style:

- Prefer concrete feature-benefit noun phrases over generic advertising
  sentences. The headline should sound like Amazon carousel copy, not a brand
  poster slogan.
- Large headlines are allowed when the slot needs a strong claim. Make them feel
  human-designed: reserve a clean title zone, use deliberate line breaks, italic
  or condensed bold type when suitable, and use a flexible colour hierarchy:
  one product/brand/category accent colour plus one neutral text colour. Add a
  smaller subheadline only when it clarifies fit, compatibility, or proof. A large
  headline should never sit randomly over the product or cover the selling detail.
- Use product-specific words, mechanism words, or exact specs when known:
  "4-in-1 Training Station", "Adjustable Height Range", "Wide Anti-Slip Base",
  "Compact Home Gym Footprint", "Reinforced Steel Frame".
- Avoid generic lifestyle slogans such as "Train More At Home", "Fits Your Home
  Space", "Upgrade Your Workout", "Built For Your Life", or "Home Fitness Made
  Easy" unless paired with a specific proof point.
- For dimension images, use utility-style headlines such as "Home Gym Fit
  Guide", "Check Your Workout Space", or "Compact Footprint" instead of vague
  fit claims.
- For lifestyle images, use the action or product role as the headline, e.g.
  "Pull-Up Training Station" or "Dip Station For Home", not motivational copy.

Headline examples by category logic:

- Instead of "Details": "Built To Stay Stable"
- Instead of "Dimensions": "Fits Your Home Gym"
- Instead of "Adjustable Height": "Adjusts For Every User"
- Instead of "Waterproof": "Keeps Gear Dry In Rain"
- Instead of "Large Capacity": "Stores More In Less Space"
- Instead of "Fast Heating": "Ready To Cook In Minutes"

Do not generate an image whose big headline, visual proof, and support labels
are not aligned. If the headline says stability, the image must show stability,
not only a product render with a stability badge.

Use dynamic expression for static generated images:

- Show process with ghosted positions, motion arrows, step overlays, before/after
  splits, height-range trails, action silhouettes, or inset magnifiers connected
  to the full product.
- For adjustable products, show the range as movement: low-to-high ghosted bars,
  sliding arrows, user-height silhouettes, and the lock/adjust mechanism.
- For dimension images, combine exact dimensions with room fit or adjustable
  range, not only front-view measurement arrows.
- For foldable or compact-storage products, first determine whether the uploaded
  product is already folded or unfolded. If it is already folded, keep that
  exact state and show compact storage through wall/corner placement, floor
  footprint overlay, room-scale context, or mechanism inset. If both states are
  needed but only one is visible, use a subtle ghosted outline only when it can
  be inferred from the real mechanism; label inferred states as visual
  explanation, not exact product shape.
- For strength/stability, show the claim being visually tested or explained:
  user action, base contact, reinforced structure, load badge, and proof detail
  in one composition.

If the image idea feels monotone, enrich it before generating. Do not add random
decoration; add useful layers that strengthen the same core viewpoint:

- **Fuse related information**: combine claim + proof + mechanism instead of
  putting each in isolated badges.
- **Create depth**: use foreground detail, main product/action in the middle,
  and scene/context or soft graphic shapes in the background.
- **Add contrast**: before/after, low/high, stable/unstable, empty/filled,
  ordinary/enhanced, indoor/space fit.
- **Connect details to the whole**: use magnifier insets, callout lines, cutaway
  highlights, or zoom windows tied to the full product.
- **Use scale and human context**: hand, body silhouette, room footprint, common
  object comparison, or product-in-use posture.
- **Vary layout across the set**: avoid producing multiple centered product
  images with badges. Mix hero action, technical range, proof-under-use, room
  fit, comparison, and mechanism explanation.

Layering check before generation:

- Foreground: what grabs attention first?
- Middle ground: where is the product or action proof?
- Background: what context supports the claim without clutter?
- Text/annotation hierarchy: no text, small caption, headline, large spec,
  dimension labels, or callouts only, whichever best expresses the selling point.

Detail/close-up images are optional. Generate AS-06 only when the details add
new buying confidence that is not already proven in other images. If the same
detail is already used in a feature, stability, or material-proof image, skip
AS-06 or integrate the detail as an inset there. Avoid generic 2x2 macro grids
when the product details do not create a stronger selling story.

For image requests, translate the buyer-concern map into a shot plan before
generation:

- Slot id and image type
- Core selling point / viewpoint
- Buyer question being answered
- Main visual proof, not just text
- Dynamic device: action, arrow, ghosted state, before/after, scale, or inset
- Layout decision: text role, text placement, typography hierarchy, text
  background, product/person relationship, detail expression, and dynamic proof
- Layering plan: foreground, middle ground, background, communication hierarchy
- Scene/background and visual intensity
- Exact short text labels to place on the image
- Negative constraints: what must not appear

Add one explicit reason each slot earns space in the gallery and what distinct buyer
question it answers. Give the primary image the cleanest compliant presentation. Let
secondary images use purposeful color, realistic context, perspective, small evidence-
backed callouts, visualized mechanisms, or human scale when that helps explain the
product and the marketplace permits it. “No text” is a per-slot design decision, not a
default for the entire set; vary layouts so the gallery does not become repeated plain
renders or identical badge cards.

The finished shot plan is the highest-priority source for prompt writing. Do not
re-plan slots, change layout decisions, or rewrite the plan's exact on-image text
lines while writing prompts; when generation reveals a needed change, update the plan
first, then regenerate only the affected prompt.

Use creative auto-completion for image planning. If the user provides only a
product photo, product type, and basic selling points, infer an appropriate
Amazon secondary-image composition, visual hierarchy, background, lighting,
icons, short callout copy, and scene context. Prefer clean commercial layouts
that make the product and benefit legible at thumbnail size.

Default to **credible commercial Amazon visuals**, not plain catalog layouts or
AI-poster layouts:

- Use high contrast between product and background, warm directional lighting,
  clear shadows, depth, large product scale, and confident but restrained
  typography.
- Use lifestyle action, dramatic close-ups, dimension arrows, or comparison
  devices to prove the benefit visually.
- Avoid flat grey backgrounds for every image; reserve them for technical slots
  only, and add accent colour, depth, or context when the user asks for a style
  such as "家庭风格" or "暖色".
- Keep text minimal, but make the few words large and high-impact.
- For real-home styles, the image should feel like a high-quality product photo
  with light commercial layout added afterwards, not a CGI fitness poster.

User-specified art direction overrides auto-completion. Preserve explicit
requests for style, scene, colour palette, language, target user, background,
layout, angle, size labels, and text placement. If the user says "家庭风格",
"厨房场景", "黑金风", "不要文字", "只要英文", "中文文案", "中英双语",
or similar, incorporate that constraint into the relevant prompt instead of
using the default style.

When the user asks for "家庭暖色", "家庭风格", "暖色家居", "home warm style",
or similar, use the **Warm Real Home Ecommerce** preset unless they explicitly
request a poster, neon, gaming, cyber, or black-gold style:

- Scene: realistic lived-in home fitness corner, warm wood floor, cream or warm
  neutral wall, natural window light, soft shadows, simple mat, plant, shelf, or
  sofa edge only when it helps scale and realism.
- Lighting: warm daylight or late-afternoon natural light with believable
  shadows. Avoid fake glow, neon rim light, gold light trails, lens flare, and
  fantasy energy effects.
- Dynamic visual proof: use real physical events such as a correct exercise
  action, hand contact, base pressure, floor footprint, perspective dimension
  lines, range ghosting for product parts only, foreground macro, or before/after
  room composition.
- Typography: choose text only after the layout is clear. Some warm home images
  should have no headline or only a small caption; others can use a large
  confident Amazon headline when the claim needs it. If a large headline is used,
  reserve a clean title zone, use clear line breaks, and use 1-2 colours for
  hierarchy. Choose the accent colour from the product, brand, category norm,
  scene, or user reference image; do not default to orange/black unless that fits
  the product or provided direction. Use concrete Amazon-style feature-benefit
  phrases instead of generic lifestyle slogans.
- Labels: vary the label system based on image role: thin callout lines, compact
  spec chips, coloured side bands, circular detail labels, icon + text stacks, or
  subtle text panels. Avoid repeating black text on white tags across the set,
  and avoid black-gold pill buttons, glowing outlines, decorative icon stacks, or
  UI panels that make the image look like a template.
- People: use realistic fitness models only where the buyer needs action proof.
  Avoid bodybuilder-poster poses, plastic skin, duplicated ghost athletes, and
  poses that cover the product or distort the frame.

Add this negative constraint to every Warm Real Home Ecommerce prompt:
"Avoid AI poster aesthetics: no neon glow, no energy rings, no fantasy light
trails, no black-and-gold button badges, no random oversized motivational
typography that lacks a reserved title area, no CGI showroom, no plastic-smooth
skin, no duplicated ghost athletes, no product-obscuring bodies. Keep the image
grounded in realistic warm home photography with purposeful Amazon ecommerce
annotations."

Visible image text language rules:

- Default to English for Amazon US or when the user says "Amazon.com", "US",
  "美国站", or "只要英文".
- Use Chinese visible text when the user says "中文文案", "图片文字用中文",
  "中文副图", "中文标注", "国内平台", or similar.
- Use bilingual Chinese-English text only when the user explicitly asks for
  "中英双语" or "双语". Keep bilingual text sparse because it increases visual
  density.
- If the marketplace is unclear, infer from the user's requested language and
  product context. State the language assumption before generation when it may
  affect the output.
- Keep specs exact in any language. Translate meaning, not unit values. Do not
  invent claims while translating.

Infer missing creative presentation choices such as scene, composition, lighting, and
layout, and state material assumptions clearly. Never infer missing product facts,
numeric specs, certifications, or performance claims. Do not ask questions first unless
the request is impossible without a product category or an evidence-locked product fact.

Resolve bundled resources relative to this skill folder. Do not assume the
current shell directory is the skill folder.

Execution flow:

- Copy only: run STEP 1 and STEP 2, then stop.
- Image set only or one image slot: skip STEP 1 and STEP 2 unless the user also
  asks for listing copy; run STEP 3 directly.
- Detail page / A+ image set: skip AS secondary-image slot planning unless the
  user also asks for副图; run STEP 3B.
- Image audit: deliver per-image and set-level findings with routed fixes; do not
  generate. Regenerate only user-approved slots via STEP 3.
- Full kit: run STEP 1 through STEP 5.

---

## STEP 1 — Generate Listing copy

Before drafting, read the selected profile in `references/platforms/` and its market
entry in `platform-rules.json`. Use that market's buyer locale and category fields. If a
required field is dynamic, import the current category template; do not invent a
marketplace-specific field list. Keep common product facts separate from
`listing.platform_fields` so content can be adapted without carrying one market's limits
into another.

For Shopee's initial rollout, apply `shared_image_baseline` across supported markets and
localize copy and visible text to the selected market. Treat those image values as
configurable project defaults, not platform-enforced limits; preserve them unless a
verified country/category override is recorded. Keep Shopee Singapore's official
image recommendations scoped to Singapore.

Every factual line in title/highlights/description/attributes/claims must trace to the
manifest's `fact_ids`. Unsupported claims are omitted or labeled unverified. Warranties,
guarantees, certifications, comparison results, safety and performance claims are only
included when the user supplied the applicable evidence/terms. Do not add a generic
guarantee close as persuasive filler.

The Amazon rules below apply to Amazon US drafting only. They are not a template for
other marketplaces.

**Title rules:**
- `[Brand] [Core Keyword] [Key Attribute] – [Differentiator], [Context]`
- Amazon US snapshot: maximum 200 characters including spaces. Current category/title
  validation still wins. Source: [Amazon title requirements](https://sellercentral.amazon.com/seller-forums/discussions/t/533f9cf7-3b5e-4974-b523-02e4a1a42c5f).
- Use natural buyer language and the key identifying details. Avoid misleading promotions
  and keyword stuffing. Amazon guidance also limits most words to two uses (excluding
  common articles/prepositions/conjunctions) and restricts characters such as
  `! $ ? _ { } ^ ¬ ¦`; brand-name exceptions need manual review.

**Highlights — common Amazon 5-bullet drafting pattern (not a universal format):**
`【ALL-CAPS LABEL】Benefit statement. Feature/spec support. Context or proof.`
- Keep each focused and supported by a product fact. 150–200 characters is not a
  compliance claim; check the current item-type field limit. Suggested coverage:
  - B1: capableOf + causes (function + problem solved)
  - B2: hasProperty + distinguishedFrom (material/spec + vs competitors)
  - B3: suitableFor + usedInContext (who + where)
  - B4: motivatedBy + distinguishedFrom (why buy + differentiation)
  - B5: partOf + relatedTo (what is included + relevant use/care facts)

**Description — recommended structure, not a fixed marketplace limit:**
1. Pain-point hook (emotional, 2-3 sentences)
2. Product as solution (introduce product + core benefit)
3. Feature deep-dive (expand bullets, add secondary keywords naturally)
4. Use-case expansion (3-4 distinct usage scenarios)
5. Factual close: care, compatibility, support or warranty only if provided

**Backend Search Terms:**
- Space-separated ONLY. No commas, quotes, repeated words.
- Amazon US snapshot: keep below 250 UTF-8 bytes; avoid brand/product identifiers,
  repeats, promotions and subjective language. Use relevant synonyms, abbreviations and
  alternate names; Amazon says common misspellings are not needed. Source: [Amazon search terms](https://sellercentral.amazon.com/seller-forums/discussions/t/93c61d8c-5c4d-43bf-9b5a-6b3e48213aa2).
- Store this as `listing.platform_fields.backend_search_terms`; it is not a universal SEO
  field for other marketplaces.

---

## STEP 2 — Display listing

Output in a copyable format using the target marketplace's actual field names. Always
show platform, country/site, locale, category and whether the current category schema was
checked. Use the platform profile's field names and keep unresolved Seller Center fields
in a separate "needs live schema" section. Do not format every site as Amazon bullets or
keyword fields.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛒  AMAZON LISTING  ·  [Product Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌  TITLE  ([X] chars)
[title]

📋  BULLET POINTS
①  [bullet 1]
②  [bullet 2]
③  [bullet 3]
④  [bullet 4]
⑤  [bullet 5]

📝  DESCRIPTION
[full description]

🔑  BACKEND SEARCH TERMS  ([X] bytes)
[space-separated terms]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If in full-kit mode, continue to the image prompt plan. If in copy-only mode,
stop after displaying the listing unless the user explicitly requested export.

---

## STEP 3 — Build image prompts and optionally generate images

Build prompt text for the selected AS slots before generating images. For full
8-image requests, build AS-02 through AS-09. For recommended image sets, build
only the 5-7 slots that answer real buyer questions. Include this product
consistency rule in every prompt:
> "Use the uploaded white-background product photo as exact visual reference.
> Product shape, colour, proportions, and design details must match precisely.
> Do NOT reproduce any watermark, overlay/promo text, shop or marketplace logo, price
> tag, or Chinese marketing graphics from the source image — remove them and keep only
> the real product. All visible text in the output is [marketplace language]."

For a multi-image set, prepend the same shared baseline to every slot prompt:

```text
SHARED PRODUCT BASELINE — identical across this set
- Verified facts: [only user-provided or successfully analyzed facts]
- Product count and variant allocation: [exact values when verified; otherwise preserve
  exactly what is visible in the reference image]
- Locked attributes: SKU identity, shape, construction, colours, Logo/product text,
  accessories, and all unedited product details
- Claims allowed on-image: [exact evidence-backed claims only]
- Forbidden: adding/removing/duplicating products, swapping variants, inventing numeric
  specs or certifications, or changing locked attributes
```

If the count or variant allocation is not verified, use `preserve exactly what is visible
in the reference image; do not add, remove, or duplicate any product instance`. Do not
replace that clause with a guessed number.

The "match precisely" instruction covers the **product** (shape/colour/proportions/
design/material) only — it must not be read as an instruction to preserve source
watermarks, overlay text, marketplace tags, or Chinese promo graphics. See STEP 0
"Source-image hygiene".

Do not default to a text-heavy collage. For production assets, generate separate
secondary images unless the user explicitly asks for a storyboard or direction
board. Each image should have one main message, large product/action visuals,
and short callouts instead of paragraphs. Keep visible text minimal: headline +
2-4 short labels or badges.

Count discipline:

- Full 8-image requests generate exactly **8 separate images**: AS-02, AS-03,
  AS-04, AS-05, AS-06, AS-07, AS-08, and AS-09.
- Broad secondary-image requests generate the strongest recommended set, usually
  5-7 images. Do not fill weak slots just to reach 8.
- Do not combine the full set into a single collage unless the user asks for a
  direction board.
- If generating fewer than 8 for a broad image-set request, briefly state the
  selected slots and why omitted slots were skipped before generation.
- If only 3-4 images are generated because of a preview request, state that it
  is a preview before generation.
- When using an image-generation tool that returns one image per call, call it
  once per required slot.
- Use the same reference image and the same shared product baseline for every slot. A
  scene change does not authorize a quantity, colour, SKU, Logo, or construction change.

For each prompt, add any inferred or user-specified style guidance. If the user
does not specify style, choose a suitable ecommerce style automatically:
technical and clean for dimension/function diagrams, warm realistic interiors
for lifestyle scenes, crisp macro lighting for detail grids, and simple
high-contrast tables for comparisons.

Visual intensity requirement:

- Every image must be thumbnail-legible: product/action occupies the visual
  center, headline is short, and labels are readable.
- Use stronger composition than a plain white/grey product render: foreground
  scale, real action, perspective depth, before/after contrast, clean dimension
  lines, inset magnifiers, or human action where appropriate.
- "Dynamic" means a visible buyer-relevant event is happening: a user is gripping
  the correct bar, the base is shown under pressure, the height range is shown
  with a product-part trail, the footprint is anchored to the floor, or a detail
  is connected to the full product. It does not mean decorative glow, energy
  rings, fantasy motion trails, or oversized poster typography.
- For "家庭风格" use a warm real home-gym/living-room fitness environment with
  wood floor, warm wall colour, natural light, and clean lifestyle props, while
  keeping the product as the hero. For "家庭暖色", apply the Warm Real Home
  Ecommerce preset above.
- For fitness equipment, include people only in scene/use images or small action
  silhouettes; keep technical images product-led.
- For fitness multi-action images, protect product geometry first. The product
  must stay as one rigid object with straight uprights, correct bars, correct
  handle locations, and stable base proportions. Do not let bodies bend, stretch,
  duplicate, or move product parts. If showing several exercises, prefer a
  workout-flow band, numbered vignettes, or separate action zones. Each pose must
  visibly grip, press, hang from, or align with the correct product part.
- Do not let technical images become static. Use arrows, range trails,
  magnified mechanisms, pressure/contact cues, or comparison states to make the
  benefit feel active and understandable.

### Rendering: call the X-Border image backend

The `$imagegen [brief]` blocks below are backend-agnostic creative briefs. To actually
render them, call the **X-Border image MCP tools** — the current contract and exact
parameters are in `references/image-backend.md`. The skill
never holds any image key; X-Border's server does.

Before rendering, check `disallowed_listing_source_types` in the selected market's
profile. If the requested rendering would produce a prohibited source type, do not
deliver it as a final listing asset. For example, TikTok Shop US disallows digital
renderings and requires actual product photography: use the skill to analyze facts,
rank buyer concerns, write the photo shot list and listing copy, then ask for or guide
capture of the real angles. A generated concept/reference image may be supplied only as
a clearly labeled non-uploadable preview when the user asks for one. Never relabel a
generated file as a photograph to pass validation.

Pick the tool by intent (details in `image-backend.md`):

- **Per-slot art direction (default):** render each selected slot with `generateImage`
  — `prompt` = the slot's `$imagegen` brief (drop the leading `$imagegen`),
  `referenceImageUrl` = the product photo URL, optional `model`
  (`nano-banana-pro` default / `seedream-4.5` / `qwen-edit-multiangle`). One call per
  slot. This preserves the detailed per-slot prompts that are this skill's whole point.
- **Image/full set:** select the valuable platform slots, state the output-image count,
  then call `generateImage` once per slot. The current MCP has no batch preset tool.
- **No product photo / pure text-to-image:** use `generateImageFromText` when there is
  **no** reference product photo, or for a scene / background / concept image from text
  alone — its reference is **optional** (default `seedream-4.5`). `generateImage`'s
  reference is required; this is the no-reference path.
- **Structured analysis first (识图):** For a multi-image set, call
  `analyzeProductImage` once and wait for it to finish before any billable generation when
  product facts are not already explicit. Use the result to build the shared baseline,
  then reuse that baseline in every slot. Do not run analysis and generation in parallel.
  For a single image, analysis remains optional unless the task needs facts not provided
  by the user.

**Input combinations (all supported):**

- **商品图 only (default):** every slot renders via `generateImage` with the product
  photo as `referenceImageUrl`.
- **商品图 + 参考图 (style/competitor reference):** the product photo keeps the
  `referenceImageUrl` identity-anchor slot; the reference image enters generation as
  extracted style DNA written into the prompt — palette, composition skeleton, proof
  device, character language. When the user explicitly demands close style adherence
  ("必须很贴这张的风格", "照这个感觉一比一"), switch that slot to
  `generateImageFromText` with `referenceImageUrls = [product photo, style reference]`
  — product photo first — and state in the prompt which URL is the product identity
  anchor and which contributes style only. This dual-reference path has a weaker
  identity lock, so its output must pass the output drift audit before any consistency
  claim.
- **参考图 only, no product photo:** `generateImageFromText` with the reference in
  `referenceImageUrls`. The output is a style/concept direction board, not a listing
  asset: it must not present the reference's product or brand as the user's, and the
  response must say a product photo is required before production slots can be made.
- **多角度商品图 (2-4 photos):** feed all of them to `analyzeProductImage` for the
  shared baseline; for each slot pick the single photo whose angle best serves that
  slot as `referenceImageUrl` and note the choice. A back-panel feature slot uses the
  back-view photo, not the front hero shot.

If required set analysis fails or returns no usable facts, do not silently continue with
independent slot guesses. Explain that no visual evidence is available and ask for another
accessible image or permission to generate previews using only the user's explicit facts.
If the user explicitly chooses to proceed, use the reference-preservation clause above,
omit every unsupported claim, and mark all results for manual product-consistency review.

For a failed `generateImage` call, retry that slot at most once and only when the tool
returned no image or usable output. Never regenerate a successful slot automatically. If
the retry also fails, report the failed slot and let the user decide whether to spend
another generation attempt.

**Sample-first staged generation (sets of 5+).** For a multi-image set of five or more
slots, generate the 2 highest-value slots first and run the output drift audit below on
them before rendering the rest. If the audit passes, continue to the remaining slots in
the same run and present the complete set together — do not pause for approval. If the
audit fails, apply the smallest-layer fix, re-audit, and stop to report before spending
credits on the remaining slots only when the failure survives the bounded fix. The
sample stage is part of one full-set run, not a preview batch. If the user explicitly
asks to see samples first, pause after the audited sample; if the user says 直接出完 /
一次出完, skip the staging entirely.

**Output drift audit (product consistency).** The reference-match clause in the prompt
is an input-side request, not a guarantee. To actually verify that a generated image
matches the provided product photo, call `analyzeProductImage` on the generated image
URLs (up to 4 per call; each call bills one analysis credit), set `focus` to a
baseline-comparison instruction, and compare the returned attributes against the shared
product baseline:

- shape, construction, and proportions
- colour and surface finish
- Logo and printed product text
- component placement: handles, buttons, ports, panels, feet
- accessory set and packaging contents
- product-instance count and variant allocation

Run this audit by default for (a) any multi-image set and (b) any product-instance
quantity or variant edit — the two highest-drift-risk cases. Elsewhere run it when the
user asks for guaranteed consistency. State the audit's credit cost the first time it
applies in a task; skip the audit only when the user explicitly declines that cost, and
then keep the pending-review-preview language for the results.

When the audit finds drift, route the fix to the smallest responsible layer instead of
regenerating the set (see `references/image-backend.md` → "Revision routing"): name the
exact drifted attribute in a strengthened reference clause — for example "keep the
control panel on the right side exactly as in the reference; do not mirror the product"
— and regenerate only the affected slot, at most once. If drift survives the bounded
regeneration, report the slot with the audited difference and let the user decide. Only
a passing audit authorizes the completion message to state that product consistency was
checked.

Uploaded product photos arrive as URLs (`<image url="...">`) — pass them straight to
`referenceImageUrl` / `imageUrls`, never base64. The `$imagegen` AS-slot briefs below are
Amazon's. Other platforms use the story beats in their profile; any slot ids we assign
are internal labels, not official platform fields. Follow that market's image restrictions
and rendering path.

Call the backend when the user requested the full kit, image set only, or a specific
image slot. **If the `x-border` MCP tools are unavailable**, fall back: output the
prompt text and still write it into the Excel file when Excel output was requested.
Never claim an image was generated when no tool was called.

After rendering, report only facts present in tool results. Do not claim that count,
variant, Logo, structure, text, or styling passed inspection merely because the prompt
requested it. Without a successful output-image analysis, say that each result is a
pending-review preview and provide the shared baseline as the comparison checklist. Do
not fabricate image-specific observations from URLs or prompt text. The output drift
audit above is the only supported way to turn a pending-review preview into a verified
result.

**AS-02 — 核心卖点图 (Key Benefits)**
```
$imagegen [product matching reference photo] as the dominant visual.
This is the conversion hook, not a summary of all specs. Choose the strongest
buyer-facing promise and make it visually obvious through action, scale,
before/after, or multi-use composition. Use one bold headline and only 2-3
supporting badges. Avoid generic lines like "stable home training" unless the
visual clearly proves stability. Strong Amazon hero composition: large product,
warm commercial background, high contrast, confident but restrained headline,
shadow and depth. For Warm Real Home Ecommerce, use a real home fitness corner,
one believable action moment, and light ecommerce annotations. Avoid motivational
poster composition, giant stacked typography, glow rings, motion-trail athletes,
black-gold button badges, and bodies that hide the product. Headline should be
a concrete product-role or feature-benefit phrase, such as "4-in-1 Training
Station", "Pull-Up & Dip Station", or "Full-Body Home Workouts"; avoid generic
slogans such as "Train More At Home".
Product must exactly match the uploaded reference photo.
```

**AS-03 — 功能拆解图 (Feature Breakdown)**
```
$imagegen [product matching reference photo] centred, 3/4 angle.
Thin callout lines with circle dots pointing to only the 4-6 most important
physical features from the buyer-concern map. Labels are 2-4 words each.
Warm technical ecommerce style with either a restrained beige/light grey
background or a realistic warm home background when requested. Make a deliberate
designer layout: either a large two-tone feature headline in a reserved title
zone, or a smaller title plus coloured side-band labels. Do not default to all
black text on white tags. Use varied Amazon-style callouts such as accent-colour
side ribbons, circular detail markers, thin lines, and connected inset
magnifiers for important details. Lines balanced. Avoid a flat low-energy
diagram, but also avoid glowing arcs, neon outlines, black-gold UI buttons,
heavy decorative icon stacks, and random poster typography.
Product must exactly match the uploaded reference photo.
```

**AS-04 — 尺寸参数图 (Dimensions)**
```
$imagegen [product matching reference photo] front/side or 3/4 view.
Engineering double-arrow dimension lines for [key dimensions]. If height is
adjustable, show it dynamically with ghosted low/high positions, vertical range
trail, upward arrow, and/or user-height silhouettes.
Use exact user-provided dimensions when available. If dimensions are missing,
infer only approximate visual proportions and label every inferred size as approx.;
never present estimated dimensions as exact product specifications.
Use a small spec badge or mini table with only the dimensions and 1-2 specs
needed for space planning.
Default to white or light grey technical background unless the user requests a
scene style such as home, kitchen, bathroom, garage, or outdoor. Monospace
numbers. Dual units cm and inch. Add subtle room-scale context when helpful so
buyers understand home fit.
For Warm Real Home Ecommerce, anchor measurements to a believable room floor:
use a non-glowing footprint rectangle, perspective dimension lines, a realistic
scale silhouette, and restrained labels. Avoid luminous floor grids, neon arrows,
oversized labels, and fake exact numbers. Headline should be utility-style and
specific, such as "Home Gym Fit Guide", "Check Your Workout Space", or "Compact
Footprint"; avoid vague slogans such as "Fits Your Home Space".
Product must exactly match the uploaded reference photo.
```

**AS-05 — 场景使用图 (Lifestyle)**
```
$imagegen [target user from selling points] using [product matching
reference photo] in [natural setting appropriate for this product type].
Warm natural lighting, stronger commercial contrast, authentic action pose,
slight depth of field. Real environment, not a studio. Show the exercise action
first and the product fully visible/stable; then optionally add 1-2 small
benefit labels. Product colour/shape matches reference.
For Warm Real Home Ecommerce, make the scene look like realistic home fitness
photography: warm daylight, wood floor, lived-in but tidy room, restrained text,
and no fantasy glow, energy rings, duplicated action trails, or motivational
poster wall text.
Use one primary athlete action only unless the user explicitly asks for multiple
actions. The athlete must physically connect to the correct product contact
points: hands gripping the actual pull-up bar or dip handles, feet clear of
base bars unless the exercise requires contact, no limbs passing through the
frame. Keep the product rigid and undistorted.
```

**AS-06 — 细节特写图 (Detail Macro 2x2)**
```
$imagegen close-up detail image only if the details communicate new buying
confidence not already covered elsewhere. Prefer one integrated composition:
full product context plus 2-4 connected magnifier insets, or a dynamic detail
story such as base contact under pressure, adjustment hole/lock mechanism, grip
texture in use, or reinforced tube connection. Use 2x2 macro grid only when all
four panels are meaningful and distinct. Each label is 2-4 words. Details match
reference photo. For Warm Real Home Ecommerce, use real macro photography cues:
natural warm light, floor contact, visible texture, enlarged real part crops,
soft circular or rounded zoom windows, and labels integrated into the crop.
Detail images should feel comfortable and product-real: large macro part, clear
connection to the full product, soft warm or white background, and 1-3 label
styles that match the detail. Avoid making every label a black-on-white tag.
Avoid generic parts, repeated proof points, decorative macro panels, glowing
pressure rings, neon outlines, and black-gold label boxes.
```

**AS-07 — 竞品对比图 (Comparison)**
```
$imagegen Clean comparison table infographic.
Title: "WHY CHOOSE [product type]?"
Left "OUR PRODUCT" highlighted background, right "OTHERS" grey.
3-5 rows comparing only buyer-relevant differences from the concern map.
Left column ✓ checkmarks. Right column ✗. No competitor brand names.
Bold sans-serif. High-contrast Amazon infographic style with a product hero or
detail crop, not a plain spreadsheet.
```

**AS-08 — 使用步骤图 (How to Use)**
```
$imagegen Step-by-step diagram. 4 panels horizontal connected by arrows.
Large step numbers 1-2-3-4 with short captions (4-6 words each):
[logical usage steps for this product type].
Each panel shows product at that stage. Clean warm infographic with strong
visual hierarchy, not small low-contrast thumbnails. Product matches reference
photo.
For multi-function training, this slot may become a "training modes" module
instead of literal usage steps. Use separated panels or clearly spaced action
vignettes so each exercise has its own product copy or its own action zone.
Do not stack several full athletes on one central product if that causes
misalignment. Label each action only after verifying the pose uses the correct
bar/handle/base point.
For Warm Real Home Ecommerce, keep panels photographic and restrained: warm home
background, consistent product geometry, simple separators, small labels, and
realistic poses. Avoid comic-book panels, glowing arrows, ghost athletes,
oversized step numbers, and black-gold UI styling.
```

**AS-09 — 包装全家福 (What's in the Box)**
```
$imagegen Flat-lay overhead on pure white background.
All items laid out: [product from reference], [accessories from selling points
or standard for product type], [packaging if applicable].
Each item has a label line. "WHAT'S IN THE BOX" bold title at top.
Overhead studio lighting. Symmetric organized layout.
Product matches reference photo.
```

---

## STEP 3B — Build detail-page / A+ image modules

Use this section only when the user asks for "详情图", "详情页", "A+页面",
"A+ Content", "EBC", or product-detail long images.

Detail-page images are separate from Amazon secondary images:

- **AS slots**: carousel/listing secondary images near the main image.
- **AD modules**: detail-page/A+ modules lower on the product page.

Default to 5-7 AD modules. Do not force a module if it repeats the carousel.
Use wider, more editorial compositions than AS images. Text can be slightly
more explanatory than carousel images, but still avoid paragraph-heavy layouts.
Each module should have one section message and one clear visual proof.

Anchor the module set to **claim seeds**. AD-01 must establish 2-4 claim seeds
chosen from the highest-evidence entries in the STEP 0 selling-point sheet —
user facts first, then observed facts; AI-inferred appeals may seed only
scene/emotion modules and never numeric claims. Every later module names the
seed it expands, proves, compares, or contextualizes. If a module's message
cannot be traced back to an AD-01 seed, revise the seed set or the module
before generating; do not let mid-page modules introduce unrelated new selling
points.

Give each module a distinct copy role and sentence structure. Assign roles such
as identity, desire, proof, texture/material, scene, trust/detail, and closing
before writing copy. Adjacent modules must not share the same sentence rhythm;
if three or more modules read as "headline + one explanatory sentence + a row
of tags", rewrite at least two into a different structure: annotation map,
question-and-answer, numbered mini-steps, scene captions, comparison rows,
trust checklist, or a quiet text-free module.

Detail-page modules must feel richer than carousel secondary images. Do not
make a set of ordinary banners with empty backgrounds and one isolated model.
Before generating each AD module, make the same human design decisions required
for AS images, but at a wider/editorial scale:

- Module role: hero, problem/solution, proof, structure/detail, use-case,
  specification, setup, or FAQ.
- Text system: no headline / large headline + subheadline / large spec /
  callout-only / comparison labels. A+ can use more text than AS, but the text
  must be grouped into a designed title zone, side panel, spec block, or caption
  band.
- Colour system: choose one accent colour from product, brand, scene, category,
  or reference image plus neutral text. Do not default to any fixed colour pair.
- Layout rhythm: vary modules across the set. Avoid several consecutive wide
  banners with centered product, black-on-white tags, or identical title
  placement.
- Detail and proof: connect labels, zoom windows, cutaways, icons, and spec
  blocks to real visible product parts or scene evidence.

Before generating each AD module, choose one memorable visual hook:

- **Lifestyle world**: family members, children, pets, furniture, room depth, or
  daily-life props that make the home context feel real. Children and pets can
  appear as atmosphere or scale context, but never show a child using fitness
  equipment unless the product is explicitly designed for children.
- **Physical proof anchored to the product**: if a module mentions footprint,
  show the base on the floor with a highlighted floor rectangle, subtle
  footprint zone, measuring-tape grid, clearance shadow, or furniture-scale
  comparison. If it mentions stability, show force through the frame, base
  pressure, suction-foot contact, or anti-wobble contrast. If it mentions
  adjustability, show the movement path on the upright holes and ghosted
  low/high states.
- **Editorial depth**: foreground detail, middle-ground product/action, and
  background context must all support the same claim. Avoid large unused blank
  areas unless they intentionally protect a strong headline.
- **Contrast device**: before/after, small-space/converted-space,
  unstable/stable, low/high adjustment, single exercise/multiple exercises, or
  ordinary tube/reinforced frame.
- **Connected detail**: use zoom windows, cutaways, overlays, or callout lines
  attached to the real product. Do not place generic floating icons that are not
  tied to visible product parts.

A+ creative gate: every AD module needs **one big idea + one visual event + one
environmental layer**. If the module can be described as "product with a label",
redesign it before generation. Use text to name the conclusion, but let the
scene, overlay, action, or product close-up prove it.

A+ layout quality gate:

- Headline, if used, must have a reserved title zone, deliberate size/line breaks,
  and colour hierarchy. It may be large and bold when it serves the module.
- Support text should be 1 short subheadline or 2-4 short proof labels, not a
  paragraph pasted over the image.
- Avoid repeating the same label style across AD modules. Mix title bands,
  diagonal panels, macro crops, icon rows, comparison panels, spec boards, and
  text-free lifestyle modules when appropriate.
- A+ detail modules should use comfortable enlarged part crops, rounded/circular
  zoom windows, cutaways, or connected insets, not a rigid grid of tiny labels.

Suggested AD module map:

- **AD-01 — Brand/value hero**: wide lifestyle banner; product in the target
  environment; concise value statement. Build a full home training atmosphere,
  not an empty room: family member watching, child/pet nearby as lifestyle
  context, warm furniture, mat, water bottle, sunlight, and room depth. Keep the
  product/action as the hero, but use family-life elements to make the image
  emotionally warmer and less sparse.
- **AD-02 — Problem/solution / space transformation**: show the buyer pain point
  and how the product solves it in one strong visual. If home footprint is the
  proof, anchor the claim to the base with a highlighted floor footprint,
  subtle rectangle, measuring grid, tape marks, or furniture clearance. Avoid a
  weak split screen where both sides look similar.
- **AD-03 — Core selling-point module**: combine related claims and proof points,
  e.g. load capacity + material thickness + reinforced frame. Show force moving
  through the frame, reinforced structure highlights, base pressure/contact, and
  connected tube-thickness detail, instead of only listing "150 kg" and
  "1.2 mm".
- **AD-04 — Product structure/detail module**: larger callout diagram or macro
  detail grid explaining important mechanics. Use connected zoom insets tied to
  the product, and make each inset answer a different concern: grip comfort,
  adjustment lock, dip handle contact, suction-foot stability, fastener/frame
  joint. Prefer one large hero detail plus 2-3 connected support details over a
  generic grid. Skip any inset that repeats another module.
- **AD-05 — Use-case module**: multiple scenes or actions showing how the
  product fits real daily use. Use a workout-flow composition, split scene,
  diagonal collage, radial action map, or multi-scene band; bodies must align
  correctly with bars and handles. The
  product may be smaller than in carousel images if action clarity is the point.
  For complex multi-action modules, split exercises into separate zones,
  repeated mini product views, or numbered action panels. Do not force
  pull-up, dip, knee raise, and push-up bodies onto one central product if it
  creates product distortion or wrong body/product contact.
- **AD-06 — Size/specification module**: dimensions, compatibility, fit, or
  model/spec table if those facts affect purchase confidence. Specs must be
  shown on the real product or floor plane: footprint on the base, height range
  on uprights, user/family silhouettes for scale, and exact numbers in a small
  clean spec block.
- **AD-07 — Setup/care/FAQ module**: optional only when installation, use steps,
  maintenance, or common objections are meaningful.

For detail-page modules, classify selling points the same way as secondary
images, but allow richer storytelling:

- Headline: buyer-facing result.
- Subheadline: 1 short supporting sentence when needed.
- Visual proof: real product scene, structural callout, spec table, or macro.
- Proof labels: exact specs from the user, not invented claims.

A+ module prompt checklist:

- Specify wide module format such as 970x600, 1464x600, or vertical long-module
  only when requested.
- State what fills foreground, middle ground, and background.
- State the exact product part that proves each spec.
- State the module's layout decision: text role, title zone, colour hierarchy,
  label style, product/person relationship, detail expression, and dynamic proof.
- Allow family, children, pets, or daily-life objects only when they support the
  buyer concern; keep them secondary to the product.
- Keep visible text designed and grouped: headline or large spec if useful,
  optional short subheadline, and 1-4 proof labels. Do not paste paragraphs over
  the image.
- Avoid making every module a centered product hero. Vary layout: cinematic
  home scene, floor-footprint proof, structural overlay, connected detail
  diagram, workout-flow scene, and specification board.

Do not use "详情图" to mean AS-06. If the user asks for "详情图里的细节模块",
generate AD-04, not AS-06, unless they explicitly say "副图细节图".

**When the target is Amazon**, after image generation or prompt output remind the user:
> ⚠️ AM-01 主图：使用真实拍摄白底照片，并在上传前复核 Amazon 当前图片规则。

For other platforms, use that profile's primary-image and live-check reminder; do not
show the Amazon AM-01 wording.

When creating the output manifest, record each selected asset in `media` with its role,
internal slot name, prompt/brief, source type, path, technical metadata and fact IDs. Mark
skipped slots only when the platform profile defined them; slot names are not platform
upload fields.

---

## STEP 4 — Save Excel summary

Skip this step in copy-only mode and image set only mode unless the user
explicitly asks for Excel, export, save, table, or a downloadable summary file.

For a full kit or requested export, save the normalized content, product evidence,
selling-point sheet, locked image plan, media assets and release-review checklist as a
JSON manifest following `references/platforms/listing-manifest.schema.json`. Record each
image's buyer question, visual proof, layout, exact text decision and evidence IDs. Do
not mark human release gates passed on the basis of prompts alone. Run the scoped policy
preflight and include its findings and production-readiness status in the workbook:

```bash
python3 /path/to/xborder-image-skill/scripts/validate_listing.py listing-manifest.json
python3 /path/to/xborder-image-skill/scripts/generate_excel.py listing-manifest.json \
  --output "[platform]_[market]_listing.xlsx"
```

The preflight applies deterministic checks to the manifest's declared metadata and
evidence references; it does not decode the actual image files or make visual judgments.
The `production_readiness` result can be `blocked`, `human_review_required`, or
`candidate_for_manual_upload`. The candidate state requires a completed human release
checklist and no open local findings; it is not marketplace approval. Visual truthfulness,
seller-account eligibility, restricted-product approvals, real-file inspection and live
category schemas remain explicit manual checks.

---

## STEP 5 — Done message

Adapt the done message to the mode. Do not claim images or Excel were generated
when the user requested copy-only output.

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 按本次模式输出完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 平台 / 站点 / 类目 / 语言：[scope]
📄 Listing 字段：[done/skip; use the selected profile's fields]
🖼️ 图片策划/成图：[done/skip]
📊 JSON manifest / Excel：[done/skip]
🏭 生产状态：[blocked / concept_preview / human_review_required / candidate_for_manual_upload]
⚠️ 未完成的类目、文件或 Seller Center 核对项：[list or none]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## COSMO dimensions (cover ≥8 across all copy)

isUsedFor / capableOf / suitableFor / hasProperty / partOf / relatedTo /
causes / motivatedBy / usedInContext / complementedBy / distinguishedFrom /
associatedWith / instanceOf / preconditionOf / enabledBy

---

## Quality gates (check before finishing)

- [ ] Platform, country/site, buyer locale and category are recorded; assumptions are labeled
- [ ] The market-scoped profile is applied; foreign-market limits are not reused
- [ ] Category-required fields come from a current schema or are marked unresolved
- [ ] Numeric facts and claim text map to evidence; no generic warranty/guarantee is added
- [ ] Full-kit/export manifest follows `listing-manifest.schema.json`; preflight findings are included
- [ ] Production status uses the three-state release standard; synthetic/unverified test assets are never labeled as upload candidates
- [ ] Selling-point sheet ranks buyer concerns, evidence strength, practical benefit, visual proof, and claim risk before the slot plan
- [ ] Every generated primary/gallery asset records buyer question, visual proof, why it earns gallery space, evidence IDs, and exact text/no-text decision
- [ ] Product-page URLs and direct image URLs are handled separately; only successfully inspected sources become evidence
- [ ] Human release-review gates are completed against final files, not inferred from generation prompts
- [ ] Preflight is described as a check, never as marketplace approval
- [ ] Listing copy checks apply only when listing copy is generated
- [ ] Amazon bullet/description lengths are not presented as hard limits without current category evidence
- [ ] Amazon US backend terms, if used, stay below 250 UTF-8 bytes and follow sourced guidance
- [ ] ≥8 COSMO dimensions covered when listing copy is generated
- [ ] Image generation matches requested mode; copy-only requests do not force images
- [ ] Broad "副图" requests produce a justified 5-7 image set, not a weak forced 8
- [ ] Exact "完整8张" requests produce AS-02 through AS-09 as 8 separate images
- [ ] Preview batches under 5 images are generated only when explicitly requested
- [ ] Multi-image sets use one shared product baseline copied unchanged into every slot prompt
- [ ] Sets of 5+ slots use sample-first staged generation (2 audited slots before the rest) unless the user opted out
- [ ] Output drift audit run — or explicitly declined by the user — for every multi-image set and quantity/variant edit before any consistency claim
- [ ] Drift fixes name the exact drifted attribute and regenerate only the affected slot, at most once, before reporting back
- [ ] Selling-point sheet separates user facts, observed facts, and AI-inferred points; inferred points are labeled and never appear as on-image numeric claims
- [ ] A+ module sets trace every module back to an AD-01 claim seed
- [ ] A+ modules use distinct copy roles; no three modules share the same sentence rhythm
- [ ] Style/competitor reference never occupies the identity anchor; the dual-reference path passes the drift audit before any consistency claim
- [ ] 参考图-only requests deliver concept boards clearly marked as not listing assets
- [ ] Slot ids and planning vocabulary do not appear as visible text on any image
- [ ] Prompts follow the locked shot plan; on-image text lines match the plan exactly
- [ ] Category profile from references/categories/ is applied when one matches; no cross-category props, scenes, or personas
- [ ] Image-audit mode delivers findings without generating; replacements only for user-approved slots
- [ ] Required product analysis finishes before set generation; analysis and generation are not started in parallel
- [ ] No numeric spec, certification, comparison, or performance claim lacks user or successful-analysis evidence
- [ ] Every slot preserves the same product count and variant allocation, or explicitly locks the reference-image count when exact values are unknown
- [ ] Completion text does not claim visual facts passed inspection unless output-image analysis proved them
- [ ] Every image has a buyer concern, visual proof, and strong thumbnail hierarchy
- [ ] Every image makes a deliberate layout decision: text/no text, text position, typography hierarchy, text background, product/person relationship, detail expression, and dynamic proof
- [ ] Each image expresses its selling point correctly even if it has no headline; the product, person, detail, or annotation must carry the claim
- [ ] Visible text, when used, has human-designed size, position, spacing, colour hierarchy, and optional background support; it does not feel auto-placed
- [ ] Visible headlines use concrete buyer-facing feature-benefit language, not generic poster slogans such as "Train More At Home" or "Fits Your Home Space"
- [ ] A multi-image set varies its visual proof and label system within the selected platform's image rules
- [ ] Fitness-equipment images may use bold accent-colour + neutral headline hierarchy, large spec numbers, side ribbons, circular icons, diagonal detail panels, or large part close-ups when they serve the selling point; accent colour is selected from product/brand/category/reference context, not fixed to orange/red
- [ ] Warm-home images follow Warm Real Home Ecommerce: realistic home photo feel, restrained annotations, natural warm light, no CGI showroom look
- [ ] Images do not show AI-poster artifacts: neon glow, energy rings, fantasy light trails, black-gold button badges, oversized motivational typography, duplicated ghost athletes, or product-obscuring bodies
- [ ] Product current state is protected; foldable/storage claims do not compress, shrink, or invent a more extreme product state
- [ ] Multi-action fitness images keep the product rigid and anatomically plausible; each body pose connects to the correct bar, handle, or base point
- [ ] Detail-page/A+ modules are not ordinary empty banners; each has one big idea, one visual event, and one environmental layer
- [ ] A+ specs are anchored to visible product parts or floor/room context, such as footprint on the base or load proof through the frame
- [ ] User style constraints such as "家庭风格" and "暖色" are visible in the prompt
- [ ] Visible image text language follows the selected site; any locale assumption is stated
- [ ] No source watermark, shop/marketplace logo, promo badge, price tag, or Chinese overlay text carried from the uploaded photo into the output (removed per STEP 0 "Source-image hygiene")
- [ ] Image text follows the selected market locale; actual product/packaging labels are preserved accurately
- [ ] Excel generation matches requested mode; copy-only requests do not write files unless export is requested
- [ ] Main-image guidance comes from the selected platform/market profile; do not show an Amazon warning for other platforms
- [ ] Excel file written only when the user requested export or full-kit output
