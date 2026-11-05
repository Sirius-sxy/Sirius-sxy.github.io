"""Check bilingual routes and rendered content after a Jekyll build (stdlib only)."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import unittest


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.elements = []
        self.text = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)

    def select(self, tag, **attrs):
        return [a for t, a in self.elements if t == tag and all(a.get(k) == v for k, v in attrs.items())]

    def has_text(self, text):
        return text in " ".join(self.text)


class SiteLanguagesTest(unittest.TestCase):
    routes = ("/", "/publications/", "/awards/", "/year-archive/", "/cv/")

    def read_page(self, route):
        return Page(SITE_DIR / route.lstrip("/") / "index.html")

    def local_path(self, url):
        return unquote(urlsplit(url).path)

    def test_paired_routes_metadata_and_switches(self):
        for route in self.routes:
            for prefix, lang, other_lang, label in (("", "en-US", "zh-CN", "中文"), ("/zh", "zh-CN", "en", "English")):
                with self.subTest(route=prefix + route):
                    current = prefix + route
                    other = route if prefix else "/zh" + route
                    page = self.read_page(current)
                    self.assertEqual(page.select("html")[0]["lang"], lang)
                    switch = page.select("a", **{"class": "language-switch"})
                    self.assertEqual(len(switch), 1)
                    self.assertEqual(switch[0]["href"], BASEURL + other)
                    self.assertEqual(switch[0]["hreflang"], other_lang)
                    self.assertTrue(page.has_text(label))
                    canonical = page.select("link", rel="canonical")[0]
                    self.assertEqual(self.local_path(canonical["href"]), BASEURL + current)
                    alternates = {a["hreflang"]: self.local_path(a["href"]) for a in page.select("link", rel="alternate") if "hreflang" in a}
                    self.assertEqual(alternates, {"en": BASEURL + route, "zh-CN": BASEURL + "/zh" + route, "x-default": BASEURL + route})
                    self.assertEqual(page.select("meta", property="og:locale")[0]["content"], lang.replace("-", "_"))

    def test_chinese_navigation_and_links_resolve(self):
        for route in self.routes:
            page = self.read_page("/zh" + route)
            for label in ("论文发表", "荣誉奖励", "博客文章", "个人简历", "清华大学", "网站最后更新于"):
                self.assertTrue(page.has_text(label), (route, label))
            links = {self.local_path(a["href"]) for a in page.select("a") if "href" in a}
            for target in self.routes:
                self.assertIn(BASEURL + "/zh" + target, links)
            for target in links:
                if target.startswith(BASEURL + "/zh/"):
                    relative = target[len(BASEURL):].lstrip("/")
                    self.assertTrue((SITE_DIR / relative / "index.html").is_file(), target)

    def test_collection_entries_stay_in_sync(self):
        for route in self.routes:
            en, zh = (self.read_page(prefix + route) for prefix in ("", "/zh"))
            en_entries = [a["href"] for a in en.select("a", rel="permalink")]
            zh_entries = [a["href"] for a in zh.select("a", rel="permalink")]
            self.assertTrue(en_entries, route)
            self.assertEqual(en_entries, zh_entries, route)
        home = self.read_page("/zh/")
        self.assertTrue(home.has_text("代表性论文"))
        self.assertTrue(home.has_text("可编程网络"))
        self.assertTrue(home.has_text("大语言模型"))
        publications = self.read_page("/zh/publications/")
        for text in ("著作", "期刊论文", "会议论文", "下载 PDF", "引用", "发表于"):
            self.assertTrue(publications.has_text(text), text)
        self.assertTrue(self.read_page("/publications/").has_text("Download PDF"))
        self.assertTrue(self.read_page("/zh/awards/").has_text("第三届 IPv6 技术应用创新大赛总决赛一等奖"))

    def test_cv_translations_and_downloads(self):
        for route in ("/cv/", "/zh/cv/"):
            page = self.read_page(route)
            downloads = [a for a in page.select("a") if "download" in a]
            self.assertEqual({a["download"] for a in downloads}, {"Xiaoyi-Shi-CV-en.pdf", "Xiaoyi-Shi-CV-zh.pdf"})
            for link in downloads:
                self.assertEqual(link["href"], BASEURL + "/files/" + link["download"])
                self.assertTrue((SITE_DIR / "files" / link["download"]).is_file())
        chinese = self.read_page("/zh/cv/")
        for text in ("教育背景", "博士研究生", "工学学士", "中文简历", "英文简历", "查看 PDF"):
            self.assertTrue(chinese.has_text(text), text)
        self.assertTrue(self.read_page("/cv/").has_text("Education"))

    def test_untranslated_details_offer_chinese_home_without_false_alternates(self):
        index = self.read_page("/publications/")
        target = self.local_path(index.select("a", rel="permalink")[0]["href"])[len(BASEURL):]
        path = SITE_DIR / target.lstrip("/")
        if path.is_dir():
            path /= "index.html"
        elif not path.is_file():
            path = path.with_suffix(".html")
        page = Page(path)
        self.assertEqual(page.select("a", **{"class": "language-switch"})[0]["href"], BASEURL + "/zh/")
        self.assertFalse([a for a in page.select("link", rel="alternate") if "hreflang" in a])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, default=Path("_site"))
    parser.add_argument("--baseurl", default="")
    args = parser.parse_args()
    SITE_DIR = args.site_dir
    BASEURL = args.baseurl.rstrip("/")
    unittest.main(argv=[__file__], verbosity=2)
