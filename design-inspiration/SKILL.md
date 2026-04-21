---
name: design-inspiration
description: Use when building UI components, landing pages, frontend code, or any visual design work. Enforces a reference-first workflow using curated design galleries before writing any code. Triggers on requests to "build a landing page", "design a component", "style this UI", "make this look better", or any frontend/visual task where aesthetic quality matters.
---

# Design Inspiration Skill

## Purpose

Before writing any frontend code, establish a concrete visual reference. This prevents generic AI-default aesthetics (purple gradients, center-aligned hero, Inter font, rounded-2xl everywhere) and ensures output matches a specific, intentional design direction.

The operator rule: a senior designer never starts with a blank canvas. They open Mobbin, Land-book, or their swipe file first. This skill enforces that same discipline.

## Workflow

### Step 1: Classify the design context

Identify what's being built, then map to the right reference source:

| Context | Primary Reference | Secondary |
|---------|------------------|-----------|
| Marketing landing page | landing.love | curations.supply |
| B2B SaaS product UI | saaspo.com | mobbin.com |
| Mobile app | mobbin.com | sleek.design |
| Design system / component library | component.gallery | saaspo.com |
| Brand identity / logo | rebrand.gallery | curations.supply |
| Typography decisions | uncut.wtf | — |
| Animation / motion | 60fps.design | — |
| Icons | hugeicons.com | — |

If the context is ambiguous, ask one clarifying question. Do not proceed to code without a reference.

### Step 2: Request references from the user

Tell the user:
1. Browse the recommended site
2. Paste 2–3 screenshots of designs to emulate
3. Note any specific elements they want pulled forward (hero layout, color palette, type treatment, motion style)

If the user provides a live URL instead of screenshots, use a headless browser or ask them to screenshot — do not guess at what the page looks like.

### Step 3: Extract the design spec

Using vision, analyze the screenshots and produce a structured design spec before coding:

- **Layout**: grid system, section rhythm, hero structure, max-width, gutter
- **Type scale**: heading sizes (h1–h3), body copy, line-height ratios, font families
- **Color system**: primary, secondary, neutrals, semantic colors — as hex values
- **Spacing**: padding/margin scale, vertical rhythm between sections
- **Component patterns**: button styles, card treatments, navigation pattern, form styling
- **Motion**: what animates, timing, easing curves, scroll behavior
- **Imagery**: photo vs illustration, treatment (grayscale, duotone, full color), aspect ratios

Output the spec as a short markdown block and get user confirmation before writing code.

### Step 4: Implement with approved tooling

**Icons — Hugeicons**

Install: `npm install hugeicons-react`

Import: `import { Home01Icon, Search01Icon } from 'hugeicons-react';`

**Typography — Uncut.wtf fonts (free, commercial use OK)**
- Download from https://uncut.wtf
- Host in `/public/fonts/` in the project
- Reference via `@font-face` in CSS
- Uncut Sans is the default workhorse — clean, modern, no licensing cost

**Animation — Framer Motion**

Install: `npm install framer-motion`

Reference 60fps.design for timing and easing inspiration. Default to:
- Transitions: 200–300ms
- Easing: `[0.22, 1, 0.36, 1]` (custom out-expo)
- Stagger children: 50–80ms

**Styling — Tailwind CSS**
- Generate design tokens from the extracted spec into `tailwind.config.js`
- Do not use Tailwind defaults blindly — override the palette and type scale

### Step 5: Verify against reference

After implementing, compare the output to the original references. Flag any deviations explicitly. Ask the user to confirm or redirect.

## Curated Resource Index

Full list of the source galleries:

- Design curation: https://curations.supply
- Landing pages: https://landing.love
- SaaS websites: https://saaspo.com
- Mobile apps: https://mobbin.com
- Fonts: https://uncut.wtf
- Animation: https://60fps.design
- Brands: https://rebrand.gallery
- Icons: https://hugeicons.com
- Design systems: https://component.gallery
- Competitor intel (AI builder): https://sleek.design

## Anti-Patterns

Do NOT:
- Start coding without a visual reference
- Use generic Tailwind defaults without extracting a spec first
- Default to "AI chatbot purple gradients", center-aligned everything, or rounded-2xl reflex
- Skip the vision analysis step — even if the user describes the reference in text, request the screenshot
- Use emojis in UI deliverables
- Invent colors or typography without explicit source

## Project Integration Notes

When working inside an existing HPV or Buffalo Strive project:
- Check for existing brand tokens first
  - HPV: navy (#0A1F3D base) + gold accents — confirm hex values in project's brand file
  - Buffalo Strive: reference `brand-system.md` in the Strive Proposal Engine project
- Match the existing design system rather than importing a new one
- Use this skill for new greenfield work, client deliverables, or when explicitly asked to redesign

For Holbrook Field Coach and future HPV client apps:
- Greenfield — use this skill in full
- Pull from saaspo.com for B2B UI patterns, mobbin.com for mobile app screens

## Output Format for Design Specs

When returning the extracted spec, structure it as: Layout (grid, max-width, section rhythm), Type (display/H2/body/caption sizes and line-heights), Color (primary, accent, neutrals as hex), Components (button/card specs), and Motion (page transitions, hover states, scroll reveals). Use hex values and explicit measurements — never vague descriptors.
