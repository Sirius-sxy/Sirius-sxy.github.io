---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

<div class="cv-downloads">
  <p class="cv-downloads__label">中文简历 <span>Chinese CV · PDF</span></p>
  <div class="cv-downloads__actions">
    <a class="btn btn--primary" href="{{ '/files/Xiaoyi-Shi-CV-zh.pdf' | relative_url }}" target="_blank" rel="noopener">
      <i class="fas fa-file-pdf" aria-hidden="true"></i> 预览 PDF / View
    </a>
    <a class="btn" href="{{ '/files/Xiaoyi-Shi-CV-zh.pdf' | relative_url }}" download="Xiaoyi-Shi-CV-zh.pdf">
      <i class="fas fa-download" aria-hidden="true"></i> 下载 PDF / Download
    </a>
  </div>
</div>

<h2 class="cv-section">Education</h2>
<ul class="cv-edu-list">
  {% for item in site.data.cv.education %}
  <li>
    <span class="cv-period">{{ item.period_en | escape }}</span>
    <span class="cv-degree">{{ item.degree_en | escape }}</span>, {{ item.institution_en | escape }}
  </li>
  {% endfor %}
</ul>

<h2 class="cv-section">Publications</h2>
{% assign sorted_pubs = site.publications | sort: "date" | reverse %}
{% for post in sorted_pubs %}
  {% include archive-single-cv.html %}
{% endfor %}

<h2 class="cv-section">Awards</h2>
{% assign sorted_awards = site.awards | sort: "date" | reverse %}
{% for post in sorted_awards %}
  {% include archive-single-cv.html %}
{% endfor %}
