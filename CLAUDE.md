# web — clawee site

- Repo: `clawee-git/web` (public) · the clawee.org marketing + docs site ·
  trunk `main` · `gh.account = clawee-git` (call gh via `~/.claude/bin/ghp`,
  never bare `gh`).
- **Static, self-contained.** Plain HTML + CSS + a tiny vanilla JS for copy
  buttons. No build step, no framework, no CDNs, no webfonts (system monospace
  stack). Deploys by copying the files to a static host (same pattern as
  `release.clawee.org`).
- Layout: `index.html` (home), `docs/index.html` (docs), `style.css` (design system),
  `script.js` (copy buttons), `assets/` (brand icon/mark from
  `clawee-git/resources/brand`).
- **Aesthetic:** terminal/dark — slate `#0F172A`, ink `#F7F8FF`, terminal-green
  `#4ADE80` accent (the clawee icon palette). Fully monospace. Keep it cohesive;
  don't introduce sans/serif or external assets.
- **Content sources (keep in sync):** the command/flag/key/slash reference on
  `docs/index.html` mirrors `clawee-git/cli` `cmd/clawee/usage.go` — update it when the
  CLI surface changes. Install one-liners point at `release.clawee.org`
  (`clawee` client + `claweed` daemon). All burrowee references link to
  https://burrowee.com.
- **LIVE at https://clawee.org** — served static from nsm (Cloudflare Full-strict).
  Re-deploy content any time with `deploy/deploy.sh` (rsync → nsm). The one-time
  host activation (cert via snap certbot `--dns-cloudflare`, vhost in
  `sites-enabled`) is done; full runbook in `ops/README.md`. `www.clawee.org`
  301s → apex (DNS record live, cert covers it).
- **URL shape:** clean paths — home at `/` (`index.html`), docs at `/docs`
  (`docs/index.html`, directory index). No `.html` in URLs; the vhost 301s
  `/help.html`→`/docs` and `/index.html`→`/`. Add a new page as `<name>/index.html`.

## Core principles

Minimum code that solves the stated problem. Surgical changes. Match the
existing terminal aesthetic. Verify rendering in a browser before claiming done.
No `Co-Authored-By` / "Generated with Claude" commit trailers; commit/push only
when asked.

- **Version badge:** `index.html` carries a `<span class="ver">v0.1.61</span>` next to the Install heading. Bump it on every `clawee` release (and bump `style.css?v=N` if styles change so the edge cache refreshes).
