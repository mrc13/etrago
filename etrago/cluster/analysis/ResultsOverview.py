# -*- coding: utf-8 -*-
"""
"""
from config import sim_results_path, total_results_path, plot_path
# TODO: Make plot_path import work...don't know why it does not
from os import path, listdir

import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
import os
kmean = []

files1 = os.listdir(sim_results_path)

for c in range (1,len(files1)+1):

    path01= sim_results_path + 'ResultsExpansions' + str(c) +'.csv'
    Total = pd.read_csv(path01)
    k= Total.loc[0]['k-mean']
    
    if c == 1:
        results = Total
    else:
        results= results.append(Total)
 
    if (k in kmean) == False:
            kmean.append(k)

results.rename(columns={'Unnamed: 0':'Snapshots'}, inplace=True)
results.to_csv(total_results_path + 'TotalResults.csv')

for i in range(len(kmean)):
    value = int(kmean[i])
    RS = results.loc[results ['k-mean'] == value]
    R2LOPFST = RS.loc[(RS['TypeSim'] == '2LOPF') & (RS['Storage'] == True)]
    R2LOPFST = R2LOPFST.sort_values(['Snapshots'], ascending = [1]) 
    R2LOPFnoST = RS.loc[(RS['TypeSim'] == '2LOPF') & (RS['Storage'] == False)]
    R2LOPFnoST = R2LOPFnoST.sort_values(['Snapshots'], ascending = [1]) 
    RBMST = RS.loc[(RS['TypeSim'] == 'BM') & (RS['Storage'] == True)]
    RBMST = RBMST.sort_values(['Snapshots'], ascending = [1]) 
    RBMnoST = RS.loc[(RS['TypeSim'] == 'BM') & (RS['Storage'] == False)]
    RBMnoST = RBMnoST.sort_values(['Snapshots'], ascending = [1]) 

    ##Plot graphs with storage
    fig, ax = plt.subplots()
    ax2 = ax 

    R2LOPFST.plot(x='Snapshots', y='2nd LOPF', title = 'simulation time for k-mean= '+ str(value) + ' with Storage', ax=ax, label="2 LOPFs")
    RBMST.plot(x='Snapshots', y='2nd LOPF', title = 'simulation time for k-mean= '+ str(value) + ' with Storage', ax = ax2, label = "Benchmark", ls = "--")
    
    ax.set_ylabel('Simulation Time 2nd LOPF (s)')
    ax.set_xlabel('Number of Snapshots')
    
    plt.show()
    
    fig = ax.get_figure()
    fig.savefig(path.join(plot_path, 'simulation time for k-mean= '+ str(value) +'.eps'))
    
    ##Plot graphs without storage
    fig, ax = plt.subplots()
    ax2 = ax 

    R2LOPFnoST.plot(x='Snapshots', y='2nd LOPF', title = 'simulation time for k-mean= '+ str(value) + ' without Storage', ax=ax, label="2 LOPFs")
    RBMnoST.plot(x='Snapshots', y='2nd LOPF', title = 'simulation time for k-mean= '+ str(value) + ' without Storage', ax = ax2, label="Benchmark", ls = "--")
    
    ax.set_ylabel('Simulation Time 2nd LOPF (s)')
    ax.set_xlabel('Number of Snapshots')
    
    plt.show()
    
    fig = ax.get_figure()
    fig.savefig(path.join(plot_path, 'simulation time for k-mean= '+ str(value) +' without Storage.eps'))
    