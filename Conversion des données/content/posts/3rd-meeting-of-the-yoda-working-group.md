---
title: 3rd meeting of the Yoda working group
slug: 3rd-meeting-of-the-yoda-working-group
date: '2021-11-23 19:56:00'
lastmod: '2024-09-08 19:58:36'
draft: false
author: Yves.Ledru
categories:
- An2021
- EvenementGPL
- YODA
tags: []
summary: null
---

The 3rd meeting of the Yoda working group was held remotely on

**Monday, 29th of November, 2021,**~~14:00-16:00 CET~~**  14:30-16:30 CET.**

The program comprised three talks:

  * **14:30-15:00:**_"Sustaining Performance While Reducing Energy Consumption: A Control Theory Approach"_  
**by[Sophie Cerf](https://sites.google.com/view/sophiecerf/)**, Spirals (Inria Lille – Nord Europe)  
**Presentation:** [slides](https://gitlab.inria.fr/yoda/public/-/blob/def4f21117083cd8c652a4611745675ef611b124/20211129/slides/Sophie_Cerf.pdf), [video](https://gitlab.inria.fr/yoda/public/-/raw/def4f21117083cd8c652a4611745675ef611b124/20211129/videos/zoom_0.mp4)**Abstract:** Production high-performance computing systems continue to grow in complexity and size. As applications struggle to make use of increasingly heterogeneous compute nodes, maintaining high efficiency (performance per watt) for the whole platform becomes a challenge. Alongside the growing complexity of scientific workloads, this extreme heterogeneity is also an opportunity: as applications dynamically undergo variations in workload, due to phases or data/compute movement between devices, one can dynamically adjust power across compute elements to save energy without impacting performance. With an aim toward an autonomous and dynamic power management strategy for current and future HPC architectures, this paper explores the use of control theory for the design of a dynamic power regulation method. Structured as a feedback loop, our approach—which is novel in computing resource management—consists of periodically monitoring application progress and choosing at runtime a suitable power cap for processors. Thanks to a preliminary offline identification process, we derive a model of the dynamics of the system and a proportional-integral (PI) controller. We evaluate our approach on top of an existing resource management framework, the Argo Node Resource Manager, deployed on several clusters of Grid’5000, using a standard memory-bound HPC benchmark.
  * **15:00-16:00:**___"Data Science-Driven Methods for Sustainable and Failure Tolerant Edge Systems"_  
**Invited talk by[Ivona Brandić](https://www.ec.tuwien.ac.at/~ivona/)**, Institute of Information Systems Engineering (TU Wien)  
**Presentation:** [slides](https://gitlab.inria.fr/yoda/public/-/blob/def4f21117083cd8c652a4611745675ef611b124/20211129/slides/Yoda_Talk_Brandic.pdf), video recording available on [demand](mailto:yoda-request@groupes.renater.fr?subject=Recording%20of%20the%20talk%20by%20I.%20Brandi%C4%8D)**Abstract:** Nowadays we experience a paradigm shift in our society, where every item around us is becoming a computer facilitating life-changing applications like self-driving cars, telemedicine, precision agriculture or virtual reality. On one hand, for the execution of such resource-demanding applications, we need powerful IT facilities. On the other hand, the requirements often include latencies below 100 ms or even below 10 ms – what is called “tactile internet”. To facilitate low latency, computation has to be placed in the vicinity of the end-users by utilizing the concept of Edge Computing. In this talk, we explain the challenges of Edge systems in combination with tactile internet. We discuss the recent problems of geographically distributed machine learning applications and novel approaches to balance competing priorities like the energy efficiency and the staleness of the machine learning models.
  * **16:00-16:30:**___"Reasoning about Reconfigurations of Distributed Systems"_  
**by[Radu Iosif](http://nts.imag.fr/index.php/Radu_Iosif)**, MOHYTOS (VERIMAG)  
**Presentation:** [slides](https://gitlab.inria.fr/yoda/public/-/blob/def4f21117083cd8c652a4611745675ef611b124/20211129/slides/Radu_Iosif.pdf), [video](https://gitlab.inria.fr/yoda/public/-/raw/master/20211129/videos/zoom_2.mp4)**Abstract:** This paper presents a Hoare-style calculus for formal reasoning about reconfiguration programs of distributed systems. Such programs create and delete components and/or interactions (connectors) while the system components change state according to their internal behaviour. Our proof calculus uses a resource logic, in the spirit of Separation Logic, to give local specifications of reconfiguration actions. Moreover, distributed systems with an unbounded number of components are described using inductively defined predicates. The correctness of reconfiguration programs relies on havoc invariants, which are assertions about the ongoing interactions in a part of the system that is not affected by the structural change caused by the  
reconfiguration. We present a proof system for such invariants in an assume/rely-guarantee style. We illustrate the feasibility of our approach by proving the correctness of real-life distributed systems with reconfigurable (self-adjustable) tree architectures.


