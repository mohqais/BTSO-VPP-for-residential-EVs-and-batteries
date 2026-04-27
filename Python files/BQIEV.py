import numpy as np

def quantum_inspired_evolutionary_algorithm(objective_function, n_variables, population_size=40, n_generations=100, q_rotation_angle=np.pi/8, seed=42):
    
    np.random.seed(seed)
    best_fitness_record=[]
    # Initialize the population
    population = np.random.uniform(0, 1, size=(population_size, n_variables))
    q_population = np.arccos(np.sqrt(population))
    
    # Evaluate the initial population
    fitness = [objective_function(np.round(np.cos(q_individual) > np.sin(q_individual))) for q_individual in q_population]
    
    # Find the best individual in the initial population
    best_index = np.argmin(fitness)
    best_individual = np.round(np.cos(q_population[best_index]) > np.sin(q_population[best_index])).copy()
    best_fitness = fitness[best_index]
    best_fitness_record.append(best_fitness)
    
    for generation in range(n_generations):
        # Update the quantum-inspired population
        for i in range(population_size):
            for j in range(n_variables):
                if np.random.rand() < 0.5:
                    q_population[i, j] = q_population[i, j] + q_rotation_angle * (1 - 2 * np.round(np.cos(q_population[i, j]) > np.sin(q_population[i, j])))
                else:
                    q_population[i, j] = q_population[i, j] - q_rotation_angle * (1 - 2 * np.round(np.cos(q_population[i, j]) > np.sin(q_population[i, j])))
        
        # Evaluate the new population
        new_fitness = [objective_function(np.round(np.cos(q_individual) > np.sin(q_individual))) for q_individual in q_population]
        
        # Update the best individual if necessary
        for i in range(population_size):
            if new_fitness[i] < best_fitness:
                best_individual = np.round(np.cos(q_population[i]) > np.sin(q_population[i])).copy()
                best_fitness = new_fitness[i]
        best_fitness_record.append(best_fitness)
    
    return best_individual,best_fitness_record

# Example usage
# def objective_function(x):
#     """
#     Example objective function: Minimize the number of ones in the binary vector.
#     """
#     return np.sum(x)

# n_variables = 20
# solution = quantum_inspired_evolutionary_algorithm(objective_function, n_variables)
# print("Optimal solution:", solution)
# print("Objective function value:", objective_function(solution))