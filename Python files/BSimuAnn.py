# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 15:33:49 2024

@author: mqais
"""

import numpy as np
import random

def binary_simulated_annealing(objective_function, num_variables, max_iter, initial_temp, cooling_rate):
    """
    Binary Simulated Annealing (BSA) algorithm

    Parameters:
    - objective_function: function to optimize (minimize)
    - num_variables: number of binary variables
    - max_iter: maximum number of iterations
    - initial_temp: initial temperature
    - cooling_rate: cooling rate (alpha)

    Returns:
    - best_solution: best binary solution found
    - best_fitness: best fitness value found
    """
    # Initialize solution and fitness
    solution = np.random.randint(2, size=num_variables)
    fitness = objective_function(solution)
    best_fitness_record=[]

    # Initialize best solution and fitness
    best_solution = solution.copy()
    best_fitness = fitness
    best_fitness_record.append(best_fitness)
    

    # Initialize temperature
    temp = initial_temp

    for _ in range(max_iter):
        # Generate new solution by flipping a random bit
        new_solution = solution.copy()
        idx = random.randint(0, num_variables - 1)
        new_solution[idx] = 1 - new_solution[idx]

        # Calculate new fitness
        new_fitness = objective_function(new_solution)

        # Calculate delta fitness
        delta_fitness = new_fitness - fitness

        # Accept new solution if it's better or with probability exp(-delta_fitness/temp)
        if delta_fitness < 0 or random.random() < np.exp(-delta_fitness / temp):
            solution = new_solution
            fitness = new_fitness

            # Update best solution and fitness
            if fitness < best_fitness:
                best_solution = solution.copy()
                best_fitness = fitness

        # Cool down the temperature
        temp *= cooling_rate
        best_fitness_record.append(best_fitness)

    return best_solution, best_fitness_record
