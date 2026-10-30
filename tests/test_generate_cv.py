"""Regression checks for CV synchronization, PDF text, and pagination."""

from pathlib import Path
import shutil
import subprocess
import sys
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
            "name": "史笑屹", "name_en": "Xiaoyi Shi", "author_name": "Xiaoyi Shi",
            "affiliation": "清华大学", "affiliation_en": "Tsinghua University",
            "photo": "images/cv-portrait.png", "publication_categories": ["conferences", "manuscripts"],
            "education": [{"period": "2024 年—至今", "institution": "清华大学", "degree": "博士研究生",
                           "period_en": "2024 – 2029 (expected)", "institution_en": "Tsinghua University",
                           "degree_en": "Ph.D."}],
            "experience": [{"title": "学生科协干事", "period": "2021 年—2022 年",
                            "title_en": "Student Association Member", "period_en": "2021 – 2022"}],
            "extra_publications": [{"title": "ElasticChain: A Submitted Paper", "venue": "NSDI",
                                    "year": 2027, "status": "已投稿", "status_en": "Submitted",
                                    "authors": ["Xiaoyi Shi"]}],
            "extra_awards": [{"title": "清华大学综合奖学金", "title_en": "Comprehensive Scholarship",
                              "date": "2026-01-01"}],
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

    def test_bibtex_author_formats_preserve_names_and_order(self):
        self.add_record("_publications", "authors.md", {
            "title": "Author parsing", "date": "2028-01-01", "category": "conferences",
            "venue": "CONF", "bibtex": """@inproceedings{names,
                author={Shi, Xiaoyi and Ludwig van Beethoven and de la Cruz, Juan and García, María},
                year={2028}
            }""",
        })
        paper = build_context(self.root)["publications"][0]
        self.assertEqual(paper["authors"], [
            "Xiaoyi Shi", "Ludwig van Beethoven", "Juan de la Cruz", "María García",
        ])
        self.assertIn("<strong>Xiaoyi Shi</strong>", render_html(self.root))

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

    def test_english_translations_preserve_shared_records_and_chinese(self):
        english = build_context(self.root, "en")
        chinese = build_context(self.root)
        self.assertEqual(english["cv"]["name"], "Xiaoyi Shi")
        self.assertEqual(english["cv"]["education"][0]["degree"], "Ph.D.")
        self.assertEqual(english["cv"]["experience"][0]["title"], "Student Association Member")
        self.assertEqual(english["publications"][0]["status"], "Submitted")
        self.assertEqual(english["publications"][1]["status"], "Accepted, to appear")
        self.assertEqual(english["awards"][0]["title"], "Comprehensive Scholarship")
        self.assertEqual(english["awards"][1]["title"], "Competition First Prize")
        self.assertEqual(english["awards"][1]["location"], "Beijing, China")
        self.assertEqual(english["awards"][1]["period"], "Dec 2025")
        self.assertEqual(chinese["cv"]["name"], "史笑屹")
        self.assertEqual(chinese["awards"][1]["title"], "竞赛一等奖")
        for en, zh in zip(english["publications"], chinese["publications"], strict=True):
            for key in ("title", "authors", "venue", "year", "ccf", "url"):
                self.assertEqual(en.get(key), zh.get(key))
        html = render_html(self.root, "en")
        self.assertIn('<html lang="en">', html)
        self.assertIn("<strong>Xiaoyi Shi</strong>", html)
        self.assertNotRegex(html, r"[\u3400-\u9fff]")

    def test_english_sync_status_and_award_overrides(self):
        self.add_record("_publications", "new.md", {
            "title": "New <paper>", "date": "2028-01-01", "category": "conferences",
            "venue": "CONF", "cv_status": "在审", "cv_status_en": "Under review",
        })
        self.add_record("_awards", "new.md", {
            "title": "New Award", "date": "2028-01-01", "location": "London",
        })
        path = self.root / "_data/cv.yml"
        cv = yaml.safe_load(path.read_text())
        cv["award_overrides_en"] = {"award": {"title": "First Prize, NVIDIA Track"}}
        path.write_text(yaml.safe_dump(cv, allow_unicode=True), encoding="utf-8")
        english = build_context(self.root, "en")
        self.assertEqual(english["publications"][0]["status"], "Under review")
        self.assertEqual(english["awards"][0]["title"], "New Award")
        self.assertEqual(english["awards"][-1]["title"], "First Prize, NVIDIA Track")
        self.assertEqual(english["awards"][-1]["location"], "Beijing, China")
        self.assertIn("New &lt;paper&gt;", render_html(self.root, "en"))
        self.assertEqual(build_context(self.root)["awards"][-1]["title"], "竞赛一等奖")

    def test_english_cli_writes_separate_pdf_with_complete_text(self):
        chinese = self.root / "files/Xiaoyi-Shi-CV-zh.pdf"
        chinese.parent.mkdir()
        chinese.write_bytes(b"Existing Chinese PDF")
        html_path = self.root / "preview/cv-en.html"
        subprocess.run([
            sys.executable, str(ROOT / "scripts/generate_cv.py"), "--repo-root", str(self.root),
            "--language", "en", "--html-output", str(html_path),
        ], check=True, capture_output=True, text=True)
        self.assertEqual(chinese.read_bytes(), b"Existing Chinese PDF")
        self.assertIn('<html lang="en">', html_path.read_text())
        pdf = PdfReader(self.root / "files/Xiaoyi-Shi-CV-en.pdf")
        text = " ".join(" ".join(page.extract_text() for page in pdf.pages).split())
        for phrase in ("Xiaoyi Shi", "Education", "Publications and Manuscripts", "Campus Service",
                       "Honors and Awards", "Accepted, to appear", "Submitted", "Comprehensive Scholarship"):
            self.assertIn(phrase, text)
        for paper in build_context(self.root, "en")["publications"]:
            self.assertIn(paper["title"], text)
        self.assertNotRegex(text, r"[\u3400-\u9fff\ufffd]")
        self.assertEqual(len(pdf.pages), 1)
        self.assertAlmostEqual(float(pdf.pages[0].mediabox.width), 595.28, delta=1)
        self.assertAlmostEqual(float(pdf.pages[0].mediabox.height), 841.89, delta=1)

    def test_unsupported_language_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unsupported CV language"):
            build_context(self.root, "fr")

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
        for language, heading in (("zh", "荣誉奖励"), ("en", "HonorsandAwards")):
            with self.subTest(language=language):
                output = self.root / f"long-{language}.pdf"
                self.assertGreater(generate_pdf(self.root, output, language=language), 1)
                text = " ".join(page.extract_text() for page in PdfReader(output).pages)
                for index in range(25):
                    self.assertIn(f"Future research entry {index:02d}", text)
                self.assertIn(heading, "".join(text.split()))


if __name__ == "__main__":
    unittest.main()
