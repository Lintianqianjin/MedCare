import networkx as nx
from tqdm import tqdm
import chardet
import matplotlib.pyplot as plt
# import scipy as sp
import scipy.sparse as sp
import numpy as np
import json

def detectCode(filepath):
    with open(filepath, 'rb') as file:
        data = file.read(2000)
        dicts = chardet.detect(data)
    return dicts["encoding"]


class drugsGraph():
    # 无多重边 无向图
    def __init__(self):
        self.graph = nx.Graph()
        pass

    def addDrugsIngredient(self,filepath):
        # 要求数据格式两列，第一列为药，第二列为成份
        # 制表符隔开
        encoding = detectCode(filepath)
        data = open(filepath,'r',encoding=encoding)
        for index,line in tqdm(enumerate(data)):
            drug,ingre = line.strip().split('\t')
            self.graph.add_node(drug)
            self.graph.add_node(ingre)
            self.graph.add_edge(drug,ingre)

    def addIngredientInteraction(self,filepath):
        # 要求数据格式两列，第一列为成份1，第二列为成份2
        # 逗号隔开
        encoding = detectCode(filepath)
        data = open(filepath, 'r', encoding=encoding)
        for index, line in tqdm(enumerate(data)):
            ingre_1, ingre_2 = line.strip().split(',')[:2]
            self.graph.add_node(ingre_1)
            self.graph.add_node(ingre_2)
            self.graph.add_edge(ingre_1, ingre_2)

    def showGraph(self):
        nx.draw(self.graph)
        plt.show()

    def saveAdjMatrix(self,filepath= None ,type='numpy'):
        adj_csr = nx.adjacency_matrix(dg.graph)
        adj_np = adj_csr.toarray().astype(np.int32)
        print(adj_np.dtype)
        if filepath is not None:
            np.savetxt(filepath,adj_np, fmt='%d',delimiter="\t")
        return adj_np

    def saveNodesList(self,filepath= None):
        nodes = self.graph.nodes()
        nodes_dict = dict()
        for index,node in enumerate(nodes):
            nodes_dict[index] = node

        print(nodes)

        if filepath is not None:
            with open(filepath,'w') as f:
                f.write(json.dumps(nodes_dict,ensure_ascii=False))
        return nodes


if __name__ == '__main__':
    pass
    ### drugsGraph 开始###
    drug_ingre_filepath = r'metrix(1).txt'
    ingre_interaction = r'相互关系.csv'
    dg = drugsGraph()
    dg.addDrugsIngredient(drug_ingre_filepath)
    # print(dg.graph.nodes())
    # print(dg.graph.edges())
    print('仅添加药物与成份')
    print("number of edges:", dg.graph.number_of_edges())
    print("number of nodes:", dg.graph.number_of_nodes())
    dg.addIngredientInteraction(ingre_interaction)
    print('添加了成份作用')
    print("number of edges:", dg.graph.number_of_edges())
    print("number of nodes:", dg.graph.number_of_nodes())

    # print(dg.graph.adj)

    adj = dg.saveAdjMatrix(filepath='drugsGraph.txt')
    nodes = dg.saveNodesList(filepath='nodesList.json')
    print(adj)
    print(type(adj))
    # dg.showGraph()
    ### drugsGraph 结束###