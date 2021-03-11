# -*- coding: utf-8 -*-
from helperFunctions import matlabToArray, averageInRange, getNBIPower
from fileFunctions import timeToPath, getDayAndTimes, getAllPaths
from analysisFunctions import getTimeSpansForAnalysis

day = '09-03-2021'
times = ['14-46', '15-06', '15-10', '15-12', '15-14', '15-16']
time = times[0]
file = 'run'
fileType = 'mat'

days, times = getDayAndTimes()
path = timeToPath(times[0][0])

var = 'ne0'
#section = 'zerod', 'profile0d'
ts, ys = matlabToArray(path, var, isPlot=True)
print(averageInRange(ts, ys))

"""
For a single analysis of a data run (given in the path) and a single variable
Returns the average value (and associated error) for the time spans provided
    in getTimeSpansForAnalysis.
"""
def VarDataRunAnalysis(var, path):
    
    ts, ys = matlabToArray(path, var, isPlot=True)
    timeSpans = getTimeSpansForAnalysis()
    numTimeSpans = len(timeSpans)
    aves = [None]*numTimeSpans
    errs = [None]*numTimeSpans
    for i in range(numTimeSpans):
        timeSpan = timeSpans[i]
        aves[i], errs[i] = averageInRange(ts, ys, timeSpan)
    return aves, errs
#triple product = # electron temp electron density energy confinement time
def VarSweepAnalysis(var, path):
    paths = getAllPaths()
    numDataRuns = len(paths)
    for i in range(numDataRuns):
        VarDataRunAnalysis(var, paths[i])

#VarAnalysis('taue', timeToPath(times[0][0]))
"""
def timeToPath(time, day='09-03-2021'):
    
def (var):
    NBIPower = 
"""
"""
var = 'te0'
ts, ys = matlabToArray(path, var,  isPlot=True)
print(averageInRange(ts, ys))
var = 'taue'
ts, ys = matlabToArray(path, var,  isPlot=True)
print(averageInRange(ts, ys))
var = 'betap'
ts, ys = matlabToArray(path, var,  isPlot=True)
print(averageInRange(ts, ys))
"""