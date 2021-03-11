def getDayAndTimes():
    # 1d array of days
    days = ['09-03-2021'] 
    # 2d array, times on 1 axis and days on the other
    times = [['14-46', '15-06', '15-10', '15-12', '15-14', '15-16']]
    return days, times

def timeToPath(time, day='09-03-2021', fileName = 'run', fileType = 'mat'):
    path = day+'/'+time+'/'+fileName+'.'+fileType
    return path

def getAllPaths():
    allPaths = []
    days, times = getDayAndTimes()
    for day in days:
        for time in times:
            allPaths.append(timeToPath(time, day))
    return allPaths