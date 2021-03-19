import numpy as np

def NBICoarse():
    days = ['09-03-2021']
    times = [['14-46', '15-06', '15-10', '15-12', '15-14', '15-16']]
    return days, times

def NBIFine():
    days = days = ['15-03-2021'] 
    times = [['12-04','12-07','12-08','12-09','12-10','12-11','12-12','12-13','12-14','12-15','12-16','12-17','12-18','12-20','12-21','12-22','12-23','12-24', '13-41', '13-42', '13-43', '13-44', '13-45', '13-45']]
    return days, times

def ToroidalCoarse():
    days = ['Toroidal-Coarse']
    times = [['18-08','18-09','18-10','18-11','18-12','18-13','18-14']] # toroidal coarse
    return days, times

def PCurrentCoarse():
    days = ['PCurrent-Coarse']
    times = [['18-15','18-16','18-17','18-18','18-19','18-20','18-21']] # pcurrent coarse
    return days, times

def NBarCoarse():
    days = ['NBar-Coarse'] 
    times = [['18-25','18-26','18-27','18-28','18-29','18-30','18-31']] # nbar coarse
    return days, times

def ToroidalNBI():
    days = ['0.07NBI-B0', '0.09NBI-B0', '0.11NBI-B0', '0.13NBI-B0', '0.15NBI-B0', '0.17NBI-B0', '0.19NBI-B0'] 
    times = [['14-50','14-51','11-50','11-51','11-52','11-53','11-54','11-55','11-56'],
             ['14-50','14-51','11-50','11-51','11-52','11-53','11-54','11-55','11-56'],
             ['14-50','14-51','11-50','11-51','11-52','11-53','11-54','11-55','11-56'],
             ['14-50','14-51','11-50','11-51','11-52','11-53','11-54','11-55','11-56'],
             ['14-50','14-51','11-50','11-51','11-52','11-53','11-54','11-55','11-56'],
             ['14-50','14-51','11-50','11-51','11-52','11-53','11-54','11-55','11-56'],
             ['14-50','14-51','11-50','11-51','11-52','11-53','11-54','11-55','11-56']]
    times = [['14-51','11-50','11-51','11-52','11-53','11-54','11-55','11-56'],
             ['14-51','11-50','11-51','11-52','11-53','11-54','11-55','11-56'],
             ['14-51','11-50','11-51','11-52','11-53','11-54','11-55','11-56'],
             ['14-51','11-50','11-51','11-52','11-53','11-54','11-55','11-56'],
             ['14-51','11-50','11-51','11-52','11-53','11-54','11-55','11-56'],
             ['14-51','11-50','11-51','11-52','11-53','11-54','11-55','11-56'],
             ['14-51','11-50','11-51','11-52','11-53','11-54','11-55','11-56']]
    return days, times

def PCurrentFine():
    days = ['0.15NBI-1B0-Ip', '0.19NBI-1.15B0-Ip'] 
    times = [['16-50','16-51','16-52','16-53','16-54','16-55','16-56'],
             ['16-50','16-51','16-52','16-53','16-54','16-55','16-56']]
    return days, times

def NbarFine():
    days = ['0.15NBI-1B0-2.25Ip-Nbar', '0.19NBI-1.15B0-2.5Ip-Nbar'] 
    times = [['09-50','09-51','09-52','09-53','09-54','09-55','09-56'],
             ['09-50','09-51','09-52','09-53','09-54','09-55','09-56']]
    return days, times

def PowerRamps():
    days = ['0.15NBI-1B0-2.25Ip-1.4Nbar-PowerRamps'] 
    times = [['10-50','10-51','10-52','10-53','10-54','10-55']]
    return days, times

def NBISteps():
    days = ['0.19NBI-1.15B0-2.5Ip-1.4Nbar-SteppedPowerRamps']
    days = ['0.19NBI-1.15B0-2.5Ip-2.8Nbar-SteppedPowerRamps']
    days = ['TEST']
    times = [['16-17']]
    times = [['16-45']]
    times = [['14-50']]
    times = [['16-51']]
    return days, times

def NBIFullSteps():
    days = ['1.15B0-2.5Ip-1.4Nbar-SteppedNBI']
    times = [['14-50','14-51','14-52','14-53','14-54']]
    return days, times



def getDaysAndTimes():
    # 1d array of days
    # 2d array, times on 1 axis and days on the other
    days, times = NBISteps()
    
    return days, times

def timeToPath(time, day='09-03-2021', fileName = 'run', fileType = 'mat'):
    path = day+'/'+time+'/'+fileName+'.'+fileType
    return path

def getAllPaths(isSplitDays=False):
    allPaths = []
    days, times = getDaysAndTimes()
    numDays = len(days)
    for i in range(numDays):
        day = days[i]
        dayTimes = times[i]
        dayPaths = []
        for time in dayTimes:
            if isSplitDays:
                dayPaths.append(timeToPath(time, day))
            else:
                allPaths.append(timeToPath(time, day))
        if isSplitDays:
                allPaths.append(dayPaths)
    return allPaths

def getCoarseToroidalField():
    multipliers =  np.array([0.5, 1, 1.5, 2, 2.5, 3, 5])
    defaultReadings = np.array([3.487, 3.489, 3.485, 3.485, 3.482]) # in range 46 to 48
    aveVal = np.mean(defaultReadings)
    valErr = np.std(defaultReadings)
    vals = multipliers*aveVal
    N=len(multipliers)
    errs = np.zeros([N])+valErr
    return vals, errs

def getCoarseToroidalFieldDetails():
    multipliers =  [0.5, 1, 1.5, 2, 2.5, 3, 5]
    defaultReadings = [3.473, 3.483, 3.468,  3.487, 3.496, 3.489, 3.485, 3.485, 3.482, 3.482, 3.504, 3.498] # in range 46 to 48
    times =           [42.87, 44.28, 45.02,     46, 46.38,  46.5,    47,   47.5,  48,  49.37, 49.62, 50.64]
    return times, defaultReadings, multipliers
def getFineToroidalFieldDetails():
    multipliers =  [0.55, 0.7, 0.85, 1, 1.15, 1.3, 1.45, 1.6, 1.75]
    multipliers =  [0.7, 0.85, 1, 1.15, 1.3, 1.45, 1.6, 1.75]
    defaultReadings = [3.473, 3.483, 3.468,  3.487, 3.496, 3.489, 3.485, 3.485, 3.482, 3.482, 3.504, 3.498] # in range 46 to 48
    times =           [42.87, 44.28, 45.02,     46, 46.38,  46.5,    47,   47.5,  48,  49.37, 49.62, 50.64]
    return times, defaultReadings, multipliers

def getNBIRampTimes():
    multipliers =  [1,2,3,4,5,5.5]
    # dummy readings
    defaultReadings = [0.676, 0.427, 0.676, 0.427, 0.676, 0.427, 0.676,  0.427, 0.676,  0.427, 0.676, 0.427] # in range 46 to 48
    times =           [42.87, 44.28, 45.02,    46, 46.38,  46.5,    47,   47.5,    48,  49.37, 49.62, 50.64]
    return times, defaultReadings, multipliers