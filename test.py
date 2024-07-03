
import random
import time
import networkx as nx
import numpy as np

def initialize_graph(N: int, M: int) -> nx.DiGraph:
    if N < 0: raise ValueError("N is less than Zero (0)")
    if M < 0: raise ValueError("M is less than Zero (0)")
    G = nx.DiGraph()
    for i in range(N): G.add_node(i)
    while G.number_of_edges() < M:
        u = random.randint(0, N)
        v = random.randint(0, N)
        if u == v or G.has_edge(u, v): continue
        G.add_edge(u, v)
    return G

def get_avg_dist(G: nx.DiGraph):
    return np.average(np.average(nx.floyd_warshall_numpy(G)))

def est_avg_dist(N: int, M: int, max_num_iterations: int = 1000):
    # sort of simulate bfs in a way
    avg_num_neighbors = M / N
    this_step = 1
    all_steps = 1

    total_dist = 0

    #print(f"N[{0}] = \t{this_step:.3f}")
    for i in range(max_num_iterations):
        # total number of connections out of this_step
        this_step *= avg_num_neighbors
        # remove total number of connections out of this_step to a previous step
        this_step *= (1 - all_steps / N)

        if this_step + all_steps > N:
            this_step = N - all_steps
            total_dist += this_step * (i + 1)
            break
        
        #print(f"N[{i+1}] = \t{this_step:.3f}")
        # add it
        total_dist += this_step * (i + 1)
        all_steps += this_step

    return total_dist / N


if __name__ == "__main__":

    N_arr = [50, 100, 150, 200]
    P_arr = [0.2, 0.4, 0.6, 0.8, 1.0]

    init_times = []
    real_times = []
    func_times = []
    error = []

    for N in N_arr:
        for P in P_arr:
            sn1 = time.time()
            M = round(P * N * (N-1))
            G = initialize_graph(N, M)
            init_times.append(time.time() - sn1)

            s0 = time.time()
            ra_dist = get_avg_dist(G)
            real_times.append(time.time() - s0)

            s1 = time.time()
            aa_dist = est_avg_dist(N, M)
            func_times.append(time.time() - s1)
            
            error.append(abs(ra_dist - aa_dist) / ra_dist)

    print(f"Int. Time:  \t{max(init_times):.3f} \t{np.average(init_times):.3f} \t{min(init_times):.3f}")
    print(f"Real Time:  \t{max(real_times):.3f} \t{np.average(real_times):.3f} \t{min(real_times):.3f}")
    print(f"Est. Time:  \t{max(func_times):.3f} \t{np.average(func_times):.3f} \t{min(func_times):.3f}")
    print(f"Est. Error: \t{max(error):.3f} \t{np.average(error):.3f} \t{min(error):.3f}")
