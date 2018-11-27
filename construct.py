from IPython.display import display, IFrame, Image, Markdown, SVG
import os
import sys
import fnmatch
import xml.etree.ElementTree as ET
import itertools
import networkx as nx

class DisjointSet:
    def __init__(self, topics):
        self.data = dict()
        self.rank = dict()
        for topic in topics:
            self.data[topic] = topic
            self.rank[1]

    def root(topic):
        if self.data[topic] == topic:
            return topic
        else:
            self.data[topic] = find(self.data[topic])
            return self.data[topic]

    def find(t1, t2):
        return root(t1) == root(t2)

    def union(t1, t2):
        r1 = root(t1)
        r2 = root(t2)
        if r1 != r2:
            if self.rank[r1] < self.rank[r2]:
                self.data[r1] = r2
            elif self.rank[r1] > self.rank[r2]:
                self.data[r2] = r1
            else:
                self.data[r2] = r1
                self.rank[r1] += 1

def get_all_xml_files(path):
    files = []
    for filename in os.listdir(path):
        if filename.endswith('.xml'):
            files.append(os.path.join(path, filename))
    return files

# Three assumptions are made on xml permission file.
# 1. Default rule is DENY
# 2. There is no deny_rule
# 3. There is no expression
def parse_xml(f, G, topics):
    root = ET.parse(f).getroot()
    grants = root.findall("./permissions/grant")
    for grant in grants:
        subject = grant.findtext("./subject_name")
        if subject not in G:
            G.add_node(subject, color='red')
        validity = grant.find("./validity")
        if validity and validity.find("./not_before"):
            G.node[subject]['not_before'] = validity.findtext("./not_before")
        if validity and validity.find("./not_after"):
            G.node[subject]['not_after'] = validity.findtext("./not_after")
        allow_rules = grant.findall("./allow_rule")
        for ar in allow_rules:
            allows = ar.findall("./subscribe/topics/topic")
            for allow in allows:
                topic = allow.text
                if topic not in G:
                    topics.add(topic)
                    G.add_node(topic, color='green')
                G.add_edge(topic, subject)
            allowp = ar.findall("./publish/topics/topic")
            for allow in allowp:
                topic = allow.text
                if topic not in G:
                    topics.add(topic)
                    G.add_node(topic, color='green')
                G.add_edge(subject, topic)

def connect_topic_nodes(G, topics):
    ds = DisjointSet(topics)
    for i, j in itertools.combinations(topics, 2):
        if fnmatch.fnmatch(i, j):
            ds.union(i, j)
            G.add_edge(i, j)
            G.add_edge(j, i)
    return ds

def contract_nodes(G, topics, ds):
    for i, j in itertools.combinations(topics, 2):
        if ds.find(i, j):
            nx.contracted_nodes(G, i, j)

def plot_graph_figure(G, file_name, view='pdf'):
    A = nx.nx_agraph.to_agraph(G)
    A.add_subgraph()
    if view == 'pdf':
        A.draw(file_name + '.' + 'pdf', prog='dot')
        display(IFrame(file_name + '.' + view, width=950, height=300))
    elif view == 'png':
        A.draw(file_name + '.' + 'png', prog='dot')
        A.draw(file_name + '.' + 'pdf', prog='dot')
        display(Image(file_name + '.' + view))
    elif view == 'svg':
        A.draw(file_name + '.' + 'svg', prog='dot')
        display(SVG(file_name + '.' + view))
    else:
        raise ValueError("No view option: {}".format(view))

if __name__ == '__main__':
    path = sys.argv[1]
    files = get_all_xml_files(path)
    G = nx.MultiDiGraph()
    topics = set()
    for f in files:
        parse_xml(f, G, topics)
    plot_graph_figure(G, 'G')
    ds = connect_topic_nodes(G, topics)
    plot_graph_figure(G, 'connectedG')
    contract_nodes(G, topics, ds)
    plot_graph_figure(G, 'contractedG')
    nx.write_graphml_lxml(G, 'serializedG.graphml')
