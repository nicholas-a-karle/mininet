# Centrality
    This describes the math behind the centrality estimates in mininet

# Out Degree Centrality
    Mininet gives us this information
    N the number of nodes in each subgraph
    M the number of edges between each subgraph
    N[i] being the number of nodes in the ith subgraph
    M[i][j] being the number of edges between the ith and jth subgraph where i can equal j

    The average number of edges connecting a node in the ith subgraph to a node in the jth subgraph is:

    M[i][j] / N[i]

    Therefore degree centrality of a node in subgraph i is equal to the sum of that formula for all j where 0 <= j <= len(N or M)

# In Degree Centrality
    Given the above, we can simply find the average number of edges from subgraph j going to subgraph i

    This is equal to M[j][i] / N[i]

# Closeness Centrality
    The distance estimate algorithm:

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

    Can be changed to provide the centrality measure

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
