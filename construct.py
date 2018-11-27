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
# 3. There is no expression
def parseXML(f, G, topics):
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
    plot_graph_figure(G, 'G')
    nx.write_graphml_lxml(G, 'serializedG.graphml')
