__author__ = 'marcopereira'
from pandas import DataFrame
import numpy as np
import pandas as pd

class MC_Vasicek_Sim(object):
    def __init__(self, datelist,r0,sigmaR,muR,alphaR, simNumber,t_step):
    #SDE parameters - Vasicek SDE
        self.sigmaR = sigmaR
        self.muR = muR
        self.alphaR = alphaR
        self.simNumber = simNumber
        self.t_step = t_step
        self.r0 = r0
    #internal representation of times series - integer multiples of t_step
        self.datelist = datelist
    #creation of a fine grid for Monte Carlo integration
        #Create fine date grid for SDE integration
        minDay = min(datelist)
        maxDay = max(datelist)
        self.datelistlong = pd.date_range(minDay, maxDay).tolist()
        self.datelistlong = [x.date() for x in self.datelistlong]
        self.ntimes = len(self.datelistlong)
        self.libor=[]
        self.smallLibor = []

    def getLibor(self):
        rd = np.random.standard_normal((self.ntimes,self.simNumber))   # array of numbers for the number of samples
        r = np.zeros(np.shape(rd))
        nrows = np.shape(rd)[0]
        sigmaDT = self.sigmaR* np.sqrt(self.t_step)
    #calculate r(t)
        r[1,:] = self.r0+r[1,:]
        for i in np.arange(2,nrows):
            r[i,:] = r[i-1,:]+ self.alphaR*(self.muR-r[i-1,:])*self.t_step + sigmaDT*rd[i,:]
    #calculate integral(r(s)ds)
        integralR = r.cumsum(axis=0)*self.t_step
    #calculate Libor
        self.libor = np.exp(-integralR)
        return self.libor

    def getSmallLibor(self):
        #calculate indexes
        ind = self.return_indices1_of_a(self.datelistlong, self.datelist)
        self.smallLibor = np.vstack(self.libor[ind,:])
        return self.smallLibor

#####################################################################################
    def saveMeExcel(self,libor,liborName,fileName):
        df = DataFrame(libor)
        df.to_excel(fileName, sheet_name=liborName, index=False)

#####################################################################################
    def return_indices1_of_a(self, a, b):
        b_set = set(b)
        ind = [i for i, v in enumerate(a) if v in b_set]
        return ind
#####################################################################################
    def return_indices2_of_a(self, a, b):
        index=[]
        for item in a:
            index.append(np.bisect.bisect(b,item))
        return np.unique(index).tolist()

