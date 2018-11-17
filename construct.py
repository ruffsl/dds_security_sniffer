from IPython.display import display, IFrame, Image, Markdown, SVG
import os
import sys
import networkx as nx
import xml.etree.ElementTree as ET
import itertools

def getAllXMLFiles(path):
    files = []
    for filename in os.listdir(path):
        if filename.endswith('.xml'):
            files.append(os.path.join(path, filename))
    return files

# Three assumptions are made on xml permission file.
# 1. Default rule is DENY
# 2. There is no deny_rule
# 3. There is no regex
def parseXML(f, G, topics):
    root = ET.parse(f).getroot()
    grants = root.findall("./permissions/grant")
    for grant in grants:
        subject = grant.findall("./subject_name")[0].text
        if subject not in G:
            G.add_node(subject)
        validity = grant.findall("./validity")[0]
        if validity and validity.findall("./not_before"):
            G.node[subject]['not_before'] = validity.findall("./not_before")[0].text
        if validity and validity.findall("./not_after"):
            G.node[subject]['not_after'] = validity.findall("./not_after")[0].text
        allow_rule = grant.findall("./allow_rule")
        if allow_rule:
            allows = grant.findall("./allow_rule")[0].findall("./subscribe/topics/topic")
            if allows:
                for allow in allows:
                    topic = allow.text
                    if topic not in topics:
                        topics.add(topic)
                        G.add_node(topic)
                    G.add_edge(topic, subject)
            allowp = grant.findall("./allow_rule")[0].findall("./publish/topics/topic")
            if allowp:
                for allow in allowp:
                    topic = allow.text
                    if topic not in topics:
                        topics.add(topic)
                        G.add_node(topic)
                    G.add_edge(subject, topic)
        
def addNode(G, metadata, topics):
    # Add nodes of the network as vertices
    for node in metadata.keys():
        G.add_node(node, allow_sub=str(metadata[node]['allow_sub']), allow_pub=str(metadata[node]['allow_pub']), not_before=metadata[node]['not_before'], not_after=metadata[node]['not_after'], bipartite=0)
    #Add topics of the network as vertices
    for t in topics:
        G.add_node(t, bipartite=1)

def construct(G, metadata, topics):
    nodes = set(G) - topics
    # Build edges between nodes and topics
    for node in nodes:
        for topic in topics:
            pass
    for n, m in itertools.permutations(G.nodes, 2):
        for perm in metadata[n]['allow_pub']:
            for p in metadata[m]['allow_sub']:
                if p == perm:
                    G.add_edge(n, m)

def plot_graph_figure(G, file_name, view='png'):
    A = nx.nx_agraph.to_agraph(G)
    A.add_subgraph()
    if view is 'pdf':
        A.draw(file_name + '.' + 'pdf', prog='dot')
        display(IFrame(file_name + '.' + view, width=950, height=300))
    elif view is 'png':
        A.draw(file_name + '.' + 'png', prog='dot')
        A.draw(file_name + '.' + 'pdf', prog='dot')
        display(Image(file_name + '.' + view))
    elif view is 'svg':
        A.draw(file_name + '.' + 'svg', prog='dot')
        display(SVG(file_name + '.' + view))
    else:
        raise ValueError("No view option: {}".format(view))

if __name__ == '__main__':
    path = sys.argv[1]
    files = getAllXMLFiles(path)
    G = nx.MultiDiGraph()
    topics = set()
    for f in files:
        parseXML(f, G, topics)
    #addNode(G, metadata, topics)
    #construct(G, metadata, topics)
    #nx.write_graphml(G, 'g.xml')
    plot_graph_figure(G, 'G')
