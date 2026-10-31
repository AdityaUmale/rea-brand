---
name: /rea-brand report
description: An evidence report in the Stripe and Notion register; findings first, every number traceable.
colors:
  paper: "#ffffff"
  slate-surface: "#f6f8fa"
  slate-surface-2: "#eef2f6"
  navy-ink: "#0b1b33"
  slate-text: "#3c4a5e"
  slate-muted: "#6a7789"
  hairline: "#e3e8ee"
  hairline-strong: "#cfd7e1"
  signal-blue: "#2457e6"
  signal-blue-soft: "#e9efff"
  seen-green: "#0b7a4b"
  seen-green-bg: "#e5f5ec"
  inferred-amber: "#8a5300"
  inferred-amber-bg: "#fff2d6"
  night-paper: "#0d1117"
  night-surface: "#151b24"
  night-surface-2: "#1b2330"
  night-ink: "#eef2f7"
  night-text: "#b7c1ce"
  night-muted: "#8592a3"
  night-hairline: "#242d3a"
  night-hairline-strong: "#2f3a49"
  night-blue: "#7aa2ff"
  night-blue-soft: "#1a2440"
  night-seen: "#4fd18f"
  night-seen-bg: "#11291e"
  night-inferred: "#f2b84b"
  night-inferred-bg: "#2e2410"
  night-code: "#111720"
typography:
  display:
    fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "42px"
    fontWeight: 700
    lineHeight: 1.08
    letterSpacing: "-0.025em"
  headline:
    fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif"
    fontSize: "28px"
    fontWeight: 680
    lineHeight: 1.2
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif"
    fontSize: "19px"
    fontWeight: 620
    lineHeight: 1.35
    letterSpacing: "-0.01em"
  lead:
    fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif"
    fontSize: "17.5px"
    fontWeight: 620
    lineHeight: 1.4
    letterSpacing: "-0.01em"
  stat-value:
    fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif"
    fontSize: "28px"
    fontWeight: 680
    lineHeight: 1.1
    letterSpacing: "-0.02em"
    fontFeature: "\"tnum\""
  body:
    fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.65
    fontFeature: "\"cv11\", \"ss01\""
  table:
    fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif"
    fontSize: "14.5px"
    fontWeight: 400
    fontFeature: "\"tnum\""
  label:
    fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif"
    fontSize: "12.5px"
    fontWeight: 600
  pill:
    fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif"
    fontSize: "11px"
    fontWeight: 650
    lineHeight: 1
    letterSpacing: "0.05em"
  code:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    fontSize: "13.5px"
    lineHeight: 1.6
rounded:
  pill: "999px"
  marker: "2px"
  control: "8px"
  nav-item: "7px"
  icon-button: "9px"
  panel: "12px"
  tile: "14px"
spacing:
  topbar: "64px"
  sidebar: "264px"
  content-max: "880px"
  layout-max: "1320px"
  measure: "70ch"
  section-gap: "56px"
  main-x: "64px"
  tile-gap: "12px"
components:
  stat-tile:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.navy-ink}"
    typography: "{typography.stat-value}"
    rounded: "{rounded.tile}"
    padding: "15px 16px 14px"
  pill-seen:
    backgroundColor: "{colors.seen-green-bg}"
    textColor: "{colors.seen-green}"
    typography: "{typography.pill}"
    rounded: "{rounded.pill}"
    padding: "4px 7px"
  pill-inferred:
    backgroundColor: "{colors.inferred-amber-bg}"
    textColor: "{colors.inferred-amber}"
    typography: "{typography.pill}"
    rounded: "{rounded.pill}"
    padding: "4px 7px"
  button-copy:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.navy-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.control}"
    padding: "6px 10px"
  button-copy-hover:
    backgroundColor: "{colors.slate-surface}"
  button-icon:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.slate-text}"
    rounded: "{rounded.icon-button}"
    size: "36px"
  toc-link:
    textColor: "{colors.slate-muted}"
    rounded: "{rounded.nav-item}"
    padding: "6px 12px"
  toc-link-active:
    textColor: "{colors.signal-blue}"
  table-head:
    backgroundColor: "{colors.slate-surface}"
    textColor: "{colors.slate-muted}"
    typography: "{typography.label}"
    padding: "10px 14px"
  table-cell:
    textColor: "{colors.slate-text}"
    typography: "{typography.table}"
    padding: "11px 14px"
  prompt-panel:
    backgroundColor: "{colors.slate-surface}"
    textColor: "{colors.navy-ink}"
    typography: "{typography.code}"
    rounded: "{rounded.panel}"
    padding: "14px 16px"
  finding-number:
    backgroundColor: "{colors.signal-blue-soft}"
    textColor: "{colors.signal-blue}"
    rounded: "{rounded.control}"
    size: "26px"
