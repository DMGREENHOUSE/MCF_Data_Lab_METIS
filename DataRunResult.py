import scipy.io
from plotFunctions import singleXYPlot
import numpy as np
from DataRunResultVar import DataRunResultVar

class DataRunResult:
    def __init__(self, file_path, isPrintDetails=False, isPlotDefaultVars=False):
        self.data_set = self.pathToDataSet(file_path)
        if isPrintDetails:
            self.list_subsections()
            self.list_indexes()
            self.list_indexes('profil0d')
        # extract time
        self.times0DArray = self.get_variable('temps')
        self.timesProfileArray = self.get_variable('temps', subsection='profil0d')
        # extract neutral beam power
        pnbi0D = self.createNBIAnalysis('pnbi', isPlotDefaultVars)
        pnbi0D.addDescription(r'NBI Power [$MW$]')
        # store those that have been found
        self.foundVars = [[pnbi0D],
                          ['pnbi']]
        # Useful vars
        usefulVars = [['ne0',    r'Central Electron Density Estimation [$m^{-3}$]', 'zerod'],
                      ['te0',    r'Central Electron Temperature Estimation [$eV$]', 'zerod'],
                      ['ni0',    r'Central Ion Density Estimation [$m^{-3}$]',      'zerod'],
                      ['tibord', r'Edge Ion Temperature Estimation [$eV$]',         'zerod'],
                      ['taue',   r'Energy Confinement Time [$s$]',                  'zerod'],
                      ['betap',  r'Poloidal Normalised Plasma Beta',            'zerod'],
                      ['modeh',  r'Confinement Mode: (0=Low, 1=High)',              'zerod'],
                      ['ip',     r'Plasma Current [$A$]',                           'zerod'],
                      ['nbar',   r'Line Averaged Electron Density [$m^{-3}$]',      'zerod'],
                      ['q0',     r'Central Safety Factor Estimation',               'zerod'],
                      ['tip',    r'Profile Ion Temperature Estimation [$eV$]',      'profil0d']]
        for i in range(len(usefulVars)):
            self.addVar(usefulVars[i][0], usefulVars[i][1], usefulVars[i][2], isPlotDefaultVars)
        
        # triple product
        tripleProductArray = self.findTripleProduct()
        self.createNewVar(tripleProductArray, 'triple', r'Triple Product (using central electron values) [$keVsm^{-3}$]',isPlotDefaultVars)
    
    def findTripleProduct(self):
        # central electron density x central electron temperature x energy confinement time
        ne0Arr = self.findVar('ne0').vars
        te0Arr = self.findVar('te0').vars
        te0Arr/=1000
        taueArr = self.findVar('taue').vars
        tripleProductArray = ne0Arr*te0Arr*taueArr
        return tripleProductArray
    
    def createNewVar(self, newVarArray, varName, varDescrip, isPlotDefaultVars):
        subsection= 'userDef'
        varObj = DataRunResultVar(self.times0DArray, newVarArray, varName, subsection, isPlot=isPlotDefaultVars)
        varObj.addDescription(varDescrip)
        self.foundVars[0].append(varObj)
        self.foundVars[1].append(varName)
    
    def createVarAnalysis(self, name, subsec, isPlot):
        varValArray = self.get_variable(name, subsection=subsec)
        timeArr = None
        if subsec == 'zerod':
            timeArr = self.times0DArray
        elif subsec == 'profil0d':
            timeArr = self.timesProfileArray
        else:
            print('ERROR: subsection not yet accounted for. Subsection provided is {}'.format(subsec))
                
        return DataRunResultVar(timeArr, varValArray, name, subsec, isPlot=isPlot)
    
    def createHardCodeVarAnalysis(self, name, baseArray, multiplier, timeArr, isPlot):
        subsec = 'userDef'
        baseArray = np.array(baseArray)
        varValArray = baseArray*multiplier
        return DataRunResultVar(timeArr, varValArray, name, subsec, isPlot=isPlot)
                
    def createNBIAnalysis(self, name, isPlot):
        varValArray = np.array(self.getNBIPower())/1000000
        return DataRunResultVar(self.times0DArray, varValArray, name, 'zerod', isPlot=isPlot)
    
    def pathToDataSet(self, path):
        data_set = scipy.io.loadmat(path)
        return data_set
    
    def list_subsections(self):
        print("subsections available:")
        print(self.data_set['post'].dtype)

    def list_indexes(self, subsection='zerod'):
        print("indexes in subsection " + subsection + ":")
        print(self.data_set['post'][subsection][0][0].dtype)

    def createUnknownLen2DArr(self, raw2DArr, isComplex):
        multi_var_arr = []
        i=0
        isBeforeLim = True
        if isComplex:
            while isBeforeLim:
                try:
                    multi_var_arr.append([complex(x[i]) for x in raw2DArr])
                    i+=1
                except:
                     isBeforeLim = False
        else:
            while isBeforeLim:
                try:
                    multi_var_arr.append([float(x[i]) for x in raw2DArr])
                    i+=1
                except:
                     isBeforeLim = False
                
        return multi_var_arr

    def get_variable(self, varName, subsection='zerod', isComplex=False):
        raw_var_arr = self.data_set['post'][subsection][0][0][varName][0][0]
        var_arr = None
        if subsection == 'zerod':
            if isComplex:
                var_arr = [complex(x[0]) for x in raw_var_arr]
            else:
                var_arr = [float(x[0]) for x in raw_var_arr]
        elif subsection == 'profil0d':
            var_arr = self.createUnknownLen2DArr(raw_var_arr, isComplex)
            
        else:
            print('ERROR: subsection not yet accounted for. Subsection provided is {}'.format(subsection))
        return var_arr
    
    def getNBIPower(self, subsection='zerod'):
        name = 'pnbi'
        NBIPower_Complex = self.get_variable(name, subsection, isComplex=True)
        NBIPower_ComplexSum = [(np.real(x)+np.imag(x)) for x in NBIPower_Complex]
        return NBIPower_ComplexSum
    
    def findVar(self, targetVarName):
        targetIndex = None
        for i in range(len(self.foundVars[1])):
            varName = self.foundVars[1][i]
            if varName == targetVarName:
                targetIndex = i
        if targetIndex == None:
            print('ERROR: no var of this name ({}) has been found. Please try addVar first'.format(targetVarName))
        else:
            return self.foundVars[0][targetIndex]
    
    def addVar(self, varName, varDescription, subsec, isPlot, isHardCode=False,
               hardCodeBaseArray=[], hardCodeTimeArray=[],hardCodeMultiplier=0):
        thisVar = None
        if isHardCode:
            thisVar = self.createHardCodeVarAnalysis(varName, hardCodeBaseArray,
                                                     hardCodeMultiplier, hardCodeTimeArray, isPlot)
        else:
            thisVar = self.createVarAnalysis(varName, subsec, isPlot)
        thisVar.addDescription(varDescription)
        self.foundVars[0].append(thisVar)
        self.foundVars[1].append(varName)
        

    
    