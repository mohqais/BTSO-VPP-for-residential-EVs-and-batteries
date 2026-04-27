import numpy as np
import scipy.optimize as opt

def qao_binary_optimization(objective_function, n_variables, beta_init=0.1, beta_final=10.0, n_steps=10, n_samples=10, seed=42):
  
    np.random.seed(seed)
    best_fitness_record=[]
    # Initialize the binary vector randomly
    x_best = np.random.randint(2, size=n_variables)
    f_best = objective_function(x_best)
    best_fitness_record.append(f_best)
    
    for step in range(n_steps):
        # Compute the current "temperature" using the annealing schedule
        beta = beta_init + (beta_final - beta_init) * step / (n_steps - 1)
        
        # Generate multiple samples and evaluate them
        for _ in range(n_samples):
            x = np.random.randint(2, size=n_variables)
            f = objective_function(x)
            
            # Update the best solution if a better one is found
            if f < f_best:
                x_best = x
                f_best = f
        
        # Compute the gradient of the objective function
        grad = -f_best * x_best
        
        # Compute the quantum transition probability
        transition_prob = 1 / (1 + np.exp(2 * beta * grad))
        
        # Update the binary vector based on the transition probability
        x_new = np.where(np.random.rand(n_variables) < transition_prob, 1 - x_best, x_best)
        
        # Accept the new state if it has a lower objective function value
        f_new = objective_function(x_new)
        if f_new < f_best:
            x_best = x_new
            f_best = f_new
        best_fitness_record.append(f_best)
    
    return x_best,best_fitness_record