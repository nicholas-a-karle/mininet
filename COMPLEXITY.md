# Complexity
    The point of this library is to reduce the complexity of graph-based work
    It does this largely by sacrificing the accuracy of the data
    This is useful for randomized simulations and estimations of actual data
    For the large part, the principles here can be reapplied if the structure of the graph is well understood

# Space Complexity
    Given the average number of nodes in each subgraph K, we can calculate the improvement in memory efficiency mininet / graph
    The number of subgraphs becomes |S| = |V| / K
    We reduce the number of edges from |V|^2 or |E| to |S|^2
    0 <= |E| <= |V|^2
    |S|^2 = |V|^2 / K^2

    |E| = p|V|^2
    |S|^2 = |V|^2 / K^2
    p|V|^2 = |V|^2 / K^2
    p = 1/K^2

    An edgelist version becomes more memory efficient when density is less than 1/K^2
    Of course NetworkX and MiniNet store more info than the basics, so it is a little more complicated

# Time Complexity
    Time complexity depends on the method and comparing the two
    Many of these methods could be easily applied to a normal graph as well
    I'll keep these in the file "MEASUREMENTS.md"
    