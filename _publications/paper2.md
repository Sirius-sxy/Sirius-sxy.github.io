---
title: 'P4runpro: Enabling Runtime Programmability for RMT Programmable Switches'
collection: publications
category: conferences
permalink: /publication/paper2
date: 2024-08-04
venue: 'Proceedings of the ACM SIGCOMM 2024 Conference'
opensource: true
repogiturl: 'https://github.com/P4runpro/P4runpro'
paperurl: 'https://dl.acm.org/doi/abs/10.1145/3651890.3672230'
citation: "Yifan Yang, Lin He, Jiasheng Zhou, Xiaoyi Shi, Jiamin Cao, and Ying Liu. 2024. P4runpro: Enabling Runtime Programmability for RMT Programmable Switches. In Proceedings of the ACM SIGCOMM 2024 Conference (ACM SIGCOMM '24). Association for Computing Machinery, New York, NY, USA, 921–937.
https://doi.org/10.1145/3651890.3672230"
---

Programmable switches have revolutionized network operations by enabling the flexible customization of packet processing logic using language like P4. However, changing the programs running on the switch requires disturbing traffic and suspending other unrelated programs. In this paper, we present P4runpro, enabling runtime data plane updates with dynamic resource allocation. The P4runpro data plane abstracts hardware resources and defines dynamically reconfigurable atomic operations that form packet processing logic. P4runpro provides runtime programming interfaces called P4runpro primitives for the operator to write high-level programs. We have designed the P4runpro compiler to automatically and consistently link the P4runpro programs to the running data plane. We implement our prototype on a Tofino switch. We implement 15 example runtime programs using P4runpro to demonstrate its generality and expressiveness. Our evaluation results show that compared to the state-of-the-art, P4runpro can respond within hundreds of milliseconds, achieve an average of \\(60\%\\) to \\(80\%\\) dynamic resource utilization, concurrently run \\(\approx0.6K\\) to \\(\approx2.8K\\) programs, and introduce lower overhead. Our case studies illustrate the benefit of runtime programming and prove the same functionality between P4runpro and conventional P4 programs.