---

# Design System: /rea-brand report

## Overview

**Creative North Star: "The Audited Ledger"**

The report reads like good product documentation that has been audited. White paper, cool slate, navy ink and one confident blue: the category standard of Stripe docs and Notion, picked on purpose so that nothing competes with the findings. Pages are dense but calm. Hairline rules and soft slate panels separate content; there is no ornament, and every colour beyond the neutrals means something.

Trust is the thing being designed. Evidence pills (SEEN in green, INFERRED in amber) are the only colour outside the blue accent. Every figure is set in tabular numerals, numeric table columns align right, and stat tiles link to the evidence behind them. The design never borrows the identity of the person being analysed; every report looks the same so the data is what changes.

The system rejects the dark, glowing analytics dashboard and the undifferentiated wall of doc text. Dark mode exists as a straight inversion of the same quiet system, not as a showpiece.

**Key Characteristics:**
- White and cool-slate grounds, navy ink, a single blue accent for links and the active state.
- Green and amber appear only as evidence pills; colour carries meaning, never decoration.
- Inter throughout, with tabular figures wherever numbers sit.
- Hairline borders (1px) and rounded panels (12 to 14px); one soft ambient shadow, used only on stat tiles.
- Sticky top bar and contents sidebar with a sliding active marker; the content column holds a 70ch measure.
- Light and dark themes from one token set, toggled and remembered.

## Colors

A cool, near-monochrome slate palette with one blue voice and two evidence signals.

### Primary
- **Signal Blue** (signal-blue; night-blue in dark): links (underlined at 35% tint, full on hover), the active contents link and its sliding marker, the chart line and dots, focus rings, the slash in the `/rea-brand` mark, and the numbered finding badges.
- **Signal Blue Soft** (signal-blue-soft; night-blue-soft in dark): text selection, finding-number badge ground, active contents chip on narrow screens.

### Secondary
- **Seen Green** (seen-green on seen-green-bg): the SEEN evidence pill, and the copy button's confirmed state ("Copied").

### Tertiary
- **Inferred Amber** (inferred-amber on inferred-amber-bg): the INFERRED evidence pill only.

### Neutral
- **Paper** (paper; night-paper): page ground, tile, table, chart and button grounds.
- **Slate Surface** (slate-surface; night-surface): table heads, callout panels, hover grounds, and the prompt panel (night-code in dark). **Slate Surface 2** is the deeper step.
- **Navy Ink** (navy-ink; night-ink): headings, bold text, stat values, first table column, code.
- **Slate Text** (slate-text; night-text): running text and table cells.
- **Slate Muted** (slate-muted; night-muted): meta lines, labels, table heads, captions, inactive contents links, chart axes.
- **Hairline** (hairline; night-hairline): every 1px border and section rule. **Hairline Strong** marks hover borders, chart pin lines, scrollbar thumb.

### Named Rules
**The One Voice Rule.** Blue is the only accent. It marks where you can go and where you are; it never fills a large area.

**The Evidence Colour Rule.** Green and amber are reserved for SEEN and INFERRED. No other component may use them for decoration, status or emphasis (the copy confirmation reuses green because it is a confirmed, seen action).

**The Paired Theme Rule.** Every colour has a light and a dark value from the same token name; components reference the role, never a hex.

## Typography

**Display Font:** Inter (with ui-sans-serif, system-ui, -apple-system, Segoe UI fallback)
**Body Font:** Inter
**Label/Mono Font:** ui-monospace, SFMono-Regular, Menlo, Consolas for prompt code only

