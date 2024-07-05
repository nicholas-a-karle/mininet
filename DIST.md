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

    We extend the single-subgraph version like so

    Params:
    N: List[int]
    M: List[List[int]]
    o: int

    Init:
    dist_sum = [0 ... 0]: len = len(N)
    n_sum_prev = [0 ... 0]: len = len(N)
    n_prev = [0 ... 0]: len = len(N)
    n_now = [0 ... 0]: len = len(N)
    done = [0 ... 0]: len = len(N)
    
    Do:
    n_now[o] = 1

    for d in range(some_maximum_value):

        // iteration operations
        n_prev = n_now
        n_sum_prev += n_prev
        n_now = [0 ... 0]: len = len(N)

        for each subgraph k:
            if done[k] flagged: continue
            
            sum = S(M[i, k] * (n_prev[i] / N[i])) for each sugraph i
            n_now[k] = sum - n_sum_prev[k]

            if n_now[k] overflows total:
                n_now[k] limited
                done[k] is flagged as True

        // add vectors    
        dist_sum[k] += n_now[k] * (d+1)


# What is Missed by these Function
    The single-subgraph version can have it's maximum error with calculations when M=2N
    Here it estimates avg_dist = 4.22

    The maximum avg_dist this can be is a straight line, where avg_dist ~ 33
    
    This is a 87% error