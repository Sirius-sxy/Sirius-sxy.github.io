# Publication maintenance workflow

This repo stores publications as individual Markdown files under `_publications/`.

## Recommended update flow

1. Prepare a JSON file that matches `scripts/publication-template.json`.
2. Run:
   ```bash
   python3 scripts/add_publication.py --input paper.json
   ```
3. Commit and push the repo.

## Required fields

- `title`
- `date` in `YYYY-MM-DD`
- `venue`
- `category` (`books`, `manuscripts`, or `conferences`)

## Optional fields

- `slug`
- `published`
- `paperurl`
- `repogiturl`
- `repozenodourl`
- `repodoiurl`
- `repolicense`
- `ccf`, `thcpl`, `core`
- `citation`
- `excerpt`
- `body`
- `extra_frontmatter`

## Notes

- The site page at `_pages/publications.html` renders `_publications/*.md` directly.
- The current collection categories are controlled in `_config.yml`.
- If a paper title is non-ASCII, provide a custom `slug`.
