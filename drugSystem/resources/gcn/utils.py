import scipy.sparse as sp
import numpy as np

class graphProcessing():

    def __init__(self):
        pass

    def normalize_adj(self,adj):
        """邻接矩阵标准化"""
        adj = sp.coo_matrix(adj)
        # 度矩阵对角线元素
        rowsum = np.array(adj.sum(1))
        d_inv_sqrt = np.power(rowsum, -0.5).flatten()
        d_inv_sqrt[np.isinf(d_inv_sqrt)] = 0.
        d_mat_inv_sqrt = sp.diags(d_inv_sqrt)
        # D**-0.5*Adj*D**-0.5
        return adj.dot(d_mat_inv_sqrt).transpose().dot(d_mat_inv_sqrt)

    def addSelfCirculation(self,adj):
        for index,row in enumerate(adj):
            adj[index][index] = 1

        return adj

    def preprocess_features(self,features):
        """特征矩阵标准化"""
        rowsum = np.array(features.sum(1))
        r_inv = np.power(rowsum, -1).flatten()
        r_inv[np.isinf(r_inv)] = 0.
        r_mat_inv = sp.diags(r_inv)
        features = r_mat_inv.dot(features)
        return features


if __name__ == '__main__':
    pass
    # gen = generator()
    # adj = gen.genPostiveSamplesID()
    # print(adj)
    # for index,pari in enumerate(adj):
    #     if pari[0] == pari[1]:
    #         print(pari)
    #
    #         print(index)
    #
    # negIDs = gen.genNegativeSamplesID()
    # for index,pari in enumerate(negIDs):
    #
    #     print(pari)
    #
    #     print(index)