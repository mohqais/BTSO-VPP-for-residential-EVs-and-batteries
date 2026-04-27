import numpy as np

def TSO_algor(SearchAgents_no, dim,L, fobj):
    best_voltage = np.ones(dim,dtype=bool)  # Initialize best voltage vector
    best_score = float('inf')  # Change this to -inf for maximization problems
    # voltages =np.random.randint(0, 2, size=(SearchAgents_no,dim)) #1*(np.random.uniform(size=[SearchAgents_no, dim])>0.7)  # Initialize voltages
    voltages=np.random.uniform(size=[SearchAgents_no, dim])<0.5
    
    Convergence_curve = np.zeros(L)

    # Main loop
    for l in range(L):
        for i in range(SearchAgents_no):
            

            fitness = np.array([fobj(voltages[i, :])])  # Calculate objective function for each search agent

            # Update the best
            if fitness < best_score:
                best_score = fitness.copy()
                best_voltage = voltages[i, :].copy()

        t = 2 - l * (2 / L)
        K = 1  # K is a real number
        r1 = np.random.rand(1,SearchAgents_no)
        r2 = np.random.rand(1,SearchAgents_no)
        r3 = np.random.rand(1,SearchAgents_no)
        T = 2 * t * r1 - t
        C1 = K * r2 * t + 1
        r5=np.random.uniform(-1,1,(SearchAgents_no,dim))
        best_v=np.tile(best_voltage,(SearchAgents_no,1))
        flag1=np.exp(-T).T * (voltages - C1.T * best_v)<r5
        flag2=np.exp(-T).T *((np.cos(T * 2 * np.pi) + np.sin(T * 2 * np.pi)).T * (voltages - C1.T * best_v))<r5
        flag3=r3<0.2
        voltages=(best_v*flag1+np.invert(best_v)*np.invert(flag1))*flag3.T+(best_v*flag2+np.invert(best_v)*np.invert(flag2))*np.invert(flag3).T
        
        Convergence_curve[l] = best_score
        

    return best_voltage, Convergence_curve
