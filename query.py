import networkx as nx
import argparse

# Given a bipartite directed graph G, find all topic nodes identified by label color as green. 
def findTopics(G):
    return [x for x, y in G.nodes(data=True) if y['color'] == 'green']

# Given a single node in the graph, find all nodes that can be reached from the given node.
def findTargets(G, topics, source):
    length = dict(nx.single_source_shortest_path_length(G, source))
    targets = length.keys() - topics
    targets.remove(source)
    return targets

# Given a single node in the graph, find all nodes that can reach to it.
def findSources(G, topics, target):
    length = dict(nx.single_target_shortest_path_length(G, target))
    sources = length.keys() - topics
    sources.remove(target)
    return sources

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", help="specify target node label")
    parser.add_argument("-s", "--source", help="specify source node label")
    args = parser.parse_args()

    G = nx.read_graphml('./serializedG.graphml')
    topics = findTopics(G)
    if args.source:
        print("From source node {}: {}".format(args.source, findTargets(G, topics, args.source)))
    if args.target:
        print("From target node {}: {}".format(args.target, findSources(G, topics, args.target)))
    if not args.source and not args.target:
        print("Topics involved:", topics)
