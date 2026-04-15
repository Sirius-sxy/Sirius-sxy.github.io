---
title: "L7LB: High Performance Layer-7 Load Balancing on Heterogeneous Programmable Platforms"
collection: publications
category: conferences
permalink: /publication/L7LB
date: 2023-05-20
venue: 'IEEE INFOCOM 2023-IEEE Conference on Computer Communications Workshops (INFOCOM WKSHPS)'
#slidesurl: #'http://academicpages.github.io/files/slides1.pdf'
opensource: true
published: true
paperurl: 'https://sirius-sxy.github.io/files/L7LB_poster.pdf'
repogiturl: 'https://github.com/Tsinghua-NSLab/L7LB'
citation: 'Xiaoyi Shi, Yifan Li, Chengjun Jia, Xiaohe Hu and Jun Li, "L7LB: High Performance Layer-7 Load Balancing on Heterogeneous Programmable Platforms," IEEE INFOCOM 2023 - IEEE Conference on Computer Communications Workshops (INFOCOM WKSHPS), Hoboken, NJ, USA, 2023, pp. 1-2, doi: 10.1109/INFOCOMWKSHPS57453.2023.10225882.'
apa: "Shi, X., Li, Y., Jia, C., Hu, X., & Li, J. (2023). L7LB: High Performance Layer-7 Load Balancing on Heterogeneous Programmable Platforms. In IEEE INFOCOM 2023 - IEEE Conference on Computer Communications Workshops (INFOCOM WKSHPS) (pp. 1-2). IEEE. https://doi.org/10.1109/INFOCOMWKSHPS57453.2023.10225882"
bibtex: |
  @inproceedings{shi2023l7lb,
    title={L7LB: High Performance Layer-7 Load Balancing on Heterogeneous Programmable Platforms},
    author={Shi, Xiaoyi and Li, Yifan and Jia, Chengjun and Hu, Xiaohe and Li, Jun},
    booktitle={IEEE INFOCOM 2023 - IEEE Conference on Computer Communications Workshops (INFOCOM WKSHPS)},
    pages={1--2},
    year={2023},
    organization={IEEE},
    doi={10.1109/INFOCOMWKSHPS57453.2023.10225882}
  }
---

# Abstract

Layer-7 load balancing is an essential pillar in modern enterprise infrastructure. It is inefficient to scale software layer-7 load balancing which requires hundreds of servers to meet the large-scale service requirements of 1 Tbps throughput and 1M concurrent requests. This paper presents L7LB with a novel fast path and slow path co-design architecture running on a heterogeneous programmable server-switch. L7LB is efficient by offloading most packets' forwarding onto the Tbps bandwidth switch chip, with few CPU cores processing application connections. The preliminary prototype demonstrates the layer-7 load balancing functionality and shows that L7LB can meet the large-scale service requirements.