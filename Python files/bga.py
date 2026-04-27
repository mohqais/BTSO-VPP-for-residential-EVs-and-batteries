
import numpy as np
import pandas as pd
import random


class BGA():
    
    def __init__(self, pop_shape, method, p_c=0.8, p_m=0.2, max_round = 20, early_stop_rounds=None, verbose = None, maximum=True):
        
        if early_stop_rounds != None:
            assert(max_round > early_stop_rounds)
        self.pop_shape = pop_shape
        self.method = method
        self.pop = np.zeros(pop_shape)
        self.fitness = np.zeros(pop_shape[0])
        self.p_c = p_c
        self.p_m = p_m
        self.max_round = max_round
        self.early_stop_rounds = early_stop_rounds
        self.verbose = verbose
        self.maximum = maximum

    def evaluation(self, pop):
        
        return np.array([self.method(i) for i in pop])

    def initialization(self):
        
        self.pop = np.random.randint(low=0, high=2, size=self.pop_shape)
        self.fitness = self.evaluation(self.pop)

    def crossover(self, ind_0, ind_1):
        
        assert(len(ind_0) == len(ind_1))

        point = np.random.randint(len(ind_0))
#         new_0, new_1 = np.zeros(len(ind_0)),  np.zeros(len(ind_0))
        new_0 = np.hstack((ind_0[:point], ind_1[point:]))
        new_1 = np.hstack((ind_1[:point], ind_0[point:]))

        assert(len(new_0) == len(ind_0))
        return new_0, new_1

    def mutation(self, indi):
        
        point = np.random.randint(len(indi))
        indi[point] = 1 - indi[point]
        return indi


    def rws(self, size, fitness):
        
        if self.maximum:
            fitness_ = fitness
        else:
            fitness_ = 1.0 / fitness
#         fitness_ = fitness
        idx = np.random.choice(np.arange(len(fitness_)), size=size, replace=True,
               p=fitness_/fitness_.sum()) # p 就是选它的比例
        return idx

    def run(self):
        
        global_best = 0
        self.initialization()
        best_index = np.argsort(self.fitness)[0]
        global_best_fitness = self.fitness[best_index]
        global_best_ind = self.pop[best_index, :]
        eva_times = self.pop_shape[0]
        count = 0
        Best_fitness=[]
        

        for it in range(self.max_round):
            Best_fitness.append(global_best_fitness)
            next_gene = []

            for n in range(int(self.pop_shape[0]/2)):
                i, j = self.rws(2, self.fitness) # choosing 2 individuals with rws.
                indi_0, indi_1 = self.pop[i, :].copy(), self.pop[j, :].copy()
                if np.random.rand() < self.p_c:
                    indi_0, indi_1 = self.crossover(indi_0, indi_1)

                if np.random.rand() < self.p_m:
                    indi_0 = self.mutation(indi_0)
                    indi_1 = self.mutation(indi_1)

                next_gene.append(indi_0)
                next_gene.append(indi_1)

            self.pop = np.array(next_gene)
            self.fitness = self.evaluation(self.pop)
            eva_times += self.pop_shape[0]

            if self.maximum:
                if np.max(self.fitness) > global_best_fitness:
                    best_index = np.argsort(self.fitness)[-1]
                    global_best_fitness = self.fitness[best_index]
                    global_best_ind = self.pop[best_index, :]
                    count = 0
                else:
                    count +=1
                worst_index = np.argsort(self.fitness)[-1]
                self.pop[worst_index, :] = global_best_ind
                self.fitness[worst_index] = global_best_fitness

            else:
                if np.min(self.fitness) < global_best_fitness:
                    best_index = np.argsort(self.fitness)[0]
                    global_best_fitness = self.fitness[best_index]
                    global_best_ind = self.pop[best_index, :]
                    count = 0
                else:
                    count +=1

                worst_index = np.argsort(self.fitness)[-1]
                self.pop[worst_index, :] = global_best_ind
                self.fitness[worst_index] = global_best_fitness

            # if self.verbose != None and 0 == (it % self.verbose):
            #     print('Gene {}:'.format(it))
            #     print('Global best fitness:', global_best_fitness)

            if self.early_stop_rounds != None and count > self.early_stop_rounds:
                #print('Did not improved within {} rounds. Break.'.format(self.early_stop_rounds))
                break

        #print('\n Solution: {} \n Fitness: {} \n Evaluation times: {}'.format(global_best_ind, global_best_fitness, eva_times))
        return global_best_ind, Best_fitness
