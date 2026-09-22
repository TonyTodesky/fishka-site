#!/usr/bin/env bash
# Mirror Beget Sprutio public_html into ./legacy and ./public/legacy (both gitignored).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${1:-}"
if [[ -z "$SRC" ]]; then
  echo "Usage: $0 /path/to/.../s921183s.beget.tech/public_html" >&2
  exit 1
fi
mkdir -p "$ROOT/legacy" "$ROOT/public/legacy"
rsync -a --delete \
  --exclude 'index.php' \
  --exclude 'cgi-bin/' \
  --exclude '.DS_Store' \
  "$SRC/" "$ROOT/legacy/"
# Runtime assets for Astro (skip Word/Office zip backups in menus)
rsync -a --delete \
  --exclude 'index.php' \
  --exclude 'cgi-bin/' \
  --exclude '.DS_Store' \
  --exclude 'fishka2menu/*.zip' \
  --exclude 'fishka2menu/archive_*' \
  "$SRC/" "$ROOT/public/legacy/"
du -sh "$ROOT/legacy" "$ROOT/public/legacy"
echo "Synced legacy dump + public/legacy assets"
