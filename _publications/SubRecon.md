---
title: "SubRecon: Efficient Internet‑wide IPv6 Subnet Discovery and Its Applications"
collection: publications
category: conferences
permalink: /publication/SubRecon
date: 2025-9-22
venue: 'The 33rd IEEE International Conference on Network Protocols'
published: true
paperurl: 'https://ieeexplore.ieee.org/abstract/document/11192454'
citation: "Jiasheng Zhou, Ying Liu, Lin He, Yifan Yang, Xiaoyi Shi, Daguo Cheng, Chentian Wei, Yun Fan, and Guanglei Song. 2025. SubRecon: Efficient Internet‑wide IPv6 Subnet Discovery and Its Applications. In Proceedings of the 33rd IEEE International Conference on Network Protocols (ICNP 2025). Seoul, South Korea."
---

# Abstract
The vastness of the IPv6 address space has led to the common practice of allocating prefixes to end users rather than individual addresses. Users can assign these prefixes as a single subnet or divide them into multiple subnets for different purposes. Allocation strategies vary significantly in terms of prefix granularity, and identifying the actual granularity of subnet assignments is crucial for improving measurement efficiency, accuracy, and for better IPv6 network management. However, no existing method can discover IPv6 subnets at an Internet-wide scale.

To this end, we propose SubRecon, an Internet-wide IPv6 subnet discovery system. SubRecon consists of two key phases: subnet delimitation and target expansion. In the subnet delimitation phase, we perform a systematic scan across the entire IPv6 address space without relying on any existing seed dataset. This phase adopts a top-down approach, probing prefixes from the shortest to the longest in a hierarchical manner. At each level, we recursively refine prefixes and discard sub-prefixes that do not meet the convergence condition. This pruning strategy eliminates redundant probes in unallocated regions, significantly reducing the search space and improving probing efficiency. To further improve coverage, the target expansion phase leverages the active address dataset as an auxiliary input. It identifies active addresses not covered by previously discovered subnets, expands them into new candidate target prefixes, and performs another round of subnet delimitation. This helps enhance the completeness and coverage of the final discovered subnet set. Experimental results show that SubRecon discovers 8,381,974 IPv6 subnets across 14,147 autonomous systems, and the resulting subnet list can serve as high-quality input for topology discovery. Additionally, during the subnet discovery process, SubRecon identifies a large number of last-hop router interfaces, discovering approximately 10 million more than the current state-of-the-art methods.