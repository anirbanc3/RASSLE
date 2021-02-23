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
            filename_timing = 'filetiming_'+str(128+(i * 4))+'_'+str(j+1)+'.txt'
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
    
    minimum = numberOfFiles
  
    for k in dataset:
        if (len(k) < minimum):
            minimum = len(k)
            
    pruned_dataset = [[0 for j in range(minimum)] for i in range(keys)]
    for i, item in enumerate(dataset):
        for j, val in enumerate(item):
            if (j < minimum):
                pruned_dataset[i][j] = val
                
    print(minimum)
            
    np.save('rassle_timing_dataset.npy', np.array(pruned_dataset))
    



