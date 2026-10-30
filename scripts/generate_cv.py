#!/usr/bin/env python3
"""Generate the downloadable Chinese CV from the website's source data.

    python scripts/generate_cv.py
    python scripts/generate_cv.py --output /tmp/cv.pdf --html-output /tmp/cv.html
"""

from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path
import re
from urllib.parse import urlparse

import bibtexparser
from bibtexparser.customization import getnames
from jinja2 import Environment, FileSystemLoader, select_autoescape
import yaml

ROOT = Path(__file__).resolve().parents[1]


def read_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def read_collection(directory: Path) -> list[dict]:
    items = []
    for path in sorted(directory.glob("*.md")):
        match = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|$)", path.read_text(encoding="utf-8"), re.S)
        if not match:
            raise ValueError(f"Missing YAML front matter: {path}")
        item = yaml.safe_load(match.group(1))
        if not isinstance(item, dict) or not item.get("title") or not item.get("date"):
            raise ValueError(f"Missing title or date: {path}")
        items.append({**item, "slug": path.stem})
    return items


def parse_date(value: date | str) -> date:
    # Existing collection dates sometimes omit leading zeroes (2025-9-22).
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return datetime.strptime(str(value), "%Y-%m-%d").date()


def short_venue(venue: str) -> str:
    # Prefer the acronym in "The ... Conference (ICNP 2026)".
    acronym = re.search(r"\(([^()]+\b\d{4})\)\s*$", venue)
    if acronym:
        venue = acronym.group(1)
    return re.sub(r"\s*\b(?:19|20)\d{2}\b", "", venue).strip()


def title_key(title: str) -> str:
    return " ".join(title.split()).casefold()


def publication(item: dict, overrides: dict, site_url: str) -> dict:
    entries = bibtexparser.loads(item.get("bibtex", "")).entries
    bib = entries[0] if entries else {}
    authors = item.get("authors", [])
    if not authors and bib.get("author"):
        authors = []
        for name in getnames(re.split(r"\s+and\s+", bib["author"])):
            family, _, given = name.partition(",")
            authors.append(f"{given.strip()} {family.strip()}".strip())
    venue = overrides.get("venue", short_venue(item.get("venue", "")))
    link = item.get("paperurl") or (site_url + item["permalink"] if item.get("permalink") else "")
    if urlparse(link).scheme not in ("https", "http"):
        link = ""
    return {
        "title": item["title"],
        "venue": venue,
        "year": bib.get("year", parse_date(item["date"]).year),
        "authors": authors,
        "citation": item.get("citation", ""),
        "ccf": str(item.get("ccf", "")).removeprefix("CCF-"),
        "poster_demo": item.get("poster_demo", False),
        "status": item.get("cv_status", "已录用，待发表" if item.get("published") is False else ""),
        "url": link,
    }


def build_context(root: Path) -> dict:
    config = read_yaml(root / "_config.yml")
    cv = read_yaml(root / "_data/cv.yml")
    site_url = config["url"].rstrip("/") + "/" + config.get("baseurl", "").strip("/")
    site_url = site_url.rstrip("/")
    collection = read_collection(root / "_publications")
    records = [
        item for item in collection
        if item.get("category") in cv["publication_categories"] and item.get("cv_include", True)
    ]
    publications = [
        (parse_date(item["date"]), publication(
            item, cv.get("publication_overrides", {}).get(item["slug"], {}), site_url
        ))
        for item in records
    ]
    # A collection opt-out must also suppress a matching reference-only entry.
    titles = {title_key(item["title"]) for item in collection}
    for item in cv.get("extra_publications", []):
        key = title_key(item["title"])
        if key not in titles:
            when = parse_date(item["date"]) if item.get("date") else date(int(item["year"]), 12, 31)
            publications.append((when, item))
            titles.add(key)
    publications.sort(key=lambda entry: entry[0], reverse=True)

    awards = []
    for item in read_collection(root / "_awards"):
        if item.get("cv_include", True):
            awards.append({**item, **cv.get("award_overrides", {}).get(item["slug"], {})})
    awards.extend(cv.get("extra_awards", []))
    awards.sort(key=lambda item: parse_date(item["date"]), reverse=True)
    for item in awards:
        when = parse_date(item["date"])
        item["period"] = f"{when.year} 年 {when.month} 月"

    photo = root / cv["photo"] if cv.get("photo") else None
    if photo and not photo.is_file():
        raise FileNotFoundError(f"CV portrait not found: {photo}")
    return {
        "cv": cv,
        "email": config["author"]["email"],
        "cv_url": site_url + "/cv/",
        "photo_uri": photo.resolve().as_uri() if photo else "",
        "publications": [item for _, item in publications],
        "awards": awards,
    }


def render_html(root: Path) -> str:
    env = Environment(
        loader=FileSystemLoader(root / "scripts/cv"),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return env.get_template("template.html").render(**build_context(root))


def generate_pdf(root: Path, output: Path, html_output: Path | None = None) -> int:
    # Keep data-only tests usable without native Pango libraries.
    from weasyprint import HTML

    html = render_html(root)
    document = HTML(string=html, base_url=str(root)).render()
    # Render to memory first so a failed build never truncates the existing PDF.
    pdf = document.write_pdf()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(pdf)
    if html_output:
        html_output.parent.mkdir(parents=True, exist_ok=True)
        html_output.write_text(html, encoding="utf-8")
    return len(document.pages)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, help="Defaults to files/Xiaoyi-Shi-CV-zh.pdf")
    parser.add_argument("--html-output", type=Path, help="Optional HTML for inspecting the print layout")
    args = parser.parse_args()
    root = args.repo_root.resolve()
    output = args.output or root / "files/Xiaoyi-Shi-CV-zh.pdf"
    pages = generate_pdf(root, output, args.html_output)
    print(f"Generated {output} ({pages} A4 page(s))")


if __name__ == "__main__":
    main()
