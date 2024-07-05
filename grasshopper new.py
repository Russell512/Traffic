import numpy as np

# Parameters
N = 10  # Number of grasshoppers (solutions)
K = 8  # Total number of phases (4 interactions -> 8 phases)
upper_bound = 60  # Max time of each phase
lower_bound = 5  # Min time of each phase
f = 0.5  # Attraction force intensity
l = 1.5  # Attractive length scale
c_min = 0.00001  # Minimum value of c
c_max = 1.0  # Maximum value of c
phi = 0.5  # Exchange parameter
T = 100  # Total number of iterations

# Initialize grasshoppers
# generates an N x K array with random values uniformly distributed between lower_bound and upper_bound.
grasshoppers = np.random.uniform(lower_bound, upper_bound, (N, K))
# grasshoppers = 論文中的S(all solutions)
# S = {s1,s2,...,sn} 代表n隻grasshopper(n 個solution)

def w(r):
    """Weight function for social interaction."""
    return f * np.exp(-r / l) - np.exp(-r)

def calculate_c(t, T, c_min, c_max, phi):
    """Calculate the parameter c based on the current iteration."""
    if t < phi * T:
        return 2 * (1 - t / T)
    else:
        return c_max - (c_max - c_min) * (t / T)

def update_position(grasshoppers, t, T, c_min, c_max, phi):
    """Update positions of grasshoppers based on social interaction."""
    c = calculate_c(t, T, c_min, c_max, phi)
    new_positions = np.zeros_like(grasshoppers)  # creates an array of zeros with the same shape as solutions.
    for i in range(N):  # iterates over each solution.(先挑一個solution，每run一次這個loop就更新一隻grasshopper的位置)
        for k in range(K):  # iterates over each phases(dimensions)(每run一次這個loop就更新一隻grasshopper的一個phase)
            # sigma 開始
            interaction_sum = 0  # sigma 的結果
            for j in range(N):
                if i != j:
                    d_ij = np.abs(grasshoppers[j, k] - grasshoppers[i, k])
                    if d_ij == 0:
                        d_ij = 1e-8  # To avoid division by zero
                    d_hat_ij = (grasshoppers[j, k] - grasshoppers[i, k]) / d_ij
                    interaction_sum += w(d_ij) * d_hat_ij
            # sigma 結束
            new_positions[i, k] = c**2 * ((upper_bound - lower_bound) / 2) * interaction_sum
    return new_positions

# Perform iterations
for t in range(T):
    new_grasshoppers = update_position(grasshoppers, t, T, c_min, c_max, phi)
    grasshoppers = new_grasshoppers

np.set_printoptions(precision=1, suppress=True)
# Print initial and updated positions
print("Initial Grasshopper Positions:")
print(grasshoppers)
print("\nUpdated Grasshopper Positions:")
print(new_grasshoppers)
