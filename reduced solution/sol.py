"""
Max Independent Set Approximation
Molloy - Nov 2025

Compute a greedy solution first then try and use
a weighted random selection method to try and improve
with whatever time remains.

"""
import argparse
import copy
import random
import time

SAFETY = 2
SAFETY_LOOP=10


def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--t', action='store', type=int,
                        dest='timeToCompute', default=60, required=False,
                        help='number of seconds to run the approximation')
    parser.add_argument('--v', action='store_true',dest='verbose',required=False,
                        help='verbose')

    return parser.parse_args()    

def make_adj():
    adj = {}
    edge_count = int(input())
    for _ in range(edge_count):
            u,v = input().split()
            if u not in adj:
                adj[u] = set()
            if v not in adj:
                adj[v] = set()
            adj[u].add(v)
            adj[v].add(u)
    return adj

def compute_degree(adj):
    deg = [(len(adj[u]),u) for u in adj]
    deg.sort()
    return deg

def remove_vertex_from_adj(adj,u):
    # go down u's adj and remove any nodes
    for v in adj[u]:
        adj[v].remove(u)
        # if len(adj[v]) == 0:
        #     del adj[v]
    if u in adj:
        del adj[u]

def pure_greedy(adj):
    indset = set()
    working_adj = copy.deepcopy(adj)
    while len(working_adj) != 0:
        deg = compute_degree(working_adj)
        # remove lowest degree vertice and adjust adj
        u = deg[0][1]
        list_to_remove = [v for v in working_adj[u]]
        for v in list_to_remove:
           remove_vertex_from_adj(working_adj, v)

        if u in working_adj:
            del working_adj[u]
        indset.add(u)
    return indset

# select vertex randomly
# weight with inverse of its degree so that
# min degree vertices have a higher probability of being
# selected.
def choose_with_weights(adj):
    deg = compute_degree(adj)
    weights = [1/max(0.000001,vertexDegree) for vertexDegree,y in deg] # inverse the degree
    #print(deg,weights)
    x = random.choices(deg,weights=weights)
    return x[0]

def random_1(adj):
    # strategy is to pick vertex to add with weight proportional
    # to its degree

    indset = set()
    working_adj = copy.deepcopy(adj)
    while len(working_adj) != 0:
        deg_plus_vertex =  choose_with_weights(working_adj)
        u = deg_plus_vertex[1]
        list_to_remove = [v for v in working_adj[u]]
        for v in list_to_remove:
           remove_vertex_from_adj(working_adj, v)

        if u in working_adj:
            del working_adj[u]

        indset.add(u)

    return indset
def main():
    args = read_args()

    adj = make_adj()

    best_indset = pure_greedy(adj)
    if args.verbose:
        print('best from greedy is:', len(best_indset))
    start = time.time()
    time_for_loop = None
    while True:
        new_indset = random_1(adj)
        if len(new_indset) > len(best_indset):
            best_indset = new_indset
            if args.verbose:
                print('improvement found:', len(best_indset), time.time())
        if time_for_loop is None:
            time_for_loop = time.time() - start
                
        if start + args.timeToCompute - SAFETY  < time.time() + time_for_loop*SAFETY_LOOP:
            break

    print(best_indset)

main()