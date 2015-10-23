__author__ = 'marcopereira'
import numpy as np
import datetime
from  MonteCarloSimulators.Vasicek import vasicekMCSim
from Products.Rates import Bond, BondRisky

#CashFlow Dates
t_series = np.round(np.arange(0,1.001,0.25)*365)
base = datetime.datetime.today()
datelist = [base + datetime.timedelta(days=x) for x in t_series]
datelist = [x.date() for x in datelist]

#SDE parameter
t_step = 1.0/365
r0 = 0.08
sigmaR = 0.05
muR = 0.05
alphaR=3.0
simNumber=1000

#SDE parameter
t_step = 1.0/365
lambda0 = 0.08
sigmaLambda = 0.05
muLambda = 0.05
alphaLambda=3.0
simNumber=1000

#Bond parameters
coupon = 0.08
R = 0.4

#Monte Carlo trajectories creation - R
t1 = datetime.datetime.now()
myVasicekLibor = vasicekMCSim.MC_Vasicek_Sim(datelist, r0,sigmaR, muR, alphaR, simNumber,t_step)
longLibor = myVasicekLibor.getLibor()
libor = myVasicekLibor.getSmallLibor()
myVasicekLibor.saveMeExcel(libor,"libor","../DataResults/LiborCurve/libor.xlsx")

#Monte Carlo trajectories creation - Q
myVasicekQ = vasicekMCSim.MC_Vasicek_Sim(datelist, lambda0,sigmaLambda, muLambda, alphaLambda, simNumber,t_step)
longQ = myVasicekQ.getLibor()
Q = myVasicekQ.getSmallLibor()
myVasicekQ.saveMeExcel(Q,"Q","../DataResults/SurvivalCurve/Q.xlsx")


#Bond Pricing
myBond = Bond.Bond(libor,coupon, datelist)
myRiskyBond = BondRisky.BondRisky(libor,Q,coupon,datelist,R)
print('Bond Cashflows PV = ', str(myBond.PVAvg()))
print('Bond PV = ', str(myBond.PVAvg().sum()))
print('Bond PV Variance =' , str(myBond.PV().var()))


print('RiskyBond Cashflows PV = ', str(myRiskyBond.PVAvg()))
print('RiskyBond PV = ', str(myRiskyBond.PVAvg().sum()))
print('RiskyBond PV Variance =' , str(myRiskyBond.PV().var()))

t2 = datetime.datetime.now()
print(str(t2-t1))