**Character:** One neutral grotesque at fine weight steps (400 to 700, including 550, 620, 650, 680) does all the work; hierarchy comes from size, weight and negative tracking on headings, not from a second family. Body uses Inter's cv11 and ss01 alternates.

### Hierarchy
- **Display** (700, 42px, 1.08, -0.025em; 30px under 720px): the report title, balanced wrap.
- **Headline** (680, 28px, 1.2, -0.02em; 23px under 720px): section headings, which also feed the contents list.
- **Title** (620, 19px, 1.35, -0.01em): platform and play subheadings.
- **Lead** (620, 17.5px, 1.4): the bold first line of each numbered finding, with a 15px detail line under it.
- **Stat value** (680, 28px, 1.1, tabular; 22px under 720px): the figure in a stat tile.
- **Body** (400, 16px, 1.65): running text, paragraphs and list items capped at 70ch.
- **Table** (400, 14.5px, tabular): table cells; heads at 600, 12.5px muted.
- **Label** (600, 12.5px): table heads, the "Contents" title, the prompt panel head, buttons.
- **Pill** (650, 11px, 0.05em, uppercase): evidence pills only.

### Named Rules
**The Tabular Figures Rule.** Any element that shows counts, money, dates or rank sets `font-variant-numeric: tabular-nums`; numeric table columns right-align (left on phones, where tables scroll).

**The Uppercase Is Evidence Rule.** Uppercase tracked text is the evidence pill's voice. Headings and labels stay in sentence case.

## Layout

A docs layout. A 64px sticky top bar (mark left; person, date, repo link and theme toggle right) sits over a two-column grid: a 264px sticky contents sidebar with a right hairline, and a main column (64px side padding) holding an 880px article inside a 1320px frame. Text measure is 70ch.

The first viewport carries the title, a meta line, a row of four stat tiles (12px gap) and the numbered short version. Sections are separated by a hairline and 56px above and below it. Tables sit in a bordered wrapper; on wide screens their head row sticks under the top bar.

Responsive behaviour: at 1080px and below the sidebar becomes a horizontally scrolling sticky chip row under the top bar (active item on a soft blue chip, marker hidden) and main padding drops to 24px. At 720px and below stat tiles go two-up, the stat pill drops below the label, the top bar hides the person and repo, tables become max-content with horizontal scroll, and the growth chart swaps to its compact variant. Scroll padding (88px, 124px on narrow screens) keeps anchored headings clear of the sticky bars.

## Elevation & Depth

Flat and tonal. Depth comes from slate surfaces against paper and from 1px hairlines; the sticky top bar uses an 88% paper tint with a saturate-and-blur backdrop. One ambient two-layer shadow exists, and only stat tiles wear it, so the evidence tiles read as the one raised, clickable thing in the first viewport.

### Shadow Vocabulary
- **Tile lift** (`box-shadow: 0 1px 2px rgba(11,27,51,.06), 0 8px 24px -12px rgba(11,27,51,.12)`; dark: `0 1px 2px rgba(0,0,0,.4), 0 8px 24px -12px rgba(0,0,0,.6)`): stat tiles only.
- **Linked pill ring** (`box-shadow: inset 0 0 0 1px` currentColor at 28%, full on hover): marks an evidence pill that links to its source.

### Named Rules
**The Hairline First Rule.** Separate with a 1px hairline or a slate surface before reaching for a shadow. Panels, tables, prompts and charts are bordered, not lifted.

## Shapes

Soft rectangles at a small set of radii: 14px for stat tiles and the chart frame, 12px for tables, prompt panels, callouts and contact sheets, 9px for the icon button, 8px for buttons and finding badges, 7px for contents links, and full pills for evidence. Borders are always 1px. The only line accent is the 2px, 2px-radius sliding contents marker. Circles appear only in the chart (dots, pin badges, legend keys).

## Components

