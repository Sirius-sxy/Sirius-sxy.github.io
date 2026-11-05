# Sirius-sxy.github.io
See [link](https://sirius-sxy.github.io) for details.

For automatic CV PDF generation and content updates, see [CV_WORKFLOW.md](CV_WORKFLOW.md).

The English pages live at `/`, and the Simplified Chinese pages at `/zh/`.
Their navigation, profile, and interface translations are in `_data/languages.yml`
and `_data/navigation.yml`. Paired pages set `lang` and `translation_url` in
front matter; shared includes render publications, awards, blog listings, and CV
data in both languages. Publication, award, and blog detail pages retain their original
content. Chinese award titles reuse `_data/cv.yml`.

After `bundle exec jekyll build`, run `python scripts/check_site_languages.py`
to check bilingual routes, metadata, shared entries, and CV download links.
