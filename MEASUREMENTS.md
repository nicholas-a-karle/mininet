# Measurements
    This file is a compendium of measurements from the class mininet
    |V|  = V
    |E|  = E
    |NV| = N
    |NE| = M
    O|NV| / O(V) = K

## Distance via Subgraph-Subgraph Size and Number of Edges (Subgraph -> All)
    Time Complexity:
    I * S^2 + S
    I = 10 + 5 * S
    O(10 + 5*S) = S
    O( S^3 + S )

    vs.
    Dijkstra's 

    O( N^2 ) or O( (N+M) * log(N) )
    N^2 vs. S^3 + S = (N/K)^3 + (N/K)
    Let us ignore N/K
    N^2 vs. N^3 / K^3
    1 vs. N / K^3

    For Mininet to be more effective, K^3 must be greater than N
    K^3 > N
    So minimum K is cbrt(N)
    S ~ N/K, so maximum S  is N^(2/3) = N^2/N^3