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

## Pre-requisites

The demo requires OpenSSL library to be installed in the system. 

## How to run the demo

The attack works in two phases - template building and template matching

### Template Building

1. Run the shell script `script_template.sh` to build the templates. In our experiments, we consider the most significant bit (msb) to be 1 and build templates for 6 msbs. Therefore total number of templates built is 32 (keeping msb as 1).
2. Once the above script ends, run `generate_template.py` to create the template dataset.

### Template Matching

