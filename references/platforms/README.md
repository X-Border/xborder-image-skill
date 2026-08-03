# Platform profiles — multi-marketplace listing image skill

This skill (X-Border Listing Image Skill) generates listing copy + listing/marketing
images for multiple e-commerce marketplaces. Amazon is the reference implementation;
Temu and Noon are supported. Adding another marketplace = write one profile file here,
reuse everything else.

## What is SHARED (write once, all platforms reuse)

- **Execution modes** — full kit / image-set-only / copy-only / single-slot / A+ /
  preview (SKILL.md STEP 0).
- **Product & selling-point reading** and current-state protection (STEP 0).
- **Image backend** — how a brief becomes a rendered image via the current X-Border MCP
  tools (`references/image-backend.md`).
- **Image-craft principles** — thumbnail legibility, one message per image, real
  product match, no AI-poster artifacts (SKILL.md STEP 3 + `amazon-image-strategy.md`).
- **Excel export** (`scripts/generate_excel.py`, STEP 4) and the done message (STEP 5).

## What is PER-PLATFORM (one file in this folder)

1. **Copy rules** — title format/length, bullet/highlight count & format, description
   length, keyword/search-term budget, language(s).
2. **Image slot taxonomy** — the slot ids and meaning for that marketplace.
3. **Compliance** — main-image rules, banned content, cultural/localisation notes.

## Files

| file | status |
|---|---|
| `amazon.md` | ✅ reference — detailed slot briefs live in `SKILL.md` STEP 1/3/3B |
| `temu.md` | ✅ implemented |
| `noon.md` | ✅ implemented |

## Resolution at runtime (SKILL.md STEP 0)

Detect the platform from the request (default **Amazon**). Load that profile, apply its
copy rules + slot taxonomy, and reuse the shared flow for everything
else. If the user does not name a platform, ask or default to Amazon.

## Adding a new platform (checklist)

1. Copy a profile.
2. Fill copy rules (title/bullets/description/keywords) + language(s).
3. Define the slot taxonomy + default recommended set.
4. Note compliance (main image, banned content, localisation).
5. Add the platform's trigger words to `SKILL.md` frontmatter `description` + a
   detection cue in STEP 0.
6. Everything else (modes, backend, Excel, image craft) is inherited — do not copy.
