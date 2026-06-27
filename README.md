# clawee web

The clawee marketing + docs site — a static, self-contained two-page site.

- `index.html` — home: intro, install one-liner, how-it-works, why-clawee.
- `docs/index.html` — docs: requirements (burrowee), install, pairing, full command reference.
- `style.css` — the terminal-themed design system (dark slate, terminal-green accent).
- `script.js` — copy-to-clipboard for command snippets (no dependencies).
- `assets/` — brand icon/mark (from `clawee-git/resources/brand`).

No build step, no framework, no CDNs. Open `index.html` in a browser, or deploy
the files as-is (static host — same pattern as `release.clawee.org`).

## Develop

```sh
python3 -m http.server 8080   # then open http://localhost:8080
```

## Content sources

Commands/flags mirror `clawee-git/cli` (`cmd/clawee/usage.go`). The install
one-liners point at `release.clawee.org`. burrowee references link to
https://burrowee.com.
