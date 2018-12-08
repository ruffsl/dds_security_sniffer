import os
import sys
import random
import argparse
import pickle
import networkx as nx

# Given a single node in the graph, find all nodes that can be reached from the given node.
def findTargets(G, source, perm_map, check_func):
    res = set()
    try:
        for nei in G.neighbors(source):
            if check_func(perm_map[source], perm_map[nei]):
                res.add(nei)
        return returnDict(res, perm_map)
    except AttributeError:
        return res

# Given a single node in the graph, find all nodes that can reach to it.
def findSources(G, target, perm_map, check_func):
    res = set()
    try:
        for nei in G.Predecessors(target):
            if check_func(perm_map[nei], perm_map[target]):
                res.add(nei)
        return returnDict(res, perm_map)
    except AttributeError:
        return res

# Mock function that checks whether there is really a path or not. A, B are the path of permission files.
def mockCheck(A, B):
    if random.choice([0, 1]):
        return True
    else:
        return False

# Given a source and a destination node, find whether there exists a path originating from source to destination. If such a path exists, returns the nodes in sequence. Otherwise, returns false.
def checkReachability(G, src, dest, perm_map, check_func):
    while True:
        try:
            path = nx.shortest_path(G, source=src, target=dest)
        except nx.NetworkXNoPath:
            return False
        found = True
        for i in range(len(path)-1):
            if not check_func(perm_map[path[i]], perm_map[path[i+1]]):
                found = False
                G.remove_edge(path[i], path[i+1])
        if found:
            return returnDict(path, perm_map)

def returnDict(l, perm_map):
    res = dict()
    for n in l:
        res[n] = get_ip(perm_map, n)
    return res

def check_route(path, source, target, check_func):
    G = nx.read_graphml(os.path.join(path, 'serializedG.graphml'))
    with open(os.path.join(path, 'data.pickle'), 'rb') as f:
        perm_map = pickle.load(f)
    if source and target:
        print("Path from {} to {}: {}".format(source, target, checkReachability(G, source, target, perm_map, check_func)))
    elif source:
        print("Nodes to take over from source {}: {}".format(source, findTargets(G, source, perm_map, check_func)))
    elif target:
        print("Nodes to take over from target {}: {}".format(target, findSources(G, target, perm_map, check_func)))

def get_ip(perm_map, subject):
    ip_str = os.path.basename(perm_map[subject])
    return ip_str.split('_')[0]

def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", help="specify target node label")
    parser.add_argument("-s", "--source", help="specify source node label")
    parser.add_argument('--path', required=True)
    args = parser.parse_args(argv)
    check_route(path=args.path, source=args.source, target=args.target, check_func=mockCheck)

if __name__ == "__main__":
    main()
