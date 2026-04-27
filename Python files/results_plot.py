"""
Created on Tue Sep 24 19:42:16 2024
@author: mqais
"""
from matplotlib_inline.backend_inline import set_matplotlib_formats
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates 
import numpy as np
import matplotlib.ticker as ticker
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator
from matplotlib.ticker import FormatStrFormatter
set_matplotlib_formats('svg')

def plot_results(loading_line,Volt,Pgrid,PV,Load,EV_no,EV_avail,socEV,socB,P_bat,P_ev,TimeIndex,name,time_elapse):
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111)
    p1=plt.plot(socB.T,label='EV',linewidth=0.5,color='tan')
    p2=plt.plot(socB.T.mean(axis=1),linewidth=1.5,color='brown')
    plt.xlabel('Time step (every 15 min)',fontsize=14,weight = 'bold',color='blue')
    plt.ylabel('SOC of residential BESSs',fontsize=14,weight = 'bold',color='blue')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.legend([p1[0],p2[0]],['1000 BESS SOC profiles','Average SOC Profile'],frameon=False,fontsize=16)
    #plt.legend(['EV'+'{:d}'.format(h+1) for h in range(len(hld['Bus33']))])
    plt.tick_params(axis='both', which='major', labelsize=16)
    ax.set(xlim=(0, 97))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(8))
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.set_xticklabels(['00:00','00:00','02:00','04:00','06:00','08:00','10:00','12:00','14:00','16:00','18:00','20:00','22:00','24:00'])
    #plt.xticks(rotation=90)
    split_points=[0,32,72,97]
    split_colors = ['blue', 'grey', 'blue']
    for i in range(len(split_points)-1):
        plt.axvspan(split_points[i+1], split_points[i], facecolor=split_colors[i], alpha=0.15, zorder=-1)
    ax.tick_params(axis='x', colors='blue')
    ax.tick_params(axis='y', colors='blue')
    ax.spines['left'].set_color('brown')
    ax.spines['right'].set_color('brown')
    ax.spines['top'].set_color('brown')
    ax.spines['bottom'].set_color('brown')
    plt.show()
    
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111)
    p1=plt.plot(socEV.T,label='EV',linewidth=0.5,color='tan')
    p2=plt.plot(socEV.T.mean(axis=1),linewidth=1.5,color='brown')
    plt.xlabel('Time step (every 15 min)',fontsize=14,weight = 'bold',color='blue')
    plt.ylabel('SOC of residential EVs',fontsize=14,weight = 'bold',color='blue')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.legend([p1[0],p2[0]],['1000 EV SOC profiles','Average SOC Profile'],frameon=False,fontsize=16)
    #plt.legend(['EV'+'{:d}'.format(h+1) for h in range(len(hld['Bus33']))])
    plt.tick_params(axis='both', which='major', labelsize=16)
    ax.set(xlim=(0, 97))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(8))
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.set_xticklabels(['00:00','00:00','02:00','04:00','06:00','08:00','10:00','12:00','14:00','16:00','18:00','20:00','22:00','24:00'])
    #plt.xticks(rotation=90)
    split_points=[0,32,72,97]
    split_colors = ['blue', 'grey', 'blue']
    for i in range(len(split_points)-1):
        plt.axvspan(split_points[i+1], split_points[i], facecolor=split_colors[i], alpha=0.15, zorder=-1)
    ax.tick_params(axis='x', colors='blue')
    ax.tick_params(axis='y', colors='blue')
    ax.spines['left'].set_color('brown')
    ax.spines['right'].set_color('brown')
    ax.spines['top'].set_color('brown')
    ax.spines['bottom'].set_color('brown')
    plt.show()
    
    '''
    plot statistics of SOC of EVS
    '''
    # fig=plt.figure()
    # ax = fig.add_subplot(111)
    # sns.set(style="whitegrid")
    df3=socEV

    # Create a box plot with time as x-ticks
    plt.figure(figsize=(12, 6))
    ax1=sns.boxplot(df3,whis=(0,100),width=0.5,notch=True)

    plt.xlabel('Time step (every 15 min)',fontsize=14,weight = 'bold',color='blue')
    plt.ylabel('SOC of residential EVs',fontsize=14,weight = 'bold',color='blue')
    plt.tick_params(axis='both', which='major', labelsize=14)
    ax1.set(xlim=(0, 97))
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(8))
    ax1.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax1.set_xticklabels(['00:00','00:00','02:00','04:00','06:00','08:00','10:00','12:00','14:00','16:00','18:00','20:00','22:00','24:00'])
    #plt.xticks(rotation=90)
    split_points=[0,32,72,97]
    split_colors = ['blue', 'grey', 'blue']
    for i in range(len(split_points)-1):
        plt.axvspan(split_points[i+1], split_points[i], facecolor=split_colors[i], alpha=0.15, zorder=-1)

    # Show the plot with tight layout
    plt.margins(0,0)
    ax1.tick_params(axis='x', colors='blue')
    ax1.tick_params(axis='y', colors='blue')
    ax1.spines['left'].set_color('brown')
    ax1.spines['right'].set_color('brown')
    ax1.spines['top'].set_color('brown')
    ax1.spines['bottom'].set_color('brown')
    plt.savefig(name+"SOC_EVs.svg", format='svg',bbox_inches='tight')
    plt.show()
    
    '''
    plot statistics of SOC of batteries
    '''
    # fig=plt.figure()
    # ax = fig.add_subplot(111)
    # sns.set(style="whitegrid")
    df3=socB

    # Create a box plot with time as x-ticks
    plt.figure(figsize=(12, 6))
    ax1=sns.boxplot(df3,whis=(0,100),width=0.5,notch=True)

    plt.xlabel('Time step (every 15 min)',fontsize=14,weight = 'bold',color='blue')
    plt.ylabel('SOC of residential BESS',fontsize=14,weight = 'bold',color='blue')
    plt.tick_params(axis='both', which='major', labelsize=14)
    ax1.set(xlim=(0, 97))
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(8))
    ax1.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax1.set_xticklabels(['00:00','00:00','02:00','04:00','06:00','08:00','10:00','12:00','14:00','16:00','18:00','20:00','22:00','24:00'])
    #plt.xticks(rotation=90)
    split_points=[0,32,72,97]
    split_colors = ['blue', 'grey', 'blue']
    for i in range(len(split_points)-1):
        plt.axvspan(split_points[i+1], split_points[i], facecolor=split_colors[i], alpha=0.15, zorder=-1)

    # Show the plot with tight layout
    plt.margins(0,0)
    ax1.tick_params(axis='x', colors='blue')
    ax1.tick_params(axis='y', colors='blue')
    ax1.spines['left'].set_color('brown')
    ax1.spines['right'].set_color('brown')
    ax1.spines['top'].set_color('brown')
    ax1.spines['bottom'].set_color('brown')
    plt.savefig(name+"SOC_BESS.svg", format='svg',bbox_inches='tight')
    plt.show()

    # '''
    # plot the bus voltages
    # '''
    # fig = plt.figure()
    # ax20 = fig.add_subplot(111)
    # sns.boxplot(Volt.transpose(),whis=(0,100),width=0.5,notch=False)
    # plt.plot([0.94]*33,linestyle='dashed')
    # plt.xlabel('Bus#',fontsize=12,weight = 'bold',color='blue')
    # plt.ylabel('Bus voltage (pu)',fontsize=12,weight = 'bold',color='blue')
    # plt.xticks(rotation=90, fontweight='light',  fontsize='x-small')
    # plt.tick_params(axis='both', which='major', labelsize=10)
    # plt.margins(0,0)
    # ax20.set(ylim=(0.93,1.005))
    # ax20.set_xticklabels(np.arange(1,34))
    # ax20.tick_params(axis='x', colors='blue')
    # ax20.tick_params(axis='y', colors='blue')
    # ax20.spines['left'].set_color('brown')
    # ax20.spines['right'].set_color('brown')
    # ax20.spines['top'].set_color('brown')
    # ax20.spines['bottom'].set_color('brown')
    # plt.savefig(name+"Voltage.svg", format='svg',bbox_inches='tight')
    # plt.show()
    
    # Create a box plot with time as x-ticks
    plt.figure(figsize=(12, 6))
    ax1=sns.boxplot(Volt,whis=(0,100),width=0.5,notch=True)
    plt.plot([0.94]*97,linestyle='dashed')

    plt.xlabel('Time step (every 15 min)',fontsize=14,weight = 'bold',color='blue')
    plt.ylabel('Bus voltage (pu)',fontsize=14,weight = 'bold',color='blue')
    plt.tick_params(axis='both', which='major', labelsize=14)
    ax1.set(xlim=(0, 97),ylim=(0.82,1.0))
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(8))
    ax1.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax1.set_xticklabels(['00:00','00:00','02:00','04:00','06:00','08:00','10:00','12:00','14:00','16:00','18:00','20:00','22:00','24:00'])
    #plt.xticks(rotation=90)
    split_points=[0,32,72,97]
    split_colors = ['blue', 'grey', 'blue']
    for i in range(len(split_points)-1):
        plt.axvspan(split_points[i+1], split_points[i], facecolor=split_colors[i], alpha=0.15, zorder=-1)

    # Show the plot with tight layout
    plt.margins(0,0)
    ax1.tick_params(axis='x', colors='blue')
    ax1.tick_params(axis='y', colors='blue')
    ax1.spines['left'].set_color('brown')
    ax1.spines['right'].set_color('brown')
    ax1.spines['top'].set_color('brown')
    ax1.spines['bottom'].set_color('brown')
    plt.savefig(name+"Voltage.svg", format='svg',bbox_inches='tight')
    plt.show()
    
    '''
    Stacked areas
    '''
    fig = plt.figure()
    ax44 = fig.add_subplot(111)
    positive_labels=['EVs','Bat_Charging','Households']
    negative_labels=['PV','Bat_Discharging','Imported grid power']
    plt.stackplot(TimeIndex,P_ev.sum(),P_bat.sum().clip(lower=0),Load.sum(),labels=positive_labels,colors=['orange','g','olive'])
    # plt.stackplot(TimeIndex,P_bat.sum(),colors=['g'])
    plt.stackplot(TimeIndex,-PV.sum(),P_bat.sum().clip(upper=0),Pgrid,labels=negative_labels ,colors=['yellow','lime','cyan'])
    # plt.stackplot(TimeIndex,-Load.sum(),colors=['b'])
    plt.legend(loc='lower center',ncols=2,facecolor='inherit',frameon=False)
    plt.xlabel('Time step (every 15 min)',fontsize=12,weight = 'normal',color='blue')
    plt.ylabel('Aggregated Real Power (MW)',fontsize=12,weight = 'normal',color='blue')
    ax44.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    #plt.legend(['EV'+'{:d}'.format(h+1) for h in range(len(hld['Bus33']))])
    plt.margins(0,0)
    ax44.tick_params(axis='x', colors='blue')
    ax44.tick_params(axis='y', colors='blue')
    ax44.spines['left'].set_color('brown')
    ax44.spines['right'].set_color('brown')
    ax44.spines['top'].set_color('brown')
    ax44.spines['bottom'].set_color('brown')
    plt.savefig(name+"Powers.svg", format='svg',bbox_inches='tight')

    plt.show()
    # plot 3D for voltage and transmission line loading
    rows, cols = 33, 97
    x_1d = np.linspace(0, 97, cols)  # 97 points
    y_1d = np.linspace(1, 33, rows)   # 33 points

    # Create 2D meshgrid from 1D arrays
    X, Y = np.meshgrid(x_1d, y_1d)
    Z = Volt*100 #convert from pu to percentage

    # Create 3D plot
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(X, Y, Z, cmap='viridis', 
                           edgecolor='none', alpha=0.9)
    # Add labels and title
    ax.set_ylabel('Bus#')
    ax.set_xlabel('Time step')
    ax.set_zlabel('Voltage (%)')
    ax.set_xticks(np.arange(0, 97, 4*3))  # Ticks every 3 hours
    ax.set_xticklabels([f'{int(h/4):02d}:00' for h in np.arange(0, 97, 4*3)])
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    ax.set_zlim(80, 100)
    # Add colorbar
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, pad=0.1, fraction=0.1,format='%.1f')
    ax.view_init(elev=30, azim=-45)

    plt.show()
    
    # Create sample data with dimensions 33x97
    rows, cols = 32, 97
    x_1d = np.linspace(0, 97, cols)  # 97 points
    y_1d = np.linspace(1, 32, rows)   # 33 points

    # Create 2D meshgrid from 1D arrays
    X, Y = np.meshgrid(x_1d, y_1d)
    Z = loading_line


    # Create 3D plot for transmission line loading
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Plot surface
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', 
                           edgecolor='none', alpha=0.9)

    ax.set_ylabel('Line#')
    ax.set_xlabel('Time step')
    ax.set_zlabel('Loading (%)')
 
    ax.set_xticks(np.arange(0, 97, 4*3))  # Ticks every 3 hours
    ax.set_xticklabels([f'{int(h/4):02d}:00' for h in np.arange(0, 97, 4*3)])
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    ax.set_zlim(0, 120)
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, pad=0.1, fraction=0.1,format='%.1f')

    ax.view_init(elev=30, azim=-45)
    plt.show()

    print('The statistics of last SOC of EVs')
    print(socEV.transpose().iloc[96].astype('float').describe())
    print('minimum Voltage')
    print(Volt.min().min())
    print('The maximum elapsed time for optimization')
    print(max(time_elapse))
    