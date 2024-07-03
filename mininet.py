
# mininet
# 
# idea is to treat nodes as members of subgraphs
# the subgraphs will then have descriptors such as
#   1. Intra-subgraph Edge Density / Frequency
#   2. Inter-subgraph Edge Density / Frequency
# 
# metrics will then be calculated to approximate the represented graph's actual metrics
# 
# calculating intra-subgraph average distance
# 
# 
# 
# 
# 
# 

import networkx as nx

class mininet(nx.DiGraph):

    # standard initialization
    def __init__(self):
        super().__init__()

    def get_subgraph_size(self, group):
        return self[group]["size"]
    
    def get_num_edges(self, group1, group2):
        return self.edges[group1][group2]["edges"]

    def node_distance(self, node1, node2):
