# Overview

This repository provides the full implementation of a Virtual Power Plant (VPP) framework integrating:  
🔋 Battery Energy Storage Systems (BESS)  
🚗 Electric Vehicles (EVs)  
⚡ Voltage support for a residential distribution network  

The VPP is optimally scheduled using a novel Binary Transient Search Optimization (Binary TSO) algorithm, which is benchmarked against seven established metaheuristics: e.g. Binary PSO, Grey Wolf Optimizer (GWO), Genetic Algorithm (GA), Differential Evolution (DE), and others.  
The distribution network used is the IEEE 33-bus test system, modelled and simulated using Pandapower.  
Key objective: Improve the voltage profile of a residential distribution system by optimally coordinating EV charging/discharging and BESS dispatch within a VPP framework.  
To use this repository, download datasets and python files, use Main.py file to run the optimization algorithms. make sure all python files of all algorithms are in the same location.  
