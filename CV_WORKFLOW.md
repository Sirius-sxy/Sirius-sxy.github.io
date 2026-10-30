# CV PDF 自动生成

CV 页面 `/cv/` 底部提供中英文 PDF 的预览和下载，文件路径分别为
`/files/Xiaoyi-Shi-CV-zh.pdf` 和 `/files/Xiaoyi-Shi-CV-en.pdf`。版式参考原有中文简历，使用 A4、照片、黑白分节横线，
论文中的本人姓名加粗。中文字体嵌入 PDF，文本可选中、复制，论文标题可点击。
内容增长时自动分页，不裁剪条目。

## 内容维护

- `_data/cv.yml`：姓名、联系方式、教育背景、校园经历，以及网站尚未收录的条目。
  `name_en`、`affiliation_en` 和条目中的 `title_en`、`period_en`、`status_en` 等字段用于英文版；
  教育背景的英文也供网页使用；主要邮箱来自 `_config.yml` 的 `author.email`。
- `_publications/*.md`：自动读取论文标题、日期、会议信息、评级和录用状态。
  作者和发表年份优先读取已有 `bibtex`；无 BibTeX 时可提供 `authors` 列表，
  或使用已有 `citation`。`published: false` 沿用本站约定，显示“已录用，待发表”；
  英文版对应显示 “Accepted, to appear”。其他状态可以用 `cv_status` 和 `cv_status_en` 分别指定。
- `_awards/*.md`：自动读取奖励和日期。中文译名可以在 `cv.yml` 的 `award_overrides` 中配置；
  英文版默认使用集合中的英文标题和地点，可通过 `award_overrides_en` 调整措辞。
- `images/cv-portrait.png`：从提供的模板 PDF 提取的照片。
- `scripts/cv/template.html`：独立的 PDF 排版模板，网页样式不会影响 PDF。

模板中的校园经历、两项奖学金和补充联系方式已保留。当前简历论文仅保留已发表或已录用的条目。
`extra_publications` 中的论文若与网站集合里的标题相同，会自动以集合版本为准。
`publication_categories` 默认只包含会议和期刊，以保持原模板的论文范围。
在论文或奖励的 front matter 中设置 `cv_include: false` 可从 PDF 中排除该条目。
`publication_overrides` 的键是 Markdown 文件名（不含 `.md`），用于设置简短会刊名称。

## 本地生成与验证

建议使用独立环境（Python 3.10 或更高版本）：

```bash
conda create -n cv-pdf python=3.13 pip -y
conda activate cv-pdf
python -m pip install -r scripts/requirements-cv.txt
```

WeasyPrint 需要 Pango 和中文字体。macOS 可运行 `brew install pango`，使用系统的宋体；
若动态库未被找到，在生成命令前设置 `DYLD_FALLBACK_LIBRARY_PATH="$(brew --prefix)/lib"`。
Ubuntu 可安装 `libpango-1.0-0 libpangoft2-1.0-0 fonts-noto-cjk fonts-liberation`。
不同平台的字体会让换行略有区别。

```bash
python scripts/generate_cv.py
python scripts/generate_cv.py --language en
python -m unittest discover -s tests -v
bundle exec jekyll build
```

查看打印用 HTML，或将输出放到其他位置：

```bash
python scripts/generate_cv.py --output /tmp/cv.pdf --html-output /tmp/cv.html
python scripts/generate_cv.py --language en --output /tmp/cv-en.pdf --html-output /tmp/cv-en.html
```

仓库内保留中英文已生成的 PDF，因此普通 Jekyll 本地构建也可预览、下载。
若只使用本地 Jekyll，需要先分别运行两条生成命令更新这两份 PDF。

## GitHub Pages 自动更新

`.github/workflows/pages.yml` 在推送到 `master` 时运行：依赖安全审计 → 测试 → 生成中英文 PDF → 构建 Jekyll → 发布网站。
PDF 和网站在同一次部署中更新，不需要提交机器人生成的 PDF，也不需要额外的令牌。
Pull Request 仅构建和测试，不发布；也可在 Actions 中手动运行。

**首次启用：**在仓库 **Settings → Pages → Build and deployment → Source** 中选择
**GitHub Actions**，再推送代码或手动运行 **Build website and CV**。
如果仓库原先使用从 `master` 分支发布的默认构建，需要完成这一次切换才能使用新的生成步骤。
首次启用完成后无需重复设置，后续推送到 `master` 会自动生成 PDF 并发布网站。

`.github/dependabot.yml` 每周检查 CV 的 Python 依赖并创建升级 PR。
每次构建使用 `pip-audit` 检查 `scripts/requirements-cv.txt` 及其间接依赖；
检测到已知漏洞会停止发布，修复依赖后再部署。

[GitHub 官方自定义 Pages 工作流说明](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
介绍了这种构建和发布方式。
