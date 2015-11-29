import copy
from operator import itemgetter
import operator
import random
import sys
import community
import matplotlib.pyplot as plt
import networkx as nx


def draw_graph(graph, communities, imageFile):
    rand_value = random.random()
    val_map={}

    for community in communities:
        a = 1
        b = 125000
        rand_no = random.randint(a, b)*5
        print rand_no
        for node in community:
            normalized_rand = rand_no
            val_map[node] = normalized_rand
        a = 543*normalized_rand
        b = 658*normalized_rand
    print val_map

    values = []
    for node in graph.nodes():
        values.append(val_map.get(node, 0.25))
    print values

    nx.draw_networkx(graph, cmap = plt.get_cmap('jet'), node_color = values)
    plt.axis('off')
    plt.savefig(imageFile)
    plt.show()

def get_betweenness(graph):
    return nx.edge_betweenness(graph)

def readFileToGraph(inputFile):
    inputFileObj = open(inputFile)
    graph = nx.Graph()

    for lineStr in inputFileObj:
        lineStr = lineStr.rstrip('\n')
        edgeList = lineStr.split(' ')
    
        #print edgeList
        graph.add_edge(int(edgeList[0]), int(edgeList[1]))
    return graph

def main():
    args_len = len(sys.argv)
    if (args_len != 3):
        print "Usage: python <source_file> <input_file> <image_file>"
        sys.exit()

    inputFile = sys.argv[1]
    #print "inputFile:", inputFile
    imageFile = sys.argv[2]

    graph = readFileToGraph(inputFile)
    #store a copy of the graph. Need it to draw plot the community graph
    graphCopy = graph.copy()
    no_of_nodes = nx.number_of_nodes(graph)
    #print no_of_nodes
    no_of_communities = 1
    max_modularity = -1
    #calculate betweenness
    
    while no_of_communities != no_of_nodes:

        graph_betweenness = get_betweenness(graph)
        #print graph_betweenness
        
        max_betweenness_edge = max(graph_betweenness.iteritems(), key = operator.itemgetter(1))[0]
        #print max_betweenness_edge
        
        graph.remove_edge(max_betweenness_edge[0], max_betweenness_edge[1])
        
        connected_comp = nx.connected_components(graph)
        #print connected_comp
        
        subgraph_list = []
        subgraphs_dict = {}
        
        count = 1
        for item in connected_comp:
            item_list = sorted(list(item))
            #print item_list
            subgraph_list.append(item_list)
            
            for node in item_list:
                subgraphs_dict[node] = count
            count = count + 1 
        #print subgraphs_dict
        
        modularity_val = community.modularity(subgraphs_dict, graph)
        #print modularity_val
        
        if (modularity_val > max_modularity):
            max_modularity = modularity_val
            subgraph_list = sorted(subgraph_list)
            communities = copy.deepcopy(subgraph_list)
            
        no_of_communities = no_of_communities + 1
        #print graph.edges()
        #print graph.nodes()
    communities = sorted(communities, key=itemgetter(0))
    print communities
    
    draw_graph(graphCopy, communities, imageFile)

if __name__ == "__main__":
    main()

