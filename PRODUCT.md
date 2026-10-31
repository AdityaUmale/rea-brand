# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
- **Skill users:** creators, founders and marketers who run `/rea-brand` in Claude Code on a public creator, then read the teardown to decide what to copy for their own brand. Usually starting out or growing (under 50K followers).
- **Launch viewers:** people scrolling X who see the report in a launch post or screen recording and decide in seconds whether the skill is worth installing.

## Product Purpose
`/rea-brand` is an open-source Claude Code skill that reverse engineers a person's personal brand. Given a name or handle, it finds every public account, pulls their posts, and reports when they grew, who boosted them, how their posts are made, how one idea moves across platforms, how they make money, and ten plays to copy, each with a paste-ready prompt. Success: the reader acts on a play the same week, and a launch viewer installs the skill.

## Positioning
Evidence-first: every finding is counted from real pulled posts and labeled SEEN (linked) or INFERRED (reasoned), with the exact data cost per step (a full 6-platform teardown measured about 8 cents). A "personal brand guide" or a generic AI summary cannot show the counts, the links, or the bill.

## Operating Context
- The report is generated per run as one self-contained HTML file (`brand.html`, images inlined as base64) plus `brand.md` and CSVs, in `rea-brand/<person>/`.
- It is opened locally in a browser, screenshotted, screen-recorded for X, and shared.
- Data comes through treg (treg.to); the skill runs inside Claude Code.

## Capabilities and Constraints
- Single HTML file, no external runtime dependencies beyond optional web fonts; must work offline once fonts are cached or fall back cleanly.
- Light and dark themes; readable on desktop and phone.
- Content varies per person: number of platforms (1–8+), images per platform, plays (10), prices, tables.
- The report builder ships inside the skill as the standard template for every run.

## Brand Commitments
- Name: `/rea-brand` (lowercase, with the slash).
- Voice: plain, direct, specific numbers; SEEN / INFERRED labels are part of the product.
- The report must not borrow the analyzed person's own visual identity.

## Evidence on Hand
- A real run: Dan Koe, 2026-10-31, 6 platforms, 501 posts, 118 calls, $0.081. Source: `rea-brand/dan-koe/brand.md`, CSVs, contact sheets in `rea-brand/dan-koe/*/img/`.
- No testimonials, user counts, or press exist; do not invent them.

## Product Principles
1. Findings before prose: the reader sees what was found before reading how.
2. Every number is traceable: counted, dated, linked, labeled.
3. Actionable over impressive: each finding ends in something the reader can do.
4. Honest scope: say what was not seen, skipped, or self-reported.
