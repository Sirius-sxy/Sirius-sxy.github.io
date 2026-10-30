---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

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

{% assign cv_languages = "English,Chinese" | split: "," %}
{% for language in cv_languages %}
{% if language == "English" %}{% assign language_code = "en" %}{% else %}{% assign language_code = "zh" %}{% endif %}
{% assign cv_filename = "Xiaoyi-Shi-CV-" | append: language_code | append: ".pdf" %}
{% assign cv_path = "/files/" | append: cv_filename %}
<div class="cv-downloads">
  <p class="cv-downloads__label">{{ language }} CV <span>PDF</span></p>
  <div class="cv-downloads__actions">
    <a class="btn btn--primary" href="{{ cv_path | relative_url }}" target="_blank" rel="noopener" aria-label="View {{ language }} CV (PDF)">
      <i class="fas fa-file-pdf" aria-hidden="true"></i> View PDF
    </a>
    <a class="btn" href="{{ cv_path | relative_url }}" download="{{ cv_filename }}" aria-label="Download {{ language }} CV (PDF)">
      <i class="fas fa-download" aria-hidden="true"></i> Download PDF
    </a>
  </div>
</div>
{% endfor %}
