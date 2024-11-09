---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

Education
======
* Ph.D in Institute of Network Science and Cyberspace, Tsinghua University, 2029(expected)
* B.S. in Department of Automation, Tsinghua University, 2020-2024

Publications
======
  <ul>{% for post in site.publications reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
