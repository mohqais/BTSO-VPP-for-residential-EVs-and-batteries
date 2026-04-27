"""
Created on Thu Oct  3 17:19:49 2024
@author: mqais
"""

import pandas as pd
import pandapower as pp
import pandapower.networks as pn
import random as rn
import numpy as np
# Make sure that all algorithms are in the same file location with Main.py
from BGWO import bGWO
from BTSO import TSO_algor
from BDE import bde
from bga import BGA
from BQA import qao_binary_optimization
from BPSO import binary_pso
from BQIEV import quantum_inspired_evolutionary_algorithm
from BSimuAnn import binary_simulated_annealing

# firstly load the datasets
Loads=pd.read_csv(r'Bus Loads.csv',index_col=[0])
Q_load=pd.read_csv(r'Bus Q Loads.csv',index_col=[0])
PV_power=pd.read_csv(r'PV data.csv',index_col=[0])
Bat_data=pd.read_csv(r'Batteries data.csv',index_col=[0])
EV_data=pd.read_csv(r'EV data.csv',index_col=[0])
Available=pd.read_csv(r'EV Available.csv',index_col=[0])
socB_init=Bat_data.loc['soc_init']

def battery(Pd,soc):
     Capacity=Bat_data.loc['Capacity'].to_numpy()
     Charge_power=Bat_data.loc['Max_charge'].to_numpy()
     Discharge_power=Bat_data.loc['Max_discharge'].to_numpy()
     
     ch_eff=0.95
     del_t=15/60
     Pd=Pd*1000
     Pch=np.zeros(5)
     Pdch=np.zeros(5)
     D_ind=Pd<0 # charge if demand power is negative and discharge if positive
     Pch=(np.absolute(Pd)+(Charge_power-np.absolute(Pd))*(np.absolute(Pd)>Charge_power))*(D_ind)*(soc<1)
     soc=soc+Pch*del_t*ch_eff/Capacity
     Pch=np.add(Pch,(soc>1)*(1-soc)*Capacity/(del_t*ch_eff)) #reverse the surplus
     soc=soc+(1-soc)*(soc>1)

     Pdch=(np.absolute(Pd)+(Discharge_power-np.absolute(Pd))*(np.absolute(Pd)>Discharge_power))*(1-D_ind)*(soc>0.1)
     soc=soc-Pdch*del_t/(Capacity*ch_eff)
     Pdch=np.subtract(Pdch,(soc<0.1)*(0.1-soc)*Capacity*ch_eff/del_t)
     soc=soc+(0.1-soc)*(soc<0.1)
     P_out=(Pch-Pdch)
     return P_out/1000,soc
def EV(x_state,available,soc,delt_trip):
     Capacity=EV_data.loc['Capacity'].astype('float64').to_numpy()    
     distance=EV_data.loc['Distance'].astype('float64').to_numpy()
     drive_E=EV_data.loc['consume'].astype('float64').to_numpy()
     A_ind=available==1
     soc_ind=soc<1
     ch_eff=0.95
     dch_eff=0.8
     del_t=15/60
     del_mi=distance/delt_trip
     Pch=np.zeros(5)
     
     Pch=6.6*ch_eff*x_state*A_ind*soc_ind

     soc=soc+Pch*del_t/Capacity
     Pch=np.add(Pch,(soc>1)*(1-soc)*Capacity*ch_eff/del_t) #reverse the surplus
     soc=soc+(1-soc)*(soc>1)

     soc=soc-drive_E*del_mi*(1-A_ind)*(soc>0.1)/(Capacity*dch_eff)
     return Pch/1000,soc

class objective():
    def __init__(self,net,socB,socEV,available,delt_trip,Pd):
        self.net=net
        self.socB=socB
        self.socEV=socEV
        self.available=available
        self.delt_trip=delt_trip
        self.Pd=Pd
        
    def run(self,x):
        Pev,soc_EV=EV(x, self.available, self.socEV, self.delt_trip)
        Pd=self.Pd+Pev
        Pbat,soc_B=battery(Pd, self.socB)
        self.net.storage.p_mw[self.net.storage['name'].isin([f'EV{bus}_{h}' for bus in range(1,33) for h in range(31)])]=Pev
        self.net.storage.p_mw[self.net.storage['name'].isin([f'B{bus}_{h}' for bus in range(1,33) for h in range(31)])]=Pbat
        pp.runpp(self.net,numba=False)
        V_min=self.net.res_bus.vm_pu.min()
        #obj=(x*self.available).sum()+np.square(x/soc_EV).sum()
        if V_min>=0.94:
            obj=((1-(soc_EV))*x*self.available).sum()
        else:
            obj=0.0001 
        obj=1/(obj)
        return obj
#load the IEEE 33 bus system from Pandapower
net=pn.case33bw()
net.load.drop(net.load.index,axis=0,inplace=True)
net.line.drop([32,33,34,35,36],axis=0,inplace=True)
net.line['max_i_ka']=[(249-i*6)/1000 for i in range(32)]

for bus in range(1,33):
    for h in range(31):
        
        pp.create_load(net, bus=bus, p_mw=0,name=f'H{bus}_{h}')
        pp.create_storage(net, bus=bus, p_mw=0, max_e_mwh=1,name=f'B{bus}_{h}')
        pp.create_storage(net, bus=bus, p_mw=0, max_e_mwh=1,name=f'EV{bus}_{h}')
        pp.create_sgen(net, bus=bus, p_mw=0,name=f'PV{bus}_{h}')

