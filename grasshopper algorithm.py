import numpy as np

# Parameters
N = 10  # Number of grasshoppers(sloutions)
K = 8  # toltal number of phases (4 intersacions -> 8 phases)
upper_bound = 60 # max time of each phase
lower_bound = 5  # min time of each phase
f = 0.5  # Attraction force intensity 
l = 1.5  # Attractive length scale
c = 0.8  # Reduction coefficient for the comfort zone (temp value, to be adjusted,用論文裡c的定義)

# Initialize grasshoppers
#generates an N x K array with random values uniformly distributed between lower_bound and upper_bound.
grasshoppers = np.random.uniform(lower_bound, upper_bound, (N, K))
#grasshoppers = 論文中的S(all solutions)
#S = {s1,s2,...,sn} 代表n隻grasshopper(n 個solution)


def w(r):
    """Weight function for social interaction."""
    return f * np.exp(-r / l) - np.exp(-r)

def update_position(grasshoppers):
    """Update positions of grasshoppers based on social interaction."""
    new_positions = np.zeros_like(grasshoppers) # creates an array of zeros with the same shape as solutions.
    for i in range(N):                          # iterates over each solution.(先挑一個solution)
        #開始計算這個solution中每個dimension的
        for k in range(K):                      # iterates over each phases(dimensions)
            #sigma 開始
            interaction_sum = 0                 # sigma 的結果
            for j in range(N):                          
                if i != j:
                    d_ij = np.abs(grasshoppers[j, k] - grasshoppers[i, k])
                    if d_ij == 0:
                        d_ij = 1e-8  # To avoid division by zero
                    d_hat_ij = (grasshoppers[j, k] - grasshoppers[i, k]) / d_ij
                    interaction_sum += w(d_ij) * d_hat_ij
            #sigma 結束
            new_positions[i, k] = c**2 * ((upper_bound - lower_bound) / 2) * interaction_sum
    return new_positions

# Update grasshopper positions
new_grasshoppers = update_position(grasshoppers)
np.set_printoptions(precision=1, suppress=True)
# Print initial and updated positions
print("Initial Grasshopper Positions:")
print(grasshoppers)
print("\nUpdated Grasshopper Positions:")
print(new_grasshoppers)