### Buttons
Quiet, bordered, utility controls.
- **Shape:** gently rounded (8px; icon button 9px, 36px square).
- **Copy button:** paper ground, navy ink, hairline border, 12.5px/600 label with a 14px stroke SVG icon, 6px 10px padding.
- **Hover / Focus:** border moves to hairline-strong and ground to slate surface over 150ms; focus is a 2px blue outline at 2px offset.
- **Confirmed:** label changes in place to "Copied" (or "Select and copy" on failure), text and border turn green, and it reverts after 1.8s.
- **Theme toggle:** 36px icon button with a stroked sun SVG; the choice persists in localStorage.

### Chips (evidence pills)
- **Style:** 11px/650 uppercase at 0.05em, 4px 7px padding, full radius; SEEN is green on green tint, INFERRED amber on amber tint, with a "SEEN · SELF-REPORTED" variant.
- **State:** a linked pill drops the underline and gains a 1px inset ring at 28% of its colour, full on hover. Pills are generated from SEEN / INFERRED in the source text; they never appear inside code.

### Cards / Containers
- **Corner Style:** 14px stat tiles and chart; 12px table wrapper, prompt panel and callout.
- **Background:** paper for tiles, tables and charts; slate surface for callouts and prompts.
- **Shadow Strategy:** tile lift on stat tiles only (see Elevation & Depth).
- **Border:** 1px hairline everywhere.
- **Internal Padding:** tiles 15px 16px 14px (12px on phones); chart 18px; prompt code 14px 16px; callout 14px 18px.

### Navigation
- **Top bar:** 64px, sticky, translucent paper with blur and a bottom hairline. The `/rea-brand` mark is 650/17px navy with the slash in blue.
- **Contents sidebar:** "Contents" label, then 14px muted links (6px 12px, 7px radius). Hover gives navy text on slate; active is blue at 550 weight. A 2px blue marker slides to the active item on scroll (350ms, cubic-bezier(.16,1,.3,1); no transition under reduced motion).
- **Mobile:** a sticky, horizontally scrolling chip row; the active chip sits on signal-blue-soft.

### Stat Tile (signature)
Value (28px tabular navy), muted label under it, evidence pill top right. When it has a link the whole tile is an anchor to its evidence; hover tints the border toward blue and lifts it 1px.

### Numbered Findings (signature)
The short version is a hairline-separated ordered list. Each item has a 26px blue-on-soft-blue numbered badge (8px radius), a 17.5px lead line and a 15px detail line, held to 70ch.

### Evidence Table
Stripe-docs style: bordered 12px wrapper, slate head row at 12.5px/600 muted, 11px 14px cells with hairline rows, first column navy at 500 and unwrapped, numeric columns right-aligned with tabular figures. On wide screens the head sticks under the top bar.

### Prompt Panel
A quiet code panel: slate ground, hairline border, 12px radius, a head row with a "Prompt" label and the copy button, then wrapped 13.5px monospace in navy ink.

### Growth Chart
A log-scale line chart in inline SVG: hairline gridlines at each power of ten, muted 12px axes, a 2.5px blue line with paper-filled blue-stroked dots, navy 13px point labels, and dashed pin lines with muted labels. Under 720px it swaps to a compact variant where pins become numbered circle badges explained by a legend list below.

## Do's and Don'ts

### Do:
- **Do** keep blue as the only accent: links, the active state, the chart line, focus.
- **Do** label findings with SEEN or INFERRED pills, and link the pill to its source when a source exists.
- **Do** set every number in tabular figures and right-align numeric table columns on wide screens.
- **Do** make stat tiles link to the evidence behind the figure.
- **Do** separate content with 1px hairlines and slate surfaces; reserve the tile shadow for stat tiles.
- **Do** define every colour for both themes under the same role name.
- **Do** hold running text to a 70ch measure.

### Don't:
- **Don't** use green or amber for anything other than evidence (and the confirmed copy state).
- **Don't** borrow the analysed person's colours, fonts or imagery style.
- **Don't** turn the report into a dark, glowing analytics dashboard: no gradients, glows or neon accents.
- **Don't** add a second type family for display; hierarchy comes from Inter's weight and size steps.
- **Don't** use uppercase tracked text outside the evidence pill.
