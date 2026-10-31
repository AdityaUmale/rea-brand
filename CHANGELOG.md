# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [1.1.0] - 2026-10-31

### Added
- A shipped report template, `skills/rea-brand/report/build_report.py`, so every run produces the
  same designed `brand.html`: the five findings on the first screen, stat tiles that link to their
  evidence, SEEN / INFERRED pills (linkable), Stripe-style tables with numeric alignment and sticky
  headers, contact sheets with linked engagement keys, a log-scale growth chart with a compact
  phone version, copy-prompt panels, light and dark themes.
- `DESIGN.md` and `PRODUCT.md` documenting the report's design system.

### Changed
- `SKILL.md` now builds the HTML with the template and documents its `brand.md` conventions
  (stats, chart and prompt blocks, short-version format, contact-sheet names and sidecars).
- The Dan Koe example uses the new conventions.

## [1.0.0] - 2026-10-31

### Added
- The `rea-brand` skill: accounts, posts, growth curve, boosts, content patterns, the
  cross-platform system, funnel and money, moves vs growth, and a playbook with ready prompts.
- Full mode and content mode.
- Core four platforms (X, LinkedIn, Instagram, YouTube) with named data sources, plus any other
  platform treg has data for (Threads, Substack, TikTok, Facebook, Reddit, Bluesky, Medium,
  Pinterest).
- One-line installer, Claude Code plugin and marketplace manifests.
- A full example report (Dan Koe) and copy-paste prompts.

### Fixed during the first real run
- Prices in `SKILL.md` no longer use a dollar sign before a digit, which Claude Code read as an
  argument placeholder.
- X Articles (posts that are one bare link) are now detected, and the pinned post is fetched
  separately because the timeline can skip it.
- Old pinned Instagram posts are left out of the ranking.
- The early-era lookback now goes back to when the person had under 10K followers.
- Wayback Machine reads are limited to YouTube, with pacing for rate limits.
- Substack uses an endpoint with likes and comments instead of the RSS feed.
- The skill stops only at the account check and on cost overruns, not after every step.
- Commenters and small accounts are counted, never named.
