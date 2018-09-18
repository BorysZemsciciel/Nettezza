#!/usr/bin/env python2
#encoding: UTF-8

# Vitor da Silva and Ana Trindade Winck. 2017.
# Video popularity prediction in data streams based on context-independent features. 
# In Proceedings of the Symposium on Applied Computing (SAC '17). 
# ACM, New York, NY, USA, 95-100. 
# #DOI: https://doi.org/10.1145/3019612.3019638


import sys

sys.dont_write_bytecode = True



import numpy;
import scipy;
import sklearn;

from sklearn.datasets import load_iris;
from vendor.HoeffdingTree.hoeffdingtree import *



iris = load_iris();

data = [row.tolist()+[iris['target'][i]] for i,row in enumerate(iris['data'])]

def getData(iris):
    for row in iris:
        yield row;
        

#demo set
rows = getData(data);


def getArguments(rows):
    for row in rows:
        yield row[:-1];
        
def getTarget(rows):
    for row in rows:
        yield row[-1];
        
        
