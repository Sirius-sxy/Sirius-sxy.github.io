---
title: "SwitchTAD: Defending Deep Learning-Based Website Fingerprinting Attacks with Programmable Switches"
collection: publications
category: manuscripts
permalink: /publication/SwitchTAD
date: 2025-12-6
venue: 'Elsevier Computer Networks'
published: true
paperurl: 'https://www.sciencedirect.com/science/article/abs/pii/S1389128625008874'
citation: "Jiasheng Zhou, Lin He, Xiaoyi Shi, Yifan Yang, Jinlong E, Ying Liu, SwitchTAD: Defending deep learning-based website fingerprinting attacks with programmable switches, Computer Networks, Volume 275, 2026, 111921, ISSN 1389-1286, https://doi.org/10.1016/j.comnet.2025.111921."
---
# Abstract

Traffic analysis poses a serious threat to the privacy of users, particularly through website fingerprinting attacks. To mitigate these attacks, existing defense methods typically modify traffic patterns by configuring defense at the endpoint. However, these defense methods degrade user experience due to complex configurations and tight client-server cooperation. Furthermore, their static and coarse-grained defense rules are unable to adjust the perturbation decision flexibly at a fine-grained level according to the dynamic changes in individual packet sequences. These limitations greatly affect the effectiveness of defense. To this end, we propose SwitchTAD, a website fingerprinting defense system based on programmable switches. SwitchTAD offers a general and effective solution that protects all users behind the switch without requiring individual configurations. It also leverages the programmability of switches to process packets at a fine granularity, enabling the application of different defense policies tailored to the characteristics of each traffic flow. Specifically, we design a data plane friendly Recurrent Neural Network (RNN) architecture for generating defense policies without the intervention of the control plane. As packets arrive, the data plane uses the output of the RNN to determine whether to add dummy packets on a per-packet basis, ensuring robust defense while minimizing overhead. Experimental results show that SwitchTAD significantly reduces the accuracy of state-of-the-art website fingerprinting attacks while maintaining overall high performance.