# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 14:26:32 2016

@author: Andy
"""

import csv
import h5py
import os
import sys
import numpy as np
from scipy.stats import pearsonr
import pandas as pd
import math
'''
extraction hdf5 file part
'''
# test part
#os.chdir('/users/andy/desktop/Project4_data/data')
#os.listdir()
#os.chdir('./A/A/A')
#
#h5py.is_hdf5('TRAAABD128F429CF47.h5')
#tiedl = [h5py.File('TRAAABD128F429CF47.h5','r')] 
#tied = tiedl[0]
#len(list(tied.items()))
#analysis = tied.get('analysis')
#list(analysis.items())
#len(list(analysis.items()))
#bars_c = analysis.get('bars_confidence')
#list(bars_c)
#bars_s = analysis.get('bars_start')
#list(bars_s)
# metadata = tied.get('metadata')
# list(metadata.items())
# similar = metadata.get('artist_terms_freq')
# list(similar)

# extract the path of hd5 file
def _extract_h5(direct,pathslist):
    files = os.listdir(direct)
    for file in files:
        path = direct + '/' + file
        if h5py.is_hdf5(path) :
            pathslist.append(path)
        else :
            if os.path.isdir(path):
                _extract_h5(path,pathslist)

def extract_h5(direct):
    paths = []
    _extract_h5(direct,paths)
    return paths



# # try
# datasets = [list(perAnalysis.get(i)) for i in names]
# with open('/users/andy/desktop/sss.csv','w') as f:
#     csvs = csv.DictWriter(f,fieldnames=names)
#     csvs.writeheader()
#     csvs.writerow({i:j for i,j in zip(names,datasets)})
#     f.close()
# datasets[1]
# # end
def get_dict(paths):
    result = []
    for file in paths:
        songid = os.path.basename(file).replace('.h5','')
        perDict = {'songid':songid}
        h5 = h5py.File(file)
        h5Analysis = h5.get('analysis')
        h5names = [i[0] for i in list(h5Analysis.items())]
        datasets =[h5Analysis.get(i) for i in h5names]
        for key, value in zip(h5names,datasets):
            # lazy evaluation to make memory efficient
            perDict[key] = value
        result.append(perDict)
    return result 


# find the type
#base = h5dict[10]
#typenames = [type(base.get(i)) for i in names]
#print(typenames)
#isinstance(base.get('bars_confidence'),typenames[0])
'''
get codebook part
'''
songwordpath = '/users/andy/desktop/songs.csv'
songword = pd.read_csv(songwordpath,header = 0 , index_col = 0)

'''
calculation part
'''
# calculate similarity


def _cal_similar(baseline,new,names,letgo):
    pearsondict = {}
    for i in names:
        if i not in letgo:
            usedlen = len(new[i])
            trimedbase = baseline[i][0:usedlen]
            pp = pearsonr(np.array(new[i]),trimedbase)[0]
            if math.isnan(pp):
                pp = 0
            pearsondict[i] = pp
    return pearsondict

def get_quan_song(h5dict,names,letgo,baseline):
    final = {}
    for song in h5dict:
        per = _cal_similar(baseline,song,names,letgo)
        per2 = []
        for i in names:
            if i not in letgo:
                per2.append(per[i])
        final[song['songid']] = per2
    return final



def find_similar(final,new,baseline,names,letgo):
    newq = _cal_similar(baseline,new,names,letgo)
    similarlist = {}
    for i in final.keys():
        newvect = []
        for t in names:
            if t not in letgo:
                newvect.append(newq[t])
        newvalue = pearsonr(final[i],newvect)[0]
        if math.isnan(newvalue):
            newvalue = 0
        similarlist[i] = newvalue
    return similarlist

'''
interface
'''
files = extract_h5('/users/andy/desktop/Project4_data/data')
h5dict = get_dict(files)
## get name first
per = h5py.File(files[0])
perAnalysis = per.get('analysis')
names = [i[0] for i in list(perAnalysis.items())]
# choose the baseline first
# get the length information
len_dict = {}
for i in h5dict:
    for j in names:
        if j not in len_dict.keys():
            len_dict[j] = []
        else:
            len_dict[j].append(len(i[j]))
for i in len_dict.keys():
    print(i,' : ', max(len_dict[i]))   
# take care of 'segments_pitches', 'segments_timbre','songs'
letgo = ['segments_pitches','segments_timbre','songs']   
# baseline data set up:
np.random.seed(100)
base_dict = {}
for i in names:
    if i not in letgo:
        base_dict[i] = sorted(np.random.random_sample(size=(max(len_dict[i]),)))

final = get_quan_song(h5dict,names,letgo,base_dict)
'''
testing part
'''
# extract new file
newfilepath = '/users/andy/desktop/TestSongFile100'
newfilepaths = extract_h5(newfilepath)
newfile = get_dict(newfilepaths)
similars = []
for i in range(len(newfile)):          
    similars.append((newfile[i]['songid'],find_similar(final,newfile[i],base_dict,names,letgo)))

fieldname = [i['songid'] for i in h5dict]

with open('/users/andy/desktop/similarity.csv','w') as f:
    csvdict = csv.DictWriter(f,fieldnames=['songid',*fieldname])
    csvdict.writeheader()
    for i in similars:
        perdictrow={}
        perdictrow['songid'] = i[0]
        for j in i[1].keys():
            if math.isnan(i[1][j]):
                perdictrow[j] = 0
            else:
                perdictrow[j] = i[1][j]
        csvdict.writerow(perdictrow)
    f.close()