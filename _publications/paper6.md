---
title: "Lightning in the Dark: Uncovering Global IPv6 Router Interfaces and Their Security Implications"
collection: publications
category: conferences
permalink: /publication/paper6
date: 2025-9-22
venue: 'The 33rd IEEE International Conference on Network Protocols'
published: true
paperurl: 'https://ieeexplore.ieee.org/abstract/document/11192454'
citation: "J. Zhou, Y. Liu, L. He, X. Shi, Y. Yang, C. Wei, D. Cheng, W. Gong, & J. Yang. 2025. Lightning in the Dark: Uncovering Global IPv6 Router Interfaces and Their Security Implications. In Proceedings of the 33rd IEEE International Conference on Network Protocols (ICNP 2025). Seoul, South Korea."
---
# Abstract

The IPv6 routing infrastructure is an important part of the modern Internet, and the collection of its interface addresses is greatly significant in network security, performance optimization, and measurement analysis. However, existing methods suffer from two major problems: the lack of flexibility in budget allocation across probing rounds and the absence of a dynamic hop limit adjustment mechanism based on feedback. These problems lead to the low hit rate and inefficiency of existing methods for discovering router interfaces, which seriously hinders the comprehensive knowledge of IPv6 routing infrastructure.

To this end, we propose Helixir, a feedback-based, high hit-rate, and efficient IPv6 router interface discovery system. Helixir’s core design includes a dynamic budget allocation mechanism across probing rounds, an inter-prefix budget allocation strategy that adequately trades off exploration and exploitation, and a hop limit selection method based on Thompson sampling. Real-world experiments show that with a 100M budget, Helixir achieves a hit rate 3.64× that of state-of-the-art methods on the BGP prefixes dataset, and Helixir successfully discovers over 31 million IPv6 router interface addresses in total within half an hour. In addition, a systematic security analysis of the discovered router interfaces shows that many devices open sensitive ports and expose hundreds of potential CVE vulnerabilities, highlighting the security risks in the IPv6 network.