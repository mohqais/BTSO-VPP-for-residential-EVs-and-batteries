# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 12:48:56 2024

@author: mqais
"""

import numpy as np

def binary_pso(objective_function, num_particles, num_dimensions, max_iter, w, c1, c2):
  
    # Initialize particles
    particles = np.random.uniform(0, 1, size=(num_particles, num_dimensions))
    velocities = np.random.uniform(-1, 1, size=(num_particles, num_dimensions))

    # Initialize best positions and fitness values
    best_positions = particles.copy()
    best_fitnesses = np.array([objective_function(p) for p in particles])
    global_best_fitness=[]

    # Initialize global best position and fitness
    global_best_position = particles[np.argmin(best_fitnesses)]
    global_best_fitness.append(np.min(best_fitnesses))

    for i in range(max_iter):
        # Update velocities
        velocities = w * velocities + c1 * np.random.uniform(0, 1, size=(num_particles, num_dimensions)) * (best_positions - particles) + \
                     c2 * np.random.uniform(0, 1, size=(num_particles, num_dimensions)) * (global_best_position - particles)

        # Update positions
        particles = np.where(np.random.uniform(0, 1, size=(num_particles, num_dimensions)) < 1 / (1 + np.exp(-10*velocities)), 1, 0)

        # Evaluate fitness
        fitnesses = np.array([objective_function(p) for p in particles])

        # Update best positions and fitness values
        for j in range(num_particles):
            if fitnesses[j] < best_fitnesses[j]:
                best_positions[j] = particles[j]
                best_fitnesses[j] = fitnesses[j]

        # Update global best position and fitness
        global_best_position = best_positions[np.argmin(best_fitnesses)]
        global_best_fitness.append(np.min(best_fitnesses))

    return global_best_position, global_best_fitness