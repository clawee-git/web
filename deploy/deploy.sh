#!/usr/bin/env bash
# Deploy the clawee.org static site to the nsm origin.
#
# Mirrors the static surface (index.html, help.html, style.css, script.js,
# assets/) into STATIC_DIR on the host. Idempotent; safe to re-run on every
# content change. OPERATOR-run (needs SSH to nsm) — see ops/README.md for the
# one-time activation (DNS, vhost, cert).
#
# Usage:
#   deploy/deploy.sh                 # rsync to nsm:STATIC_DIR
#   HOST=user@nsm.renative.com deploy/deploy.sh
#   DRY=1 deploy/deploy.sh           # show what would transfer, change nothing
set -euo pipefail

HOST="${HOST:-root@nsm.renative.com}"
STATIC_DIR="${STATIC_DIR:-/ebs_storage/apps/clawee.org/static}"

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# Exactly the served surface — never ship repo meta, ops, or deploy scripts.
FILES=(index.html docs style.css script.js favicon.ico assets)

echo "→ deploying clawee.org to ${HOST}:${STATIC_DIR}"
ssh "$HOST" "mkdir -p '$STATIC_DIR'"

RSYNC_OPTS=(-az --delete --omit-dir-times --no-perms
            --exclude '.DS_Store')
[ "${DRY:-}" = "1" ] && RSYNC_OPTS+=(--dry-run -v)

rsync "${RSYNC_OPTS[@]}" "${FILES[@]}" "${HOST}:${STATIC_DIR}/"

echo "✓ done. Verify: curl -sS -o /dev/null -w '%{http_code}\\n' https://clawee.org/"
