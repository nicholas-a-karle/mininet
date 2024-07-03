# Estimating Distance Between Nodes Within a Subgraph
    Estimating distance within the subgraph can be done by finding the average ith degree number of neighbors within that subgraph from any node
    Where N[0] = 1 <=> the origin node
    And there are N nodes in the subgraph and M edges
    We can run a dynamic programming solution such as

    Params:
    N: int
    M: int

    Init:
    N[] = int []
    N[0] = 1
    total_dist = 0
    i = 1

    Do:
    while True: // can be limited
        N[i] = (N[i-1] * M / N) * (1 - sum(N[0 ... i-1]) / N)

        if sum(N[0 ... i]) > N:
            N[i] = N - sum(N[0 ... i-1])
            total_dist += N[i] * i
            break
        total_dist += N[i] * i
    
    return total_dist / N

# Estimating Distance Between Nodes in Separate Subgraphs
    We can work with a similar mindset
    On Subgraph 0 to Subgraph 1
    With N0 nodes in subgraph 0 and N1 nodes in subgraph 1
    With M0/M1 internal edges and I inter-subgraph edges
    
      sg0             sg1
    (N0, M0) - I -> (N1, M1)

# What is Missed by these Function
    It is very possible that a graph such that there are two subgraphs
    S0 has a density of 0.5, with 100 members
    S1 has a density of 0.5, with 100 members