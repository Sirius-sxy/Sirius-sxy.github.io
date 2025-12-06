---
title: "TGW: Operating an Efficient and Resilient Cloud Gateway at Scale"
collection: publications
category: conferences
permalink: /publication/TGW
published: true
date: 2025-7-7 
venue: '2025 USENIX Annual Technical Conference'
paperurl: 'https://www.usenix.org/system/files/atc25-yang-yifan.pdf'
citation: "Yifan Yang, Lin He, Jiasheng Zhou, Xiaoyi Shi, Yichi Xu, Shicheng Wang, Jinlong E, Ying Liu, Junwei Zhang, Zhuang Yuan, and Hengyang Xu, TGW: Operating an Efficient and Resilient Cloud Gateway at Scale. In Proceedings of the 2025 USENIX Annual Technical Conference (ATC '25), Boston, MA, USA, July 2025."
---
Cooperation with Tencent.

# Abstract
Large-scale cloud data centers have become a critical Internet infrastructure. As the cloud entrance, today’s cloud gateways have integrated multiple functions such as elastic public access and load balancing to cope with the rapid growth of services and requirements. To meet the demands of large-scale clouds for efficient packet forwarding, scalable state management, and high resilience, we design, deploy, and operate Tencent Gateway (TGW), an efficient and resilient cloud gateway at scale.

Compared to other large cloud providers that primarily offer services like search, e-commerce, or short-form video, the "killer services" of Tencent Cloud are online gaming and live streaming, which come with much stricter requirements for latency, jitter, and packet loss. From a technological perspective, TGW is highly decoupled and modular, with core components focused on efficient forwarding planes, a scalable state migration mechanism, a resilient failure recovery mechanism, and a failure detection and localization system. In terms of engineering, TGW has been operating in large-scale, real-world industrial environments for eight years, during which we have gained extensive insights and experience.

We evaluate TGW both in testbed and real-world scenarios. In our testbed, TGW's single node achieves \\(2.9\times\\) the forwarding capacity of prior systems. Between clusters, states and traffic can be migrated in 4 s without packet loss. In our real-world environment, TGW handles tens of Tbps of traffic, with a worst-case packet drop rate ranging from \\(10^{-7}\\) to \\(10^{-4}\\), while balancing traffic across clusters. Additionally, TGW can quickly migrate states and traffic and recover from failures without tenant awareness, guided by our failure localization system, achieving 100% availability for years.