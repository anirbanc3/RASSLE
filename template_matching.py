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
import csv


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


numberOfFiles = 196; keys = 32;

template = np.load('rassle_timing_dataset.npy')
mean_temp = np.mean(template, axis=1)
median_temp = np.median(template, axis=1)

key_bin_pair = ['100000', '100001', '100010', '100011', '100100', '100101', '100110', '100111',
                '101000', '101001', '101010', '101011', '101100', '101101', '101110', '101111',
                '110000', '110001', '110010', '110011', '110100', '110101', '110110', '110111',
                '111000', '111001', '111010', '111011', '111100', '111101', '111110', '111111']


first_temp = []; second_temp = []; third_temp = []

for j in range(keys):
    median_first = []
    median_second = []
    median_third = []
    
    one_bit_template = template[j]

    sm = np.argsort(one_bit_template, axis=0)
    new_temp = np.take_along_axis(one_bit_template, sm, axis=0)
    
    for i in range(6):
        median_first.append(np.median(new_temp[0:3333,i]))
        median_second.append(np.median(new_temp[3333:6666,i]))
        median_third.append(np.median(new_temp[6666:,i]))
        
    first_temp.append(median_first)
    second_temp.append(median_second)
    third_temp.append(median_third)
        

mont_start_time = openfile('RASSLE/file_mont_ladder.txt', 'count')
with open('sample_nonces.txt', 'r') as f:
    file = f.readlines() 
    
    
nonces = list(map(lambda each:each.strip("\n"), file))

#mont_start_time = 4335541507554953

sample_timing = [] 
for i in range(500):
    filename = 'RASSLE/filetiming_tst_'+str(i + 100)+'.txt'
    raw_timing = openfile(filename, 'timing')
    for index, item in enumerate(raw_timing):
        if (item[0] > mont_start_time[i + 100]):
#            print(item[0])
            sample_timing.append([raw_timing[index - 1][2], raw_timing[index][2], raw_timing[index + 1][2], raw_timing[index + 2][2], raw_timing[index + 3][2], raw_timing[index + 4][2], raw_timing[index + 5][2]])
            break

rank_holder = []; key_holder = []
for i in range(500):
    key = nonces[i + 100]    
    keybyte = key[0:2]
    keybyte_in_bin = str("{0:08b}".format(int(keybyte, 16)) )
    key_six_msb = keybyte_in_bin[0:6]
    for index, item in enumerate(key_bin_pair):
        if (item == key_six_msb):
            correct_index  = index

    outlist = []
    for j in range(keys):
        fileX = []
        for k in range(6):
            dist_first = abs(sample_timing[i][k] - first_temp[j][k])
            dist_second = abs(sample_timing[i][k] - second_temp[j][k])
            dist_third = abs(sample_timing[i][k] - third_temp[j][k])
            if (dist_first <= dist_second and dist_first <= dist_third):
                fileX.append(first_temp[j][k])
            elif (dist_second <= dist_first and dist_second <= dist_third):
                fileX.append(second_temp[j][k])
            elif (dist_third <= dist_second and dist_third <= dist_first):
                fileX.append(third_temp[j][k])
        fileY = sample_timing[i][0:6]
#        p,t = stats.pearsonr(fileX, fileY)
        p = np.sum((np.array(fileX)-np.array(fileY))**2)
        outlist.append((j, p))


#    outlist = sorted(outlist,key=itemgetter(1),  reverse=True)
    outlist = sorted(outlist,key=itemgetter(1))
    key_holder.append(outlist[0:5])
    
 
  
   
    for index, item in enumerate(outlist):
        if (item[0] ==  correct_index):
            print(index, item)
            rank_holder.append(index)
       
    
count = len([i for i in rank_holder if i < 5]) 
print(count)
            
nonce_candidates = [[0 for n in range(5)] for m in range(500)]
for i, keys in enumerate(key_holder):
    for j, item in enumerate(keys):
        nonce_candidates[i][j] = key_bin_pair[item[0]]


with open("nonce_bits.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(nonce_candidates)  
        
