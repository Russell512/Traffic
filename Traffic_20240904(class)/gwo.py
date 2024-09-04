import numpy as np
import time
import matplotlib.pyplot as plt
import copy

from configuration import *
from solution import Solution
from encoding import encode
from sumo_traci import simulationStart

class GWO():
    def __init__(self, N, phase, lower_bound, upper_bound, max_iter, phi, c_min=0.00001, c_max=1.0):
        self.solutions = [Solution(lower_bound, upper_bound, phase) for i in range(N)]
        self.start = time.time()
        self.history = []
        self.N = N
        self.phase = phase
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.max_iter = max_iter
        self.phi = phi
        self.c_min = c_min
        self.c_max = c_max
        
    def calculate_c(self, t):
        if t < self.phi * self.max_iter:
            return 2 * (1 - t / self.max_iter)
        else:
            return self.c_max - (self.c_max - self.c_min) * (t / self.max_iter)
    
    def Hunting(self, s_alpha, s_beta, s_delta, A1, A2, A3, C1, C2, C3, si):
        X1 = np.zeros(self.phase)
        X2 = np.zeros(self.phase)
        X3 = np.zeros(self.phase)
        p = np.zeros(self.phase)
        for k in range(self.phase):
            X1[k] = s_alpha.duration[k] - A1 * abs(C1 * s_alpha.duration[k] - si.duration[k])
            X2[k] = s_beta.duration[k] - A2 * abs(C2 * s_beta.duration[k] - si.duration[k])
            X3[k] = s_delta.duration[k] - A3 * abs(C3 * s_delta.duration[k] - si.duration[k])
            p[k] = ( X1[k] + X2[k] + X3[k] ) / 3
        return p
    
    def run(self):
        print("Initialization")
        for i, si in enumerate(self.solutions):
            i_sumocfg = encode(i, si.duration)
            simulationStart(HIS_PATH + i_sumocfg, SIM_TIME)
            si.evaluate(i)
        self.solutions = sorted(self.solutions, key = lambda s: s.value)
        s_alpha = self.solutions[0]
        s_beta = self.solutions[1]
        s_delta = self.solutions[2]

        for t in range(self.max_iter):
            old_solutions = [copy.deepcopy(solution) for solution in self.solutions]
            print(f"\nIter {t+1:4d}/{self.max_iter}\t Time used: {time.time() - self.start:.2f} sec")

            c = self.calculate_c(t)
            for i, si in enumerate(self.solutions):
                A1 = c * (2 * np.random.random() - 1)
                A2 = c * (2 * np.random.random() - 1)
                A3 = c * (2 * np.random.random() - 1)
                C1 = 2 * np.random.random()
                C2 = 2 * np.random.random()
                C3 = 2 * np.random.random()

                si.duration = self.Hunting(s_alpha, s_beta, s_delta, A1, A2, A3, C1, C2, C3, si)

            for i, si in enumerate(self.solutions):
                si.duration = [int(round(d)) for d in si.duration]
                for j in range(self.phase):
                    if si.duration[j] < self.lower_bound:
                        si.duration[j] = self.lower_bound
                    elif si.duration[j] > self.upper_bound:
                        si.duration[j] = self.upper_bound
                i_sumocfg = encode(i, si.duration)
                simulationStart(HIS_PATH + i_sumocfg, SIM_TIME)
                si.evaluate(i)
            self.solutions = sorted(self.solutions, key = lambda s: s.value)
            if self.solutions[0].value > old_solutions[0].value:
                self.solutions = old_solutions
            s_alpha = self.solutions[0]
            s_beta = self.solutions[1]
            s_delta = self.solutions[2]

            print("\nDuration: ", end="")
            print(s_alpha.duration)
            print(f"Current objective value = {s_alpha.value:.4f}")
            self.history.append(s_alpha.value)

        return s_alpha, self.history
    
    def show_result(self, name):
        print()
        print("################### PROGRAM START ###################")
        print()
        print("*************** GWO START ***************")

        opt_solution, history = self.run()
        plt.plot(history)
        plt.xlabel("Iteration")
        plt.ylabel("Objective Value")
        plt.savefig(OPT_PATH + name + "_history.png")

        print()
        print("************* GWO COMPLETED *************")
        print()
        print("Optimized solution founded:")
        print(opt_solution.duration)
        print(f"Objective value = {opt_solution.value:.4f}")
        print(f"Total time used: {time.time() - self.start:.2f} sec")
        print()
        opt_sumocfg = encode(name, opt_solution.duration)
        print(f"Simulation configuration file '{opt_sumocfg}' has been generated.")
        print()
        print("################## PROGRAM END ##################")
        print()
        return history

if __name__ == '__main__':
    N = 5
    lower_bound = 5
    upper_bound = 60
    max_iter = 3
    phi = 0.25

    gwgo = GWO(N, PHASE, lower_bound, upper_bound, max_iter, phi, c_min=0.00001, c_max=1.0)
    history = gwgo.show_result('gwo')