soc_EV=EV_data.loc['soc_init'].astype('float64').to_numpy()
soc_B=Bat_data.loc['soc_init'].to_numpy()
volt=pd.DataFrame()
loading_line=pd.DataFrame()
Bat_out=pd.DataFrame()
EV_out=pd.DataFrame()
EV_soc_store=pd.DataFrame()
B_soc_store=pd.DataFrame()
PV_tot_out=pd.DataFrame()
grid_power=[]
load2=pd.DataFrame()
qload2=pd.DataFrame()
angle=pd.DataFrame()
voltage=pd.DataFrame()
bus_results=pd.DataFrame()
fitness=[]
EV_chargedNumber=pd.DataFrame()

import time
time_elapse=[]
for t in range(Loads.shape[0]):
    net.load.p_mw=Loads.iloc[t].to_numpy()     # it is important to convert series to numpy
    net.load.q_mvar=Q_load.iloc[t].to_numpy()
    net.sgen.p_mw=PV_power.iloc[t].to_numpy()
    Pd1=Loads.iloc[t].to_numpy()-PV_power.iloc[t].to_numpy()
    if t>=40 and t<=70:
        Pch=Bat_data.loc['Max_charge'].to_numpy()/1000
        Pd1=-Pch*0.7+(Pd1-Pch*0.7)*(np.absolute(Pd1)>=0.7*Pch)
    if any(Available.iloc[t]==1) and any(soc_EV!=1):
        problem=objective(net,soc_B,soc_EV,Available.iloc[t].to_numpy(),(Available==0).sum().to_numpy(),Pd1)
        start_time = time.time()
        
        # select the required algorithm for optimization
        algor_select='BTSO'
        
        if algor_select =='BTSO':
            name='TSO'
            x,fit=TSO_algor(20, Available.shape[1],10, problem.run)
        elif algor_select=='BGWO':
            Algo=bGWO(problem.run,Available.shape[1],20,10)
            Algo.opt() #GWO
            x,fit=Algo.gBest_X,Algo.gBest_curve
        elif algor_select=='BGA':
            Algo=BGA(pop_shape=(5, Available.shape[1]), method=problem.run,max_round=10,maximum=False)
            x,fit=Algo.run() #BGA
        elif algor_select=='BPSO':
            Algo=binary_pso(problem.run,20,Available.shape[1],10,w=0.3,c1=1.,c2=0.5)
            x,fit=Algo[0],Algo[1] #BPSO
        elif algor_select=='BDE':
            x,fit= bde(problem.run, Available.shape[1], 20, 10, 0.8,0.8)
        elif algor_select=='BQA':
            x, fit=qao_binary_optimization(problem.run, Available.shape[1],0.1, 10.0, 10, n_samples=20, seed=42)
        elif algor_select=='BSA':
            x, fit = binary_simulated_annealing(problem.run,Available.shape[1], 200, 100, 0.55)
        elif algor_select=='BQDE':
            x, fit =quantum_inspired_evolutionary_algorithm(problem.run, Available.shape[1],20,10,np.pi/6)

        fitness.append(fit)
        time_elapse.append(time.time()-start_time)
    else:
        x=Available.iloc[t].to_numpy()
        name='None'
    
    Pev,soc_EV=EV(x, Available.iloc[t].to_numpy(), soc_EV, (Available==0).sum().to_numpy())
    Pd=Pd1+Pev
    Pbat,soc_B=battery(Pd, soc_B)
    net.storage.p_mw[net.storage['name'].isin([f'EV{bus}_{h}' for bus in range(1,33) for h in range(31)])]=Pev
    net.storage.p_mw[net.storage['name'].isin([f'B{bus}_{h}' for bus in range(1,33) for h in range(31)])]=Pbat
    pp.runpp(net,numba=False)
    volt[t]=net.res_bus.vm_pu
    loading_line[t]=net.res_line.loading_percent
    Bat_out[t]=Pbat
    EV_out[t]=Pev
    EV_soc_store[t]=soc_EV
    B_soc_store[t]=soc_B
    PV_tot_out[t]=PV_power.iloc[t]
    grid_power.append(net.res_bus.p_mw[0])
    EV_chargedNumber[t]=x

    if t==0:
        bus_results=net.res_bus
        load2=net.res_bus.p_mw
        qload2=net.res_bus.q_mvar
        angle=net.res_bus.va_degree
        voltage=net.res_bus.vm_pu
    else:
        bus_results=pd.concat([bus_results,net.res_bus],ignore_index=True,axis=1)
        load2=pd.concat([load2,net.res_bus.p_mw],ignore_index=True,axis=1)
        qload2=pd.concat([qload2,net.res_bus.q_mvar],ignore_index=True,axis=1)
        voltage=pd.concat([voltage,net.res_bus.vm_pu],ignore_index=True,axis=1)
        angle=pd.concat([angle,net.res_bus.va_degree],ignore_index=True,axis=1)

#plot the results
from results_plot import plot_results
TimeIndex=pd.date_range(start='2017-01-01 00:00',end='2017-01-02 00:00',freq='15min')
plot_results(loading_line,volt,grid_power,PV_tot_out,Loads.transpose(),EV_chargedNumber,
             Available, EV_soc_store, B_soc_store, Bat_out, EV_out, TimeIndex, name,time_elapse)