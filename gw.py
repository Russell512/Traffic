import math
import random

""" < FITNESS FUNCTION > """
def fitness_rastrigin(position):
    fitness_value = 0.0
    for i in range(len(position)):
        fitness_value += (position[i] * position[i]) - (10 * math.cos(2 * math.pi * position[i])) + 10
    return fitness_value

""" < WOLF CLASS > """
class Wolf:
    def __init__(self, dim, min, max, seed):
        self.rnd = random.Random(seed)
        self.position = [0.0 for i in range(dim)]

        for i in range(dim):
            self.position[i] = (max - min) * self.rnd.random() + min

        self.fitness = fitness_rastrigin(self.position)

""" < GREY WOLF OPTIMIZATION > """
def gwo(max_iter, n, dim, min, max):
    # max_iter : 總共的iteration數量
    # n : 灰狼的總數(population)
    # dim : 地圖的維度((x, y)->dim = 2; (x, y, z)->dim = 3; ...)
    # min, max: 座標的最小、最大值
    
    rnd = random.Random(42)

    # n 個灰狼的物件
    population = [Wolf(dim, min, max, i) for i in range(n)]
    # 將全體以fitness排序
    population = sorted(population, key = lambda wolf: wolf.fitness)
    # 取前三隻狼為alpha, beta, delta
    alpha_wolf = population[0]
    beta_wolf = population[1]
    delta_wolf = population[2]

    """ < MAIN LOOP OF GWO > """
    for iter in range(max_iter):
        # 每10個週期輸出一次最好的fitness
        if iter % 10 == 0 and iter > 0:
            print(f"Iter {iter} best fitness = {alpha_wolf.fitness:.3f}")
        
        # iter = 0        -> c = 2
        # iter = max_iter -> c = 0
        c = 2 * (1 - iter / max_iter)

        # 依照alpha, beta, delta三隻狼的位置更新所有灰狼的位置
        for i in range(n):
            A1 = c * (2 * rnd.random() - 1)
            A2 = c * (2 * rnd.random() - 1)
            A3 = c * (2 * rnd.random() - 1)
            C1 = 2 * rnd.random()
            C2 = 2 * rnd.random()
            C3 = 2 * rnd.random()

            X1 = [0.0 for i in range(dim)]
            X2 = [0.0 for i in range(dim)]
            X3 = [0.0 for i in range(dim)]
            Xnew = [0.0 for i in range(dim)]

            for j in range(dim):
                X1[j] = alpha_wolf.position[j] - A1 * abs(C1 * alpha_wolf.position[j] - population[i].position[j])
                X2[j] = alpha_wolf.position[j] - A2 * abs(C2 * beta_wolf.position[j] - population[i].position[j])
                X3[j] = alpha_wolf.position[j] - A3 * abs(C3 * delta_wolf.position[j] - population[i].position[j])
                Xnew[j] = (X1[j] + X2[j] + X3[j]) / 3.0

            # 利用新的position計算fitness
            new_fitness = fitness_rastrigin(Xnew)

            # 如果new_fitness更好, 就以新的position替換此狼的位置與fitness
            if new_fitness < population[i].fitness:
                population[i].position = Xnew
                population[i].fitness = new_fitness

        # 經過一個iteration後, 重新以fitness排序全部狼
        population = sorted(population, key = lambda wolf: wolf.fitness)
        # 取前三隻狼為alpha, beta, delta
        alpha_wolf = population[0]
        beta_wolf = population[1]
        delta_wolf = population[2]
    """ < MAIN LOOP OF GWO > """
    return alpha_wolf.position

""" < MAIN > """
# arguments
max_iter = 100
num_of_wolves = 50
dim = 3
min = 5
max = 60

print("\n******************************************************")
print(f"Goal: To minimize the return value of 'Rastrigin's function' in {dim} variables")
print("\t@ Function has min = 0.0 at (" + "0," * (dim - 1) + "0)")
print()
print("==========SETTINGS==========")
print(f"Iteration = {max_iter}")
print(f"n = {num_of_wolves} (number of wolves)")
print(f"dim = {dim}")
print(f"min = {min}")
print(f"max = {max}")
print("============================")
print()
print()

print("***************GWO START***************")
best_position = gwo(max_iter, num_of_wolves, dim, min, max)
print("*************GWO COMPLETED*************")
print()
print()
print("Best solution founded:")
print([f"{best_position[i]:.6f}" for i in range(dim)])
best_fitness = fitness_rastrigin(best_position)
print(f"Fitness = {best_fitness:6f}")

print("\n******************************************************")