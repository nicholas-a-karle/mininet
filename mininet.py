
# mininet
# 
# idea is to treat nodes as members of subgraphs
# the subgraphs will then have descriptors such as
#   1. Intra-subgraph Edge Density / Frequency
#   2. Inter-subgraph Edge Density / Frequency
# 
# metrics will then be calculated to approximate the represented graph's actual metrics
# 
# the idea of this is that it can be adjusted to meet memory/accuracy/time requirements
#   the most simple will be a pair of numbers (N, M) representing |V| and |E| respectively
#   next up, we have those metrics for many groups S=[(N, M), (N, M), ...]
#   then we start measuring the effect of individual bridges ***
#
#
# *** not yet implemented

import random
from typing import List
import networkx as nx
import community
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

        self.node_sg_dict = {}

    def add_subgraph(self, nodes: List[int] = []):
        nu = len(self)
        self.add_node(len(self), size=len(nodes), nodes=nodes)
        for old in range(len(self) - 1):
            self.add_edge(old, nu, edges=0)
            self.add_edge(nu, old, edges=0)
    
    # helper method unlikely to be used
    def uppdate_node_sg_dict(self):
        self.node_sg_dict = {}
        for group in self:
            for node in group['nodes']:
                self.node_sg_dict[node] = group
    
    def all_subgraph_distances(self) -> List[List[float]]:
        dists = []
        for sg in self:
            dists.append(self.calc_subgraph_distances(sg))
        return np.array(dists)

    def subgraph_distances(self, sg) -> List[float]:
        # input checking
        if (not (0 <= sg < len(self))): raise ValueError(f"Subgraph {sg} does not exist in {self}!")

        # initializations
        dist_sum = np.zeros(len(self))
        n_sum_prev = np.zeros(len(self))
        n_prev = np.zeros(len(self))
        n_now = np.zeros(len(self))
        done = np.zeros(len(self))

        # first operation
        n_now[sg] = 1

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
    
    def subgraph_closeness_centrality(self, sg) -> List[float]:
        # input checking
        if (not (0 <= sg < len(self))): raise ValueError(f"Subgraph {sg} does not exist in {self}!")

        # initializations
        dist_sum = np.zeros(len(self))
        n_sum_prev = np.zeros(len(self))
        n_prev = np.zeros(len(self))
        n_now = np.zeros(len(self))
        done = np.zeros(len(self))

        # first operation
        n_now[sg] = 1

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
        sum_dist_sum = sum(dist_sum)
        
        return 1 / sum_dist_sum

    def subgraph_density(self, sg1: int, sg2: int) -> float:
        # return the chances that the distance between these two is 1
        if sg1 == sg2:
            return self.edges[sg1][sg2]['edges'] / (self[sg1]['size'] * (self[sg2]['size']-1))
        else:
            return self.edges[sg1][sg2]['edges'] / (self[sg1]['size'] * self[sg2]['size'])
        
    def subgraph_out_degree_centrality(self, sg: int) -> float:
        degree_centrality = 0
        for i in range(len(self)):
            degree_centrality += self.edges[sg][i]['edges'] / self[sg]['size']
        return degree_centrality

    def subgraph_in_degree_centrality(self, sg: int) -> float:
        degree_centrality = 0
        for i in range(len(self)):
            degree_centrality += self.edges[i][sg]['edges'] / self[sg]['size']
        return degree_centrality

    def subgraph_total_degree_centrality(self, sg: int) -> float:
        return self.subgraph_in_degree_centrality(self, sg) + self.subgraph_out_degree_centrality(self, sg)

    def find_node_subgraph(self, node: int) -> int:
        return self.node_sg_dict[node]
    
    def convert_to_graph(self) -> nx.DiGraph:
        G = nx.DiGraph()
        n = 0
        for group in self:
            for node in group['nodes']:
                G.add_node(node)

        for g1 in self:
            for g2 in self:
                for i in range(self.edges[g1][g2]['edges']):
                    u = 0
                    v = 0
                    while u == v or G.has_edge(u, v):
                        u = random.choice(g1['nodes'])
                        v = random.choice(g2['nodes'])
                    G.add_edge(u, v)
        
        return G

    def create_from_graph(self, G: nx.DiGraph):
        self.clear()
        self.node_sg_dict = {}
        groups = list(community.best_partition(G.to_undirected()))

        for group in groups:
            self.add_subgraph(nodes = group)

        
        



