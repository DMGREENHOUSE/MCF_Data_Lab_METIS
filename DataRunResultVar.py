from analysisFunctions import getTimeSpansForAnalysis
from plotFunctions import singleXYPlot
from helperFunctions import averageInRange
import numpy as np

class DataRunResultVar:
    def __init__(self, ts, var_vals, varName, subsec, isPlot=False):
        self.times = ts # array of the times where var_vals are known
        self.vars = np.array(var_vals) # array of the var values in time
        self.varName = varName
        self.subsection = subsec
        self.analysedTimeSpans = getTimeSpansForAnalysis()
        self.aves, self.errs = self.findAveragesAndErrors()
        self.description = ''
        if isPlot:
            self.plotVarTime()
            
    def addDescription(self, description):
        self.description = description
        
    def getTimeAndVarArr(self, index):
        varArr = None
        timeArr = None
        if self.subsection=='zerod':
            varArr = self.vars
            timeArr = self.times
        elif self.subsection=='userDef':
            varArr = self.vars
            timeArr = self.times
        elif self.subsection=='profil0d':
            varArr = self.vars[index]
            timeArr = self.times[0]
        else:
            print('ERROR: subsection not yet accounted for. Subsection provided is {}'.format( self.subsection))
        return timeArr, varArr
    
    def findAveragesAndErrors(self, index=0):
        timeArr, varArr = self.getTimeAndVarArr(index)
        numTimeSpans = len(self.analysedTimeSpans)
        aves = [None]*numTimeSpans
        errs = [None]*numTimeSpans
        for i in range(numTimeSpans):
            timeSpan = self.analysedTimeSpans[i]
            aves[i], errs[i] = averageInRange(timeArr, varArr, timeSpan)
        return aves, errs
    
    def plotVarTime(self, index=0):
        timeArr, varArr = self.getTimeAndVarArr(index)
        varName = self.varName
        if self.subsection=='profil0d':
            varName = self.varName + '; Profile Index = {}'.format(index)
        singleXYPlot(timeArr,varArr,
                     xlabel='Time [s]', ylabel=varName,
                     legend='METIS-Temps corrected', xlim=[40,58])
    
    
        