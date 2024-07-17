# Multi-Mini-Net
    
    multimininet will be a version of mininet where each node can belong to multiple subgroups
    
    The goal of this is to semi-accurately simulate populations

    Here is an example:
    Age     Nodes
    0 -10   [...]
    10-20   [...]
    20-30   [...]
    ...     ...
    Income
    0-10    [...]
    20-30   [...]
    30-50   [...]
    50-70   [...]
    70-90   [...]
    ...     ...
    ...     and so on

    We can use these to get more accurate representations of data
    In this exact example we could recombine them to get subgroups based on Age-Income Pairing
    However, we could do a simulation of a school

    As such:
    Year    Nodes
    1       [...]
    2       [...]
    3       [...]
    4       [...]
    5+      [...]
    GPA     
    0.0-2.0 [...]
    2.0-2.4 [...]
    2.5-2.9 [...]
    3.0-3.4 [...]
    3.5-3.7 [...]
    3.8-3.9 [...]
    4.0     [...]
    Clubs   
    Soccer  [...]
    Robots  [...]
    Footy   [...]
    etc.

    In this example we can do the pairing with Year/GPA, but not clubs
    In theory we could, but given the number of Clubs |Clubs| we get !(|Clubs|) total groups just for clubs

    We need to find a way to accurately represent the edges between all these subgroups
    Between two subgroups where membership is not mutually exclusive we get a 2x2 matrix still

    N = [n0, n1]
    M = [
        [m00, m01],
        [m10, m11]
    ]
    
    However, since we're working down we can expand this to be a little bit better and add a shared with matrix
    
    S = [
        [s00, s01],
        [s10, s11]
    ] = [
        [n0, s01],
        [s10, n1]
    ]

    This matrix can replace the N vector such that N[i] = S[i, i]




