#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 11:56:15 2020

@author: anirban727
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from operator import itemgetter
import re


def preprocess(file):
    file_out = []
    file = list(map(lambda each:each.strip("\n"), file))
    for item in file:
        row = list(map(int, re.split(r'\t+', item)))
        file_out.append(row)
    return file_out

def parse_filecount(file):
    file_out = list(map(int, list(map(lambda each:each.strip("\n"), file))))
    return file_out

def openfile(filename, flag):
    with open(filename, 'r') as f:
        file = f.readlines()
    if (flag == 'timing'):
        return preprocess(file)
    else:
        return parse_filecount(file)

if __name__ == "__main__":
    numberOfFiles = 10000; keys = 32;
    

    dataset = []

    filename_mont = 'file_mont_ladder.txt'
    filecount = openfile(filename_mont, 'mont')
    for i in range(keys):
        filetiming = []; 
        for j in range(numberOfFiles):
            filename_timing = 'RASSLE/filetiming_'+str(128+(i * 4))+'_'+str(j+1)+'.txt'
            raw_timing = openfile(filename_timing, 'timing')
            mont_start_time = filecount[i*numberOfFiles +  j]
            for index, item in enumerate(raw_timing):
                if (item[0] > mont_start_time):
                    try:
                        filetiming.append([raw_timing[index - 1][2], raw_timing[index][2], raw_timing[index + 1][2], raw_timing[index + 2][2], raw_timing[index + 3][2], raw_timing[index + 4][2], raw_timing[index + 5][2]])
                    except:
                        print(index)
                    break
            
            
            
        print(i)
        dataset.append(filetiming)
    
    for k in dataset:
        if (len(k) == 10000):
            del k[len(k) - 1] 
        if (len(k) == 9999):
            del k[len(k) - 2] 
            
    np.save('rassle_timing_dataset.npy', np.array(dataset))
    



