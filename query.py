import random
import argparse
import pickle
import networkx as nx

# TODO: need modification. Given a single node in the graph, find all nodes that can be reached from the given node.
def findTargets(G, topics, source):
    length = dict(nx.single_source_shortest_path_length(G, source))
    targets = length.keys() - topics
    targets.remove(source)
    return targets

# TODO: need modification. Given a single node in the graph, find all nodes that can reach to it.
def findSources(G, topics, target):
    length = dict(nx.single_target_shortest_path_length(G, target))
    sources = length.keys() - topics
    sources.remove(target)
    return sources

# Mock function that checks whether there is really a path or not. A, B are the path of permission files.
def mockCheck(A, B):
    if random.choice([0, 1]):
        return True
    else:
        return False

# Given a source and a destination node, find whether there exists a path originating from source to destination. If such a path exists, returns the nodes in sequence. Otherwise, returns false.
def checkReachability(G, src, dest, perm_map):
    while True:
        try:
            path = nx.shortest_path(G, source=src, target=dest)
        except nx.NetworkXNoPath:
            return False
        found = True
        for i in range(len(path)-1):
            if not mockCheck(perm_map[path[i]], perm_map[path[i+1]]):
                found = False
                G.remove_edge(path[i], path[i+1])
        if found:
            return path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", help="specify target node label")
    parser.add_argument("-s", "--source", help="specify source node label")
    args = parser.parse_args()

    G = nx.read_graphml('./serializedG.graphml')
    with open('data.pickle', 'rb') as f:
        perm_map = pickle.load(f)
    if args.source and args.target:
        print("Path from {} to {}: {}".format(args.source, args.target, checkReachability(G, args.source, args.target, perm_map)))
