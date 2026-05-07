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
  <li>
    <span class="cv-period">2024 – 2029 (expected)</span>
    <span class="cv-degree">Ph.D.</span>, Institute of Network Science and Cyberspace, Tsinghua University
  </li>
  <li>
    <span class="cv-period">2020 – 2024</span>
    <span class="cv-degree">B.S.</span>, Department of Automation, Tsinghua University
  </li>
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
