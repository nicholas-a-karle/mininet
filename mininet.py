
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
import numpy as np

class mininet(nx.DiGraph):
    # standard initialization
    def __init__(self):
        super().__init__()

        # max iterations for estimations
        self.max_iters = {
            "dist_base": 10,
            "dist_per_node": 5
        }

    def get_subgraph_size(self, group):
        return self[group]["size"]
    
    def get_num_edges(self, group1, group2):
        return self.edges[group1][group2]["edges"]

    def node_distances(self, node):
        # input checking
        if (not (0 <= node < len(self))): raise ValueError(f"Node {node} does not exist in {self}!")

        # initializations
        dist_sum = np.zeros(len(self))
        n_sum_prev = np.zeros(len(self))
        n_prev = np.zeros(len(self))
        n_now = np.zeros(len(self))
        done = np.zeros(len(self))

        # first operation
        n_now[node] = 1

        # the loop
        # d represents the degree of the neighbor, distance
        for d in range(self.max_iters['dist_base'] + self.max_iters['dist_per_node'] * len(self)):
            # iteration operations
            n_prev = n_now
            n_sum_prev += n_prev
            n_now = np.zeros(len(self))

            for k in range(len(self)):
                if done[k]: continue

                # summing and subtracting
                unadj_sum = 0
                for i in range(len(self)):
                    unadj_sum += self.edges[i][k]['edges'] * (n_prev[i] / self[i]['size'])
                n_now[k] = unadj_sum - n_sum_prev[k]

                # check
                if n_now[k] > self[k]['size'] - n_sum_prev[k]:
                    n_now[k] = self[k]['size'] - n_sum_prev[k]
                    done[k] = True

            # add to distance sum
            dist_sum += (n_now * (d+1))
        
        # finish
        for i in range(len(self)):
            dist_sum[i] /= self[i]['size']

        return dist_sum


