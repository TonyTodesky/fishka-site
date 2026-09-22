#!/usr/bin/env python3
"""Import Fishka articles from the local Beget dump (legacy/), not HTTP.

Prefers Windows-1251 HTML from the Sprutio account archive and rewrites
image/asset URLs to /legacy/... so Astro can serve them from public/legacy.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "src/data/catalog.json"
OUT = ROOT / "src/content/articles"
LEGACY = ROOT / "legacy"
HOST_RE = re.compile(r"^https?://(www\.)?fishka\.spb\.ru(?::\d+)?", re.I)


def decode(raw: bytes) -> str:
    for enc in ("windows-1251", "utf-8", "cp1251", "koi8-r", "latin1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("latin1", errors="replace")


def extract_main(html: str) -> str:
    m = re.search(
        r'<td[^>]*width=["\']?73%[^>]*>(.*?)<td[^>]*width=["\']?3',
        html,
        re.I | re.S,
    )
    if m:
        return m.group(1)
    m = re.search(
        r'<td[^>]*bgcolor=["\']?#FFCC33[^>]*>(.*?)<td[^>]*width=["\']?3',
        html,
        re.I | re.S,
    )
    if m:
        return m.group(1)
    m = re.search(r"<body[^>]*>(.*)</body>", html, re.I | re.S)
    return m.group(1) if m else html


def site_path_from_url(url: str) -> str | None:
    """Map absolute fishka URL or site-absolute path to legacy-relative path."""
    url = url.strip()
    if not url or url.startswith(("mailto:", "data:", "javascript:", "#")):
        return None
    if HOST_RE.match(url):
        path = HOST_RE.sub("", url)
        path = urlsplit(path).path
        return unquote(path.lstrip("/"))
    if url.startswith("/"):
        return unquote(url.lstrip("/"))
    return None


def to_legacy_url(value: str, base_original: str) -> str:
    value = value.strip()
    if not value or value.startswith(("mailto:", "data:", "javascript:", "#")):
        return value

    mapped = site_path_from_url(value)
    if mapped is None:
        # Relative to the article's original URL
        abs_url = urljoin(base_original, value)
        mapped = site_path_from_url(abs_url)
        if mapped is None:
            return value

    # Keep external non-fishka absolute URLs untouched
    if value.startswith(("http://", "https://")) and not HOST_RE.match(value):
        return value

    local = LEGACY / mapped
    if local.exists():
        return "/legacy/" + mapped.replace("\\", "/")
    # Prefer local path even if missing (so broken imgs are obvious offline)
    if mapped.startswith(("articles/", "hat/", "fishka1menu/", "fishka2menu/")):
        return "/legacy/" + mapped.replace("\\", "/")
    return value


def clean(fragment: str, base_original: str) -> str:
    fragment = re.sub(r"<script\b[^>]*>.*?</script>", "", fragment, flags=re.I | re.S)
    fragment = re.sub(r"<!--.*?-->", "", fragment, flags=re.S)
    fragment = re.sub(r"on\w+\s*=\s*(\"[^\"]*\"|'[^']*')", "", fragment, flags=re.I)

    def rewrite(match: re.Match[str]) -> str:
        attr, quote, value = match.group(1), match.group(2), match.group(3)
        return f"{attr}={quote}{to_legacy_url(value, base_original)}{quote}"

    fragment = re.sub(r'(src|href)=("|\')([^"\']+)\2', rewrite, fragment, flags=re.I)
    fragment = re.sub(r"\s+", " ", fragment)
    fragment = re.sub(r">\s+<", "><", fragment)
    return fragment.strip()


def slug_from_href(href: str) -> str:
    path = href.split("/articles/", 1)[-1]
    path = re.sub(r"\.(html?|htm)$", "", path, flags=re.I)
    return path.strip("/")


def resolve_local(original: str) -> Path | None:
    mapped = site_path_from_url(original)
    if not mapped:
        return None
    candidate = LEGACY / mapped
    if candidate.is_file():
        return candidate
    # Try alternate extensions used on the old site
    stem = candidate.with_suffix("")
    for ext in (".html", ".htm", ".HTML", ".HTM"):
        alt = Path(str(stem) + ext)
        if alt.is_file():
            return alt
    return None


def main() -> None:
    if not LEGACY.is_dir():
        raise SystemExit(
            f"Missing {LEGACY}. Copy Beget public_html there first "
            "(see scripts/sync_legacy.sh)."
        )

    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    imported: list[dict] = []
    ok = missing = 0

    items = list(data.get("news", [])) + [
        article for section in data["sections"] for article in section["items"]
    ]

    for item in items:
        href = item.get("href") or item.get("original") or ""
        original = item.get("original")
        if not original:
            if str(href).startswith("http"):
                original = href
            elif "/articles/" in str(href):
                original = "http://www.fishka.spb.ru" + (
                    href if str(href).startswith("/") else "/" + str(href)
                )
            else:
                continue
        if "fishka.spb.ru" not in original and "/articles/" not in original:
            continue

        slug = slug_from_href(original)
        dest = OUT / f"{slug}.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        local = resolve_local(original)
        try:
            if not local:
                raise FileNotFoundError(f"not in legacy dump: {original}")
            html = decode(local.read_bytes())
            fragment = clean(extract_main(html), original)
            dest.write_text(fragment, encoding="utf-8")
            status = "ok"
            ok += 1
        except Exception as exc:  # noqa: BLE001
            dest.write_text(
                f"<p>Не удалось импортировать оригинал из локального дампа.</p>"
                f"<p>{original}</p>",
                encoding="utf-8",
            )
            status = f"error:{exc}"
            missing += 1
        imported.append(
            {
                "title": item.get("title"),
                "section": item.get("section"),
                "slug": slug,
                "original": original,
                "file": str(dest.relative_to(ROOT)),
                "status": status,
                "source": "legacy" if status == "ok" else "missing",
            }
        )
        print(status, slug)

    (ROOT / "src/data/imported.json").write_text(
        json.dumps(imported, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"imported {len(imported)} (ok={ok}, missing={missing})")


if __name__ == "__main__":
    main()
