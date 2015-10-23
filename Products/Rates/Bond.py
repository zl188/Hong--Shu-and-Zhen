__author__ = 'marcopereira'
import numpy as np
from pandas import DataFrame

class Bond(object):
    def __init__(self, libor, coupon, t_series):
        self.libor=libor
        self.coupon=coupon
        self.t_series = t_series
        self.ntimes=len(self.t_series)
        self.pvAvg=0.0
        self.ntimes = np.shape(self.libor)[0]
        self.ntrajectories = np.shape(self.libor)[1]
        self.cashFlows = DataFrame()
        return
    def PVAvg(self):
        deltaT= np.zeros(self.ntrajectories)
        ones = np.ones(shape=[self.ntrajectories])
        for i in range(1,self.ntimes):
            deltaTrow = ((self.t_series[i]-self.t_series[i-1]).days/365)*ones
            deltaT = np.vstack ((deltaT,deltaTrow) )
        self.cashFlows= self.coupon*deltaT
        principal = ones
        self.cashFlows[self.ntimes-1,:] +=  principal
        pv = self.cashFlows*self.libor
        self.pvAvg = np.average(pv,axis=1)
        return self.pvAvg

    def PV(self):
        deltaT= np.zeros(self.ntrajectories)
        ones = np.ones(shape=[self.ntrajectories])
        for i in range(1,self.ntimes):
            deltaTrow = ((self.t_series[i]-self.t_series[i-1]).days/365)*ones
            deltaT = np.vstack ((deltaT,deltaTrow) )
        self.cashFlows= self.coupon*deltaT
        principal = ones
        self.cashFlows[self.ntimes-1,:] +=  principal
        pv = self.cashFlows*self.libor
        pv = np.sum(pv,axis=0)
        return pv

