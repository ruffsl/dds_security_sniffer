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

def parseXML(f, metadata):
    root = ET.parse(f).getroot()
    grants = root.findall("./permissions/grant")
    for grant in grants:
        subject = grant.findall("./subject_name")[0].text
        if subject not in metadata:
            metadata[subject] = dict()
            # The first nested inner list is sub topic, and the second one is pub topics
            metadata[subject]['allow_sub'] = []
            metadata[subject]['allow_pub'] = []
            metadata[subject]['deny_sub'] = []
            metadata[subject]['deny_pub'] = []
            metadata[subject]['default'] = "DENY"
        validity = grant.findall("./validity")[0]
        if validity and validity.findall("./not_before"):
            metadata[subject]['not_before'] = validity.findall("./not_before")[0].text
        if validity and validity.findall("./not_after"):
            metadata[subject]['not_after'] = validity.findall("./not_after")[0].text
        allow_rule = grant.findall("./allow_rule")
        if allow_rule:
            allows = grant.findall("./allow_rule")[0].findall("./subscribe/topics/topic")
            if allows:
                for allow in allows:
                    metadata[subject]['allow_sub'].append(allow.text)
            allowp = grant.findall("./allow_rule")[0].findall("./publish/topics/topic")
            if allowp:
                for allow in allowp:
                    metadata[subject]['allow_pub'].append(allow.text)
        deny_rule = grant.findall("./deny_rule")
        if deny_rule:
            denys = grant.findall("./deny_rule")[0].findall("./subscribe/topics/topic")
            if denys:
                for deny in denys:
                    metadata[subject]['deny_sub'].append(deny.text)
            denyp = grant.findall("./deny_rule")[0].findall("./publish/topics/topic")
            if denyp:
                for deny in denyp:
                    metadata[subject]['deny_pub'].append(deny.text)
        default = grant.findall("./default")
        if default:
            metadata[subject]['default'] = default[0].text

def addNode(G, metadata):
    for node in metadata.keys():
        G.add_node(node, allow_sub=str(metadata[node]['allow_sub']), allow_pub=str(metadata[node]['allow_pub']), deny_sub=str(metadata[node]['deny_sub']), deny_pub=str(metadata[node]['deny_pub']), not_before=metadata[node]['not_before'], not_after=metadata[node]['not_after'], default=metadata[node]['default'])

def construct(G, metadata):
    for n, m in itertools.permutations(G.nodes, 2):
        for perm in metadata[n]['allow_pub']:
            for p in metadata[m]['allow_sub']:
                if p == perm:
                    G.add_edge(n, m)

if __name__ == '__main__':
    path = sys.argv[1]
    files = getAllXMLFiles(path)
    G = nx.MultiDiGraph()
    metadata = dict()
    for f in files:
        parseXML(f, metadata)
    addNode(G, metadata)
    construct(G, metadata)
    nx.write_graphml(G, 'g.xml')
