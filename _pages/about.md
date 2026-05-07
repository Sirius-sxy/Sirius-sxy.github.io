---
permalink: /
title: "Xiaoyi Shi"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

I am currently a 2nd-year Ph.D student at the [Institute of Network Science and Cyberspace](https://www.insc.tsinghua.edu.cn/) at [Tsinghua University](https://www.tsinghua.edu.cn/), advised by [Prof. Ying Liu](https://www.insc.tsinghua.edu.cn/info/1157/2456.htm). I received my bachelor degree at the [Department of Automation](https://www.au.tsinghua.edu.cn/), Tsinghua University. My current research topics include **programmable networks** and **large language models**.

<h2 class="home-section-title">Selected Publications</h2>

<div class="featured-pubs">
  {%- comment -%}
    Show the top CCF-A papers, most-recent-first. If fewer than 3 CCF-A
    entries exist, fall back to the most-recent published papers so the
    section never looks empty.
  {%- endcomment -%}
  {% assign ccf_a_pubs = site.publications | where: "ccf", "A" | sort: "date" | reverse %}
  {% if ccf_a_pubs.size >= 1 %}
    {% for post in ccf_a_pubs limit: 4 %}
      {% include archive-single.html %}
    {% endfor %}
  {% else %}
    {% assign recent_pubs = site.publications | sort: "date" | reverse %}
    {% for post in recent_pubs limit: 4 %}
      {% include archive-single.html %}
    {% endfor %}
  {% endif %}
</div>

<a class="featured-pubs__more" href="{{ site.baseurl }}/publications/">View all publications</a>
