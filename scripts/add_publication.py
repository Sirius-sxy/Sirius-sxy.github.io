#!/usr/bin/env python3
"""Create or update a Jekyll publication page from a JSON spec.

Usage:
  python3 scripts/add_publication.py --input paper.json
  python3 scripts/add_publication.py --input paper.json --dry-run

Required JSON fields:
  - title
  - date        (YYYY-MM-DD)
  - venue
  - category    (books | manuscripts | conferences)

Optional JSON fields:
  - slug
  - published   (bool)
  - paperurl
  - repogiturl
  - repozenodourl
  - repodoiurl
  - repolicense
  - ccf / thcpl / core
  - citation
  - body        (markdown body after the front matter)
  - excerpt     (string front matter)
  - opensource  (bool)
  - extra_frontmatter (object with arbitrary additional keys)
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any

VALID_CATEGORIES = {"books", "manuscripts", "conferences"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^A-Za-z0-9]+", "-", normalized).strip("-").lower()
    slug = re.sub(r"-+", "-", slug)
    return slug


def yaml_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def build_frontmatter(meta: dict[str, Any], permalink_slug: str) -> str:
    lines = ["---"]
    lines.append(f"title: {yaml_value(meta['title'])}")
    lines.append("collection: publications")
    lines.append(f"category: {yaml_value(meta['category'])}")
    lines.append(f"permalink: /publication/{permalink_slug}")
    lines.append(f"date: {yaml_value(meta['date'])}")
    lines.append(f"venue: {yaml_value(meta['venue'])}")

    for key in ("published", "opensource"):
        if key in meta:
            lines.append(f"{key}: {yaml_value(meta[key])}")

    for key in (
        "paperurl",
        "repogiturl",
        "repozenodourl",
        "repodoiurl",
        "repolicense",
        "ccf",
        "thcpl",
        "core",
        "citation",
        "excerpt",
        "apa",
        "slidesurl",
        "posterurl",
        "reviewsurl",
    ):
        if meta.get(key):
            lines.append(f"{key}: {yaml_value(meta[key])}")

    extra = meta.get("extra_frontmatter", {})
    if not isinstance(extra, dict):
        raise SystemExit("extra_frontmatter must be an object/dict when provided")
    for key, value in extra.items():
        lines.append(f"{key}: {yaml_value(value)}")

    body = meta.get("body", "").rstrip()
    if body:
        lines.append("---")
        lines.append(body)
    else:
        lines.append("---")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to a JSON paper spec")
    parser.add_argument("--repo-root", default=Path(__file__).resolve().parents[1], help="Repository root")
    parser.add_argument("--dry-run", action="store_true", help="Print the generated markdown instead of writing")
    parser.add_argument("--force", action="store_true", help="Overwrite existing publication page if present")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    spec_path = Path(args.input).resolve()
    meta = load_json(spec_path)

    missing = [k for k in ("title", "date", "venue", "category") if not meta.get(k)]
    if missing:
        raise SystemExit(f"Missing required fields: {', '.join(missing)}")

    if meta["category"] not in VALID_CATEGORIES:
        raise SystemExit(f"category must be one of: {', '.join(sorted(VALID_CATEGORIES))}")

    try:
        datetime.fromisoformat(str(meta["date"]))
    except ValueError:
        raise SystemExit("date must be in ISO format YYYY-MM-DD")

    slug = meta.get("slug") or slugify(str(meta["title"]))
    if not slug:
        slug = f"publication-{meta['date']}"

    out_path = repo_root / "_publications" / f"{slug}.md"
    if out_path.exists() and not args.force and not args.dry_run:
        raise SystemExit(f"Refusing to overwrite existing file: {out_path} (use --force)")

    markdown = build_frontmatter(meta, slug)
    if args.dry_run:
        print(markdown)
        return 0

    out_path.write_text(markdown, encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
