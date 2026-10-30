"""Regression checks for CV synchronization, PDF text, and pagination."""

from pathlib import Path
import shutil
import tempfile
import unittest

from pypdf import PdfReader
import yaml

from scripts.generate_cv import ROOT, build_context, generate_pdf, render_html


class CVTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory in ("_data", "_publications", "_awards"):
            (self.root / directory).mkdir()
        shutil.copytree(ROOT / "scripts/cv", self.root / "scripts/cv")
        (self.root / "images").mkdir()
        shutil.copy(ROOT / "images/cv-portrait.png", self.root / "images/cv-portrait.png")
        # Fixed fixtures let the real CV grow without breaking CI expectations.
        (self.root / "_config.yml").write_text(yaml.safe_dump({
            "url": "https://sirius-sxy.github.io", "baseurl": "",
            "author": {"email": "shi-xy24@mails.tsinghua.edu.cn"},
        }), encoding="utf-8")
        (self.root / "_data/cv.yml").write_text(yaml.safe_dump({
            "name": "史笑屹", "author_name": "Xiaoyi Shi", "affiliation": "清华大学",
            "photo": "images/cv-portrait.png", "publication_categories": ["conferences", "manuscripts"],
            "education": [{"period": "2024 年—至今", "institution": "清华大学", "degree": "博士研究生"}],
            "experience": [{"title": "学生科协干事", "period": "2021 年—2022 年"}],
            "extra_publications": [{"title": "ElasticChain: A Submitted Paper", "venue": "NSDI",
                                    "year": 2027, "status": "已投稿", "authors": ["Xiaoyi Shi"]}],
            "extra_awards": [{"title": "清华大学综合奖学金", "date": "2026-01-01"}],
            "award_overrides": {"award": {"title": "竞赛一等奖", "location": "北京"}},
        }, allow_unicode=True), encoding="utf-8")
        self.add_record("_publications", "accepted.md", {
            "title": "Asynchrony-Resilient Communication", "date": "2027-05-11",
            "category": "conferences", "venue": "Example Conference (NSDI 2027)", "published": False,
            "bibtex": "@inproceedings{accepted, author={Yang, Yifan and Shi, Xiaoyi}, year={2027}}",
        })
        self.add_record("_publications", "journal.md", {
            "title": "SwitchTAD: A Journal Paper", "date": "2025-12-6", "category": "manuscripts",
            "venue": "Computer Networks", "published": True,
            "bibtex": "@article{journal, author={Zhou, Jiasheng and Shi, Xiaoyi}, year={2026}}",
        })
        self.add_record("_awards", "award.md", {
            "title": "Competition First Prize", "date": "2025-12-5", "location": "Beijing, China",
        })

    def add_record(self, collection, filename, metadata):
        (self.root / collection / filename).write_text(
            "---\n" + yaml.safe_dump(metadata, allow_unicode=True) + "---\n", encoding="utf-8"
        )

    def test_existing_metadata_and_reference_content(self):
        context = build_context(self.root)
        papers = context["publications"]
        self.assertEqual(papers[0]["status"], "已投稿")
        self.assertIn("ElasticChain:", papers[0]["title"])
        async_paper = next(p for p in papers if p["title"].startswith("Asynchrony"))
        self.assertEqual(async_paper["status"], "已录用，待发表")
        self.assertEqual(async_paper["venue"], "NSDI")
        self.assertIn("Xiaoyi Shi", async_paper["authors"])
        switch = next(p for p in papers if p["title"].startswith("SwitchTAD"))
        # Online publication date is 2025, bibliographic year is 2026.
        self.assertEqual(str(switch["year"]), "2026")
        self.assertEqual(len(papers), 3)
        self.assertEqual(len(context["awards"]), 2)
        self.assertEqual(context["awards"][1]["period"], "2025 年 12 月")
        self.assertEqual(context["awards"][1]["title"], "竞赛一等奖")

    def test_new_records_sync_and_html_is_escaped(self):
        self.add_record("_publications", "new.md", {
            "title": "New <research> & results", "date": "2028-2-1",
            "category": "conferences", "venue": "Example Conference (CONF 2028)",
            "published": False, "citation": "New author citation",
            "paperurl": "javascript:alert(1)",
        })
        self.add_record("_awards", "new.md", {
            "title": "New award", "date": "2028-2-1", "location": "Beijing",
        })
        context = build_context(self.root)
        paper = next(p for p in context["publications"] if p["title"].startswith("New"))
        self.assertEqual(paper["venue"], "CONF")
        self.assertEqual(paper["status"], "已录用，待发表")
        self.assertEqual(paper["url"], "")
        self.assertEqual(context["publications"][0]["title"], paper["title"])
        self.assertEqual(context["awards"][0]["title"], "New award")
        html = render_html(self.root)
        self.assertIn("New &lt;research&gt; &amp; results", html)
        self.assertIn("New author citation", html)
        self.assertIn("New award", html)
        self.assertNotIn("javascript:", html)

    def test_collection_supersedes_extra_and_opt_out_is_supported(self):
        title = build_context(self.root)["publications"][0]["title"]
        self.add_record("_publications", "elastic.md", {
            "title": title, "date": "2027-05-11", "category": "conferences",
            "venue": "NSDI 2027", "published": True,
        })
        papers = build_context(self.root)["publications"]
        matches = [p for p in papers if p["title"] == title]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["status"], "")
        self.add_record("_publications", "hidden.md", {
            "title": "Hidden record", "date": "2028-01-01", "category": "conferences", "cv_include": False,
        })
        self.assertNotIn("Hidden record", render_html(self.root))
        self.add_record("_publications", "elastic.md", {
            "title": title, "date": "2027-05-11", "category": "conferences", "cv_include": False,
        })
        self.assertNotIn(title, render_html(self.root))

    def test_baseurl_and_missing_photo(self):
        config_path = self.root / "_config.yml"
        config = yaml.safe_load(config_path.read_text())
        config["baseurl"] = "/academic"
        config["author"]["email"] = "updated@example.com"
        config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
        context = build_context(self.root)
        self.assertEqual(context["email"], "updated@example.com")
        self.assertEqual(context["cv_url"], "https://sirius-sxy.github.io/academic/cv/")
        (self.root / "images/cv-portrait.png").unlink()
        with self.assertRaises(FileNotFoundError):
            build_context(self.root)

    def test_pdf_has_a4_pages_chinese_and_every_publication(self):
        output = self.root / "out/cv.pdf"
        pages = generate_pdf(self.root, output)
        pdf = PdfReader(output)
        self.assertEqual(pages, len(pdf.pages))
        self.assertEqual(pages, 1, "The short fixture should fit one A4 page")
        text = " ".join(" ".join(page.extract_text() for page in pdf.pages).split())
        compact = "".join(text.split())
        for heading in ("史笑屹", "教育背景", "论文发表", "校园经历", "荣誉奖励"):
            self.assertIn(heading, compact)
        for paper in build_context(self.root)["publications"]:
            self.assertIn("".join(paper["title"].split()), compact)
        self.assertIn("清华大学综合奖学金", compact)
        self.assertNotIn("\ufffd", text)
        for page in pdf.pages:
            self.assertAlmostEqual(float(page.mediabox.width), 595.28, delta=1)
            self.assertAlmostEqual(float(page.mediabox.height), 841.89, delta=1)
            fonts = page["/Resources"]["/Font"]
            self.assertTrue(fonts, "PDF must contain text fonts")
            for reference in fonts.values():
                font = reference.get_object()
                for descendant in font.get("/DescendantFonts", [font]):
                    descriptor = descendant.get_object()["/FontDescriptor"]
                    self.assertTrue(
                        any(key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3")),
                        "Every text font must be embedded",
                    )

    def test_growth_flows_onto_additional_pages_without_dropping_entries(self):
        for index in range(25):
            self.add_record("_publications", f"future-{index}.md", {
                "title": f"Future research entry {index:02d}", "date": "2028-01-01",
                "category": "conferences", "venue": "Example Conference (CONF 2028)",
                "citation": "A complete citation retained in the generated document. " * 3,
            })
        output = self.root / "long.pdf"
        self.assertGreater(generate_pdf(self.root, output), 1)
        text = " ".join(page.extract_text() for page in PdfReader(output).pages)
        for index in range(25):
            self.assertIn(f"Future research entry {index:02d}", text)
        self.assertIn("荣誉奖励", "".join(text.split()))


if __name__ == "__main__":
    unittest.main()
