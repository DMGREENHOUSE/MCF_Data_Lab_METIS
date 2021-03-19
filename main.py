# -*- coding: utf-8 -*-
from helperFunctions import matlabToArray, averageInRange, getNBIPower
from fileFunctions import timeToPath, getDaysAndTimes, getAllPaths, getCoarseToroidalFieldDetails, getFineToroidalFieldDetails, getNBIRampTimes
from analysisFunctions import getTimeSpansForAnalysis
from DataRunResult import DataRunResult
from plotFunctions import singleXYErrorPlot
from matplotlib import pyplot as plt
"""
For a single analysis of a data run (given in the path) and a single variable
Returns the average value (and associated error) for the time spans provided
    in getTimeSpansForAnalysis.
"""
def VarDataRunAnalysis(DRResults, SweepVarName, InterestVarName, isPlotYet=True, label=None):
    
    timeSpans = getTimeSpansForAnalysis()
    numTimeSpans = len(timeSpans)
    
    numDRResults = len(DRResults)
    
    SweepVars=[[None]*numDRResults for _ in range(numTimeSpans)]
    SweepVarErrs=[[None]*numDRResults for _ in range(numTimeSpans)]
    
    InterestVars=[[None]*numDRResults for _ in range(numTimeSpans)]
    InterestVarErrs=[[None]*numDRResults for _ in range(numTimeSpans)]
    
    SweepVarLabel = None
    InterestVarLabel = None
    for i in range(numDRResults):
        DRResult = DRResults[i]
        
        InterestVar = DRResult.findVar(InterestVarName)
        SweepVar = DRResult.findVar(SweepVarName)
        # needs a catch here for if the variable has not yet been found
        for j in range(numTimeSpans):
            SweepVars[j][i] = SweepVar.aves[j]
            SweepVarErrs[j][i] = SweepVar.errs[j]
            InterestVars[j][i] = InterestVar.aves[j]
            InterestVarErrs[j][i] = InterestVar.errs[j]
        
        SweepVarLabel = SweepVar.description
        InterestVarLabel = InterestVar.description
    colors=['darkcyan', 'black', 'darkgreen', 'brickred', 'navy']
    
    for i in range(numTimeSpans):
        legendLabel = 'Time Span Considered: {}'.format(str(timeSpans[i]))
        if label != None:
            legendLabel=label
        singleXYErrorPlot(SweepVars[i], InterestVars[i],
                          SweepVarErrs[i], InterestVarErrs[i],
                          xlabel=SweepVarLabel, ylabel=InterestVarLabel,
                          color=colors[i],
                          legend=legendLabel,
                          xscale='linear',
                          isSort=True, isShow=False)
    if isPlotYet:
        plt.show()
        

#triple product = # electron temp electron density energy confinement time
# 3-4 1e 22
#Lawson in kev - 3*10**21
# use electron temperature
def DRSweepAnalysis(paths):
    numDataRuns = len(paths)
    DRResults = [None]*numDataRuns
    for i in range(numDataRuns):
        DRResults[i] = DataRunResult(paths[i])
    return DRResults
#'ne0', 'te0', 'taue', 'betap'
def addNewVarToSweep(theseDRResults, newVarName, newVarDescription, subsec='zer0d',  isPlot=False,
                     isHardCode=False, hardCodeBaseArray=[], hardCodeTimeArray=[], hardCodeMultipliers=[]):
    i=0
    for DRResult in theseDRResults:
        if isHardCode:
            multiplier=hardCodeMultipliers[i]
            i+=1
            DRResult.addVar(newVarName, newVarDescription, subsec, isPlot,
                        isHardCode=isHardCode, hardCodeBaseArray=hardCodeBaseArray,
                        hardCodeTimeArray=hardCodeTimeArray, hardCodeMultiplier=multiplier)
        else:
            DRResult.addVar(newVarName, newVarDescription, subsec, isPlot)
    return theseDRResults


def addB0(theseDRResults):
    # Add b0
    B0Times, B0Readings, B0multipliers = getFineToroidalFieldDetails()
    
    DRResults = addNewVarToSweep(theseDRResults, 'B0', r'Toroidal Magnetic Field at R0 [$T$]', 'userDef', False,
                     isHardCode=True, hardCodeBaseArray=B0Readings, hardCodeTimeArray=B0Times,
                     hardCodeMultipliers=B0multipliers)
    return DRResults

def addNBIRampTime(theseDRResults):
    # Add b0
    NBIRMTimes, NBIRMReadings, NBIRMmultipliers = getNBIRampTimes()
    
    DRResults = addNewVarToSweep(theseDRResults, 'NBIRT', r'Normalised NBI Ramp Time [s]', 'userDef', False,
                     isHardCode=True, hardCodeBaseArray=NBIRMReadings, hardCodeTimeArray=NBIRMTimes,
                     hardCodeMultipliers=NBIRMmultipliers)
    return DRResults


def investigateVars(DRResults,
                    varsToInvestigate = ['tip', 'modeh', 'ne0', 'te0', 'ni0', 'tibord', 'taue', 'betap', 'triple'],
                    sweepVar = 'B0',
                    isPlotAtEnd=True,
                    label=None):
    for varToInvestigate in varsToInvestigate:
        VarDataRunAnalysis(DRResults, sweepVar, varToInvestigate, isPlotYet=isPlotAtEnd, label=label)

def DRMultiSweepAnalysis():
    daysPaths = getAllPaths(isSplitDays=True)
    numMultis = len(daysPaths)
    labels = ['NBI=2.33MW, BT=3.45T, Ip=3.4A']#, 'NBI=2.95MW, BT=4T, Ip=3.75A'] 
    for i in range(numMultis):
        thisDayPaths = daysPaths[i]
        DRResults = DRSweepAnalysis(thisDayPaths)
        #DRResults = addB0(DRResults)
        DRResults = addNBIRampTime(DRResults)
        
        investigateVars(DRResults, varsToInvestigate=['modeh'], sweepVar='NBIRT', isPlotAtEnd=False,
                        label=labels[i])
    plt.show()

DRResults = DRSweepAnalysis(getAllPaths())
VarDataRunAnalysis(DRResults, 'pnbi', 'triple')
#DRMultiSweepAnalysis()

"""
DRResults = DRSweepAnalysis(getAllPaths())
DRResults = addB0(DRResults)

varsToInvestigate = ['tip', 'modeh', 'ne0', 'te0', 'ni0', 'tibord', 'taue', 'betap', 'triple']
varsToInvestigate = ['modeh', 'triple']
for varToInvestigate in varsToInvestigate:
    VarDataRunAnalysis(DRResults, 'B0', varToInvestigate)
"""