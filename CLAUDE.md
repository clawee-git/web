# web — clawee site

- Repo: `clawee-git/web` (public) · the clawee.org marketing + docs site ·
  trunk `main` · `gh.account = clawee-git` (call gh via `~/.claude/bin/ghp`,
  never bare `gh`).
- **Static, self-contained.** Plain HTML + CSS + a tiny vanilla JS for copy
  buttons. No build step, no framework, no CDNs, no webfonts (system monospace
  stack). Deploys by copying the files to a static host (same pattern as
  `release.clawee.org`).
- Layout: `index.html` (home), `help.html` (docs), `style.css` (design system),
  `script.js` (copy buttons), `assets/` (brand icon/mark from
  `clawee-git/resources/brand`).
- **Aesthetic:** terminal/dark — slate `#0F172A`, ink `#F7F8FF`, terminal-green
  `#4ADE80` accent (the clawee icon palette). Fully monospace. Keep it cohesive;
  don't introduce sans/serif or external assets.
- **Content sources (keep in sync):** the command/flag/key/slash reference on
  `help.html` mirrors `clawee-git/cli` `cmd/clawee/usage.go` — update it when the
  CLI surface changes. Install one-liners point at `release.clawee.org`
  (`clawee` client + `claweed` daemon). All burrowee references link to
  https://burrowee.com.
- Deploy target (domain/host) is TBD — the output is deploy-ready static files.

## Core principles

Minimum code that solves the stated problem. Surgical changes. Match the
existing terminal aesthetic. Verify rendering in a browser before claiming done.
No `Co-Authored-By` / "Generated with Claude" commit trailers; commit/push only
when asked.
