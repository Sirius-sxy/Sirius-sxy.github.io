---
title: "Miresga: Achieving High-Performance and Reliable Layer-7 Load Balancing with Programmable Switches"
collection: publications
category: manuscripts
permalink: /publication/Miresga-TC
date: 2026-07-22
venue: 'IEEE Transactions on Computers'
opensource: true
published: true
paperurl: 'https://ieeexplore.ieee.org/document/11617301'
repogiturl: 'https://github.com/THUNAME/Miresga'
repozenodourl: 'https://zenodo.org/records/14792352'
repodoiurl: 'https://doi.org/10.5281/zenodo.14792351'
repolicense: 'AGPL3'
citation: "Xiaoyi Shi, Ying Liu, Lin He, Yifan Yang, Jiasheng Zhou, Rongbang Wu, and Jinlong E. Miresga: Achieving High-Performance and Reliable Layer-7 Load Balancing with Programmable Switches. IEEE Transactions on Computers, 2026. (Early Access) https://doi.org/10.1109/TC.2026.3715854"
ccf: "A"
thcpl: "A"
apa: "Shi, X., Liu, Y., He, L., Yang, Y., Zhou, J., Wu, R., & E, J. (2026). Miresga: Achieving high-performance and reliable layer-7 load balancing with programmable switches. IEEE Transactions on Computers. Advance online publication. https://doi.org/10.1109/TC.2026.3715854"
bibtex: |
  @article{shi2026miresga,
    title={Miresga: Achieving High-Performance and Reliable Layer-7 Load Balancing with Programmable Switches},
    author={Shi, Xiaoyi and Liu, Ying and He, Lin and Yang, Yifan and Zhou, Jiasheng and Wu, Rongbang and E, Jinlong},
    journal={IEEE Transactions on Computers},
    year={2026},
    pages={1--14},
    doi={10.1109/TC.2026.3715854},
    note={Early Access}
  }
---
# Abstract

As online cloud services continue to scale, ensuring both performance and reliability in layer-7 load balancing has become increasingly critical. Programmable switches offer Tbps-level packet processing with limited flexibility, making them promising yet constrained candidates for accelerating layer-7 load balancing. We present Miresga, a hybrid layer-7 load balancing framework that achieves high performance and reliability through software–hardware co-design. Miresga offloads elephant flows to programmable switches for line-rate forwarding, while front-end servers handle protocol parsing and scheduling, ensuring flexibility. To address the limited memory of the programmable switch, Miresga introduces an eBPF-based back-end agent to manage sequence synchronization. Miresga also employs a distributed RDMA-based state synchronization mechanism for failure tolerance and dynamic traffic migration. Our prototype on a 3.2 Tbps Intel Tofino switch demonstrates up to 3.9× throughput improvement and 60% latency reduction over optimized software baselines, while maintaining stable throughput during front-end server failures and recoveries.

This is the extended journal version of our conference paper published at The Web Conference 2025 (WWW '25): [Miresga: Accelerating Layer-7 Load Balancing with Programmable Switches](/publication/Miresga). The code repository is shared between both versions: [github.com/THUNAME/Miresga](https://github.com/THUNAME/Miresga).
