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
  CLI surface changes. Note `usage.go` is the TOP-LEVEL map only; per-command verbs
  (e.g. `relays auto` / `relays gateway`) live in each command's own usage const, so
  check both. `llms-full.txt` is a full mirror of `docs/index.html` — **every docs edit
  lands in both** (the 2026-07-17 pass updated only the HTML and left `llms-full.txt`
  stale for two weeks). Install one-liners point at `release.clawee.org`
  (`clawee` client + `claweed` daemon). All burrowee references link to
  https://burrowee.com.
- **Docs-sync marker:** `docs_sync.json` records, per sync, the cli/daemon commits the
  docs were verified against + the released versions. Next sync = read the newest entry,
  review `git log <sha>..origin/main` in each repo, update the pages, then PREPEND a new
  entry (never edit a past one) and bump the "Docs synced …" stamp at the foot of
  `docs/index.html` + `llms-full.txt`. Sync against the RELEASED surface, not cli `main`
  — the site describes what users can actually run. That stamp is deliberately plain
  text, NOT `class="ver"`: `script.js` rewrites `.ver` spans to the live channel version,
  which would make the stamp claim a sync that never happened.
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

- **Version badge:** `index.html` carries a `<span class="ver">v0.1.80</span>` next to the Install heading. It **auto-updates at runtime** — `script.js` loads `https://release.clawee.org/clawee/version.js` (JSONP `__claweeVersion({version,…})`, sourced from the R2 `latest.json` catalog) and rewrites every `.ver` span. The hardcoded value is only the **fallback** if the channel is unreachable, so you no longer need to bump it per release (keep it roughly current for the no-JS case). Bump the `script.js?v=N` / `style.css?v=N` query when those files change so the edge cache refreshes.
