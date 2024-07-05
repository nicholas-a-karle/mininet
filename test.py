
import random
import time
from typing import List
import networkx as nx
import community
import numpy as np

def initialize_graph(N: list[int], M: list[list[int]]) -> nx.DiGraph:

    print("initialize_graph call")

    if len(N) != len(M): raise ValueError(f"Sizes of N ({len(N)}) and M {len(M)} do not match on first dimension of M!")
    for i in range(len(M)):
        if len(N) != len(M[i]): raise ValueError(f"Sizes of N {len(N)} and element of M, M[{i}] ({len(M[i])}), do not match!")
        if len(M) != len(M[i]): raise ValueError(f"Sizes of M ({len(M)}) and an element of M, M[{i}] ({len(M[i])}), do not match!")
    # TODO: Check 0 <= M[i][j] <= N[i] * N[j] and 0 <= M[i][i] <= N[i] * (N[i]-1)

    G = nx.DiGraph()

    groups = []
    num_edges = [[0 for _ in N] for _ in N]
    s = 0
    for i in range(len(N)):
        # print(f"s={s} \tN[{i}]={N[i]}")
        groups.append([k for k in range(s, s+N[i])])
        s += N[i]

    for i in range(sum(N)):
        G.add_node(i)

    # print(f"num_nodes: {len(G)}")
    # for group in groups: print(group)

    for i in range(len(N)):
        for j in range(len(N)):
            while num_edges[i][j] < M[i][j]:
                u = random.choice(groups[i])
                v = random.choice(groups[j])
                if u == v or G.has_edge(u, v): continue
                G.add_edge(u, v)
                num_edges[i][j] += 1
    print("Conn. Check: \t", end='')
    print(nx.is_strongly_connected(G))
    if nx.is_strongly_connected(G):
        return G, groups
    else:
        return initialize_graph(N, M)

def get_avg_dist(G: nx.DiGraph):
    print("call get_avg_dist")
    return np.average(np.average(nx.floyd_warshall_numpy(G)))

def est_avg_dist_internal(N: int, M: int, max_num_iterations: int = 10) -> float:
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
            all_steps += this_step
            #print(f"N[{i+1}]=\t{this_step:.3f} \tweight: {this_step * (i + 1):.3f}")
            break
        
        #print(f"N[{i+1}]=\t{this_step:.3f} \tweight: {this_step * (i + 1):.3f}")
        # add it
        total_dist += this_step * (i + 1)
        all_steps += this_step

    #print(f"Total Weight: {total_dist:.3f} / {N} \tRemainder: {left}")
    return total_dist / N

def est_avg_dist(N: List[int], M: List[List[int]], o: int, max_num_iterations: int = None) -> List[float]:
    #print("call est_avg_dist")
    # given
    # the origin subgraph, o
    # the number of nodes in subgraph i, N[i], 
    # the number of edges between subgraph i and subgraph j, M[i][j], 
    # we get estimated distance to a node in any subgraph via dynamic programming into D
    if len(N) != len(M): raise ValueError(f"Sizes of N ({len(N)}) and M {len(M)} do not match on first dimension of M!")
    for i in range(len(M)):
        if len(N) != len(M[i]): raise ValueError(f"Sizes of N {len(N)} and element of M, M[{i}] ({len(M[i])}), do not match!")
        if len(M) != len(M[i]): raise ValueError(f"Sizes of M ({len(M)}) and an element of M, M[{i}] ({len(M[i])}), do not match!")
    if o < 0: raise ValueError(f"Origin o ({o}) is negative!")
    if o >= len(N): raise ValueError(f"Origin o ({o}) is greater than maximum value based on N and M, {len(N) - 1}!")
    if max_num_iterations == None: max_num_iterations = 10 + 5 * len(N)

    # TODO: Check 0 <= M[i][j] <= N[i] * N[j] and 0 <= M[i][i] <= N[i] * (N[i]-1)

    # initialization
    dist_sum = [0 for _ in N]
    n_sum_prev = [0 for _ in N]
    n_prev = [0 for _ in N]
    n_now = [0 for _ in N]
    done = [False for _ in N]
    n_now[o] = 1 # origin

    # d represents how far the neighbor degree is from origin
    for d in range(max_num_iterations):
        # iterating
        n_prev = n_now
        # summing into sum of previous
        for k in range(len(N)): n_sum_prev[k] += n_prev[k]
        # clearing now values
        n_now = [0 for _ in N]

        for k in range(len(N)):
            if done[k]: continue
            # finding n_now[k]
            unadjusted_sum = 0
            for i in range(len(N)):
                unadjusted_sum += M[i][k] * (n_prev[i] / N[i])
            # adjustment_sum = n_sum_prev[k]
            n_now[k] = unadjusted_sum - n_sum_prev[k] # adjustment_sum

            # checking if done
            if n_now[k] > N[k] - n_sum_prev[k]:
                n_now[k] = N[k] - n_sum_prev[k]
                done[k] = True

            # add to distance sum
            dist_sum[k] += n_now[k] * (d+1)
            

        #print(f"N t={d+1}: ", end="")
        #for i in range(len(N)):
        #    print(f"{n_now[i]:.3f} \t", end="")
        #print()

    for i in range(len(N)):
        dist_sum[i] /= N[i]

    return dist_sum

def est_avg_dists(N, M):
    print("call est_avg_dists")
    return [est_avg_dist(N, M, i) for i in range(len(N))]

def get_avg_dists(G: nx.DiGraph, groups: list[list[int]]) -> list[list[float]]:
    print("call get_avg_dists")
    avg_dists = [[0 for _ in range(len(groups))] for _ in range(len(groups))]

    # it looks like its N^4, but it's actually N^2 ;)
    for i in range(len(groups)):
        for j in range(len(groups)):
            for u in groups[i]:
                for v in groups[j]:
                    if u == v: continue
                    avg_dists[i][j] += nx.dijkstra_path_length(G, u, v)

    for i in range(len(groups)):
        for j in range(len(groups)):
            num_pairs = len(groups[i]) * len(groups[j])
            if i == j: num_pairs -= len(groups[i])
            avg_dists[i][j] /= num_pairs

    return avg_dists

def get_random_mininet_description(slo = 2, shi = 10, nlo = 50, nhi = 100, mep = 1.5, mp = 0.5):
    S = random.randint(slo, shi)
    print(f"call get_random_mininet_description with S={S}")
    N = [random.randint(nlo // S, (nhi+1) // S) for _ in range(S)]
    M = [[0 for _ in N] for _ in N]
    for i in range(len(N)):
        for j in range(len(N)):
            if i == j: 
                mmax = round(N[i] * (N[i] - 1) * mp)
            else: 
                mmax = round(N[i] * N[j] * mp)
            mmin = round((N[i] + N[j]) * mep)

            if mmin >= mmax: M[i][j] = mmin
            else: M[i][j] = random.randint(mmin, mmax)
                
    return N, M

if __name__ == "__main__":
    
    print(est_avg_dist_internal(100, 200))