---
title: "Miresga: Accelerating Layer-7 Load Balancing with Programmable Switches"
collection: publications
category: conferences
permalink: /publication/paper4
date: 2025-4-28 
venue: 'Proceedings of the ACM Web Conference 2025'
#slidesurl: #'http://academicpages.github.io/files/slides1.pdf'
#paperurl: 'https://sirius-sxy.github.io/files/L7LB_poster.pdf'
citation: "Xiaoyi Shi, Lin He, Jiasheng Zhou, Yifan Yang, and Ying Liu. 2025. Miresga: Accelerating Layer-7 Load Balancing with Programmable Switches. In Proceedings of the ACM Web Conference 2025 (WWW '25), April 28–May 2, 2025, Sydney, NSW, Australia. ACM, New York, NY, USA"
---

As online cloud services expand rapidly, layer-7 load balancing has become indispensable for maintaining service availability and performance. The emergence of programmable switches with both high performance and a certain degree of flexibility has made it possible to apply programmable switches to load balancing. Nevertheless, the limited memory capacity and the relatively sluggish speed of table entry insertion and deletion of programmable switches have severely constrained their performance. 
  
  To this end, we introduce Miresga, a hybrid and high-performance layer-7 load balancing system by co-designing hardware and software. 
  The core idea of Miresga is to maximize the utilization of hardware and software resources by rationally partitioning the layer-7 load balancing task, thereby improving performance. To achieve this, Miresga offloads the elephant flows, which account for the majority of traffic, to programmable switches that excel at packet processing, and Miresga utilizes general-purpose servers with stronger computational capabilities to parse application layer protocols and apply load balancing rules. To alleviate memory pressure on the programmable switch, Miresga employs a back-end agent to handle memory-intensive tasks, working in conjunction with the programmable switch to complete the offloaded tasks. This design leverages the performance advantages of the programmable switch while avoiding bottlenecks caused by its limited memory and table insertion speed.
  We implement the Miresga prototype with a 3.2 Tbps Intel Tofino switch and general-purpose servers. The evaluation results show that Miresga achieves \\(3.9\times\\) throughput and \\(0.4\times\\) latency compared to software load balancing solutions. Compared to the state-of-the-art design employing programmable switches, Miresga achieves almost the same throughput and latency for delivering large objects and \\(5.0\times\\) throughput and \\(0.2\times\\) latency when transmitting small objects.