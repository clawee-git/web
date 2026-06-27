# Ops — clawee.org

Operator activation for the clawee.org static site. Mirrors the
`release.clawee.org` channel on the same host. **Steps 1–3 are one-time
OPERATOR-ACTIVATION** (by hand, on the host / Cloudflare); after that,
`deploy/deploy.sh` keeps the static surface in sync on every content change.

Host: `nsm.renative.com` (the box that also fronts `release.clawee.org` /
console / umbree / burree / `release.burrowee.com`). Static surface:
`/ebs_storage/apps/clawee.org/static` (matches `STATIC_DIR` in
`deploy/deploy.sh`). Edge: Cloudflare, **Full (strict)**.

The nginx vhost is `ops/nginx/clawee.org.conf`.

---

## 1. DNS — OPERATOR (Cloudflare)

`clawee.org` is already in Cloudflare (the zone serves `release.clawee.org`).
Add/confirm, **Cloudflare-proxied (orange cloud)**:

- `A`  `clawee.org`      → the nsm origin IP (same origin as `release.clawee.org`)
- `A`  `www.clawee.org`  → the nsm origin IP   *(optional — the vhost 301s www → apex)*

Full (strict) means CF validates the origin cert, so the real cert (step 3) must
be in place before the apex will serve.

## 2. Install the vhost — OPERATOR (nsm)

> **nsm-specific:** `/etc/nginx/nginx.conf` includes only
> `/etc/nginx/sites-enabled/*` — a file under `conf.d/` is silently dead. It
> **must** go into `sites-enabled/`. Do **not** add `default_server` (another
> sites-enabled file already owns it on `:443`).

```sh
# OPERATOR, on nsm:
sudo cp ops/nginx/clawee.org.conf /etc/nginx/sites-enabled/clawee.org.conf
sudo mkdir -p /ebs_storage/apps/clawee.org/static
```

## 3. Issue the origin cert — OPERATOR (nsm)

Issue a cert for `clawee.org` (+ `www.clawee.org`) the same way the
`release.clawee.org` / console vhosts on this host do (certbot / the host's LE
setup), then point the `ssl_certificate` / `ssl_certificate_key` placeholders in
the vhost at the real paths.

> **nsm-specific:** this host's nginx **rejects `TLSv1.3`** — the vhost pins
> `ssl_protocols TLSv1.2;`. Leave it.

## 4. Publish the site — OPERATOR

From a clone of this repo (needs SSH to nsm):

```sh
DRY=1 deploy/deploy.sh   # preview the transfer
deploy/deploy.sh         # rsync the static surface to STATIC_DIR
```

## 5. Validate + reload — OPERATOR (nsm)

```sh
# OPERATOR, on nsm:
sudo nginx -t && sudo systemctl reload nginx
```

Then verify from anywhere:

```sh
curl -sS -o /dev/null -w '%{http_code}\n' https://clawee.org/        # 200
curl -sS -o /dev/null -w '%{http_code}\n' https://clawee.org/help.html
```

## Updating content later

Edit the HTML/CSS, commit, then just re-run `deploy/deploy.sh` — no vhost or DNS
changes needed.
