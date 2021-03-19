# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 13:59:01 2021

@author: dmg530
"""
import csv
import scipy.io
import numpy as np
from matplotlib import pyplot as plt

def csvToArray(file_path):
    results = []
    with open(file_path) as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
        for row in reader: # each row is a list
            results.append(row)
    return results


def list_subsections(full_dataset):
    print("subsections (I'm using zerod by default):")
    print(full_dataset['post'].dtype)


def list_indexes(full_dataset, subsection='zerod'):
    print("indexes in subsection " + subsection + ":")
    print(full_dataset['post']['zerod'][0][0].dtype)


def get_variable(full_dataset, index, subsection='zerod'):
    a = full_dataset['post'][subsection][0][0][index][0][0]
    a = [float(x[0]) for x in a]
    return a

def plotArray(xs, ys, var):
    plt.plot(xs, ys, label='METIS-Temps corrected')
    plt.legend()
    plt.xlim([40,58])
    plt.ylabel(var)
    plt.xlabel('Time [s]')
    plt.show()
    
def getAssumedTimeArray(ys):
    t_start_time = 40.5536 #s
    t_end_time = 56.4926 #s
    N = len(ys)
    ts = np.linspace(t_start_time, t_end_time, N)
    return ts
    
def getAssumedTimeArrayNonLin(ys):
    t_start_time = 40.5536 #s
    t_mid_time = 48.4 #s
    t_end_time = 56.4926 #s
    N = len(ys)
    N_two_thirds = int(0.66*N)
    N_remainder = N-N_two_thirds
    ts_start = np.linspace(t_start_time, t_mid_time, N_two_thirds)
    t_step = ts_start[1]-ts_start[0]
    ts_end = np.linspace(t_mid_time+t_step, t_end_time, N_remainder)
    ts = np.concatenate((ts_start, ts_end))
    return ts

def getTimeArray(data_set, subsection='zerod'):
    name = 'temps'
    return get_variable(data_set, name, subsection)

def pathToDataSet(path):
    data_set = scipy.io.loadmat(path)
    return data_set

def getNBIPower(data_set, subsection='zerod'):
    name = 'pnbi'
    NBIPower = get_variable(data_set, name, subsection)
    return NBIPower

def matlabToArray(file_path, varName, isPlot=False, isShowAll=False, subsection='zerod'):
    data_set = pathToDataSet(file_path)
    if isShowAll:
        list_subsections(data_set)
        list_indexes(data_set)
    ys=get_variable(data_set, varName, subsection)
    ts = getTimeArray(data_set, subsection)
    
    if isPlot:
        plotArray(ts, ys, varName)
    return ts, ys

def findNearestIndex(val, array):
    nextIndex = None
    nearestIndex = None
    for i in range(len(array)):
        if array[i]>val:
            nextIndex = i
            break
    lowDiff = array[nextIndex-1] - val
    highDiff = array[nextIndex] - val
    if lowDiff<highDiff:
        nearestIndex = nextIndex-1
    else:
        nearestIndex = nextIndex
    return nearestIndex

def averageInRange(ts, ys, timeSpan = [46,48]):
    lowIndex = findNearestIndex(timeSpan[0], ts)
    highIndex = findNearestIndex(timeSpan[1], ts)
    ysInRange = ys[lowIndex:highIndex]
    mean = np.mean(ysInRange)
    error = np.std(ysInRange)
    return mean, error
    
def sort2Lists(list1, list2):
    sortedList1, sortedList2 = (list(t) for t in zip(*sorted(zip(list1, list2))))
    return sortedList1, sortedList2 
def sort3Lists(list1, list2, list3):
    sortedList1, sortedList2, sortedList3 = (list(t) for t in zip(*sorted(zip(list1, list2, list3))))
    return sortedList1, sortedList2, sortedList3
def sort4Lists(list1, list2, list3, list4):
    sortedList1, sortedList2, sortedList3, sortedList4 = (list(t) for t in zip(*sorted(zip(list1, list2, list3, list4))))
    return sortedList1, sortedList2, sortedList3, sortedList4
