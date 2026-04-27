
"""
Created on Tue Aug 27 16:05:15 2024

@author: mqais
"""

import numpy as np
import random

def bde(objective_function, num_variables, num_population, num_generations, F, Cr):

    # Initialize the population randomly
    population = np.random.randint(2, size=(num_population, num_variables))
    best_fitness_record=[]

    # Evaluate the initial population
    fitness = [objective_function(individual) for individual in population]

    # Find the best individual in the initial population
    best_index = np.argmin(fitness)
    best_solution = population[best_index]
    best_fitness = fitness[best_index]
    best_fitness_record.append(best_fitness)

    # Iterate through the generations
    for _ in range(num_generations):
        # Create the new population
        new_population = []
        for i in range(num_population):
            # Select three random individuals, excluding the current individual
            indices = [j for j in range(num_population) if j != i]
            r1, r2, r3 = random.sample(indices, 3)

            # Perform mutation
            mutant = population[r1] + F * (population[r2] - population[r3])
            mutant = np.clip(mutant, 0, 1)
            mutant = mutant.astype(int)

            # Perform crossover
            trial = np.where(np.random.rand(num_variables) < Cr, mutant, population[i])

            # Evaluate the trial individual
            trial_fitness = objective_function(trial)

            # Select the better individual between the current and the trial
            if trial_fitness < fitness[i]:
                new_population.append(trial)
                fitness[i] = trial_fitness
            else:
                new_population.append(population[i])

        # Update the population
        population = new_population

        # Find the best individual in the current population
        best_index = np.argmin(fitness)
        if fitness[best_index] < best_fitness:
            best_solution = population[best_index]
            best_fitness = fitness[best_index]
        best_fitness_record.append(best_fitness)

    return best_solution,best_fitness_record
