# RASSLE

This repository contains the source codes and scripts to demonstrate RASSLE in action.

## System Specifications

The attack utilizes the deadline scheduler to achieve synchronization between the spy and victim. The demo have been tested on a system which has the following specifications:
- Processor -  Intel Xeon CPU E5-2609 v4 (Broadwell)
- Operating System - Red Hat Enterprise Linux Server 7.7 (kernel 3.10.0-1062.9.1.el7.x86_64)
- Deadline scheduler parameters – 
  - sched-runtime -> 3600
  - sched-deadline -> 3700
  - sched-period -> 7200
- Return Address Stack (RAS) size - 16
- OpenSSL version – 1.1.1g

