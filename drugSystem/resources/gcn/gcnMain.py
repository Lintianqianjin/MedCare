import tensorflow as tf
import scipy.sparse as sp
import numpy as np
import tensorboard
import os
import regex as re
from utils import graphProcessing
import random
from tqdm import tqdm
import matplotlib.pyplot as plt

utils = graphProcessing()

def load_adj_data(graphFilepath):

    adj = np.loadtxt(graphFilepath,delimiter='\t',dtype=np.float32)
    # 返回有边的行列索引[（node1_ID,node2_ID）,...]
    csc = sp.coo_matrix(adj)
    # posNodesPair = np.vstack((csc.row, csc.col)).T

    # 返回有边的行列索引[（node1_ID,node2_ID）,...]

    adj_plus_selfCir = utils.addSelfCirculation(adj)
    normed_adj = utils.normalize_adj(adj_plus_selfCir)
    # print(type(normed_adj))
    return sp.csc_matrix.toarray(normed_adj),csc.row,csc.col

###初始化数据 开始###
adj,posRow,posCol = load_adj_data(graphFilepath = f'drugsGraph.txt')
# print(true_labels.shape)
# exit()
features = np.identity(adj.shape[0])
###初始化数据 结束###

# print(features)
# print(support)

### 定义超参数 开始###
mapLength = adj.shape[0]
gcnLayer_1_outputSize = 256
gcnLayer_2_outputSize = 256
gcnLayer_3_outputSize = 256
gcnLayer_4_outputSize = 256
gcnLayer_final_outputSize = 256
dense_outputSize = 256
dropout_keep_prob = 0.8
learning_rate = 0.01
x1_adj_input_shape = np.array([mapLength, mapLength],dtype=np.int64)
x2_features_input_shape = np.array([mapLength, mapLength],dtype=np.int64) # 一开始是onehot所以shape与邻接矩阵相同
### 定义超参数 结束###

def add_gcnLayer(adj,features,in_size,out_size,id,activation_function=None,isdropout = True,adj_sparse = False,features_sparse = False):
    # if adj_sparse:
    #     print('adj sparse')
    #     adj_ordered = tf.sparse_reorder(adj)
    #     adj = tf.sparse.to_dense(adj_ordered)
    # if features_sparse:
    #     print('features sparse')
    #     features_ordered = tf.sparse_reorder(features)
    #     features = tf.sparse.to_dense(features_ordered)
    # print(adj)
    # print(features)

    with tf.name_scope(f'GraphConvLayer_{id}'):
        with tf.name_scope(f'GraphConvLayer_W_{id}'):
            Weights = tf.Variable(tf.truncated_normal(shape=[in_size, out_size], mean=0, stddev=1,dtype=tf.float32),dtype=tf.float32)
        # with tf.name_scope(f'GraphConvLayer_B_{id}'):
        #     biases = tf.Variable(tf.zeros(shape=[1,out_size])+0.0001)
        with tf.name_scope(f'GraphConvLayer_propagate_{id}'):
            adjFeatures = tf.matmul(adj,features)
        with tf.name_scope(f'GraphConvLayer_conv_{id}'):
            Wx_plus_b = tf.matmul(adjFeatures,Weights)
            if isdropout:
                Wx_plus_b = tf.nn.dropout(Wx_plus_b, keep_prob)
            # Wx_plus_b = tf.matmul(adjFeatures,Weights) + biases
        if activation_function is None:
            outputs = Wx_plus_b
        else:
            outputs = activation_function(Wx_plus_b)
        return outputs

def add_denseLayer(features,in_size,out_size,id,isdoupout = True,activation_function=None):

    with tf.name_scope(f'DenseLayer_{id}'):
        with tf.name_scope(f'DenseLayer_W_{id}'):
            Weights = tf.Variable(tf.truncated_normal(shape=[in_size, out_size], mean=0.1, stddev=0.1,dtype=tf.float32),dtype=tf.float32)
        # with tf.name_scope(f'DenseLayer_B_{id}'):
        #     biases = tf.Variable(tf.zeros(shape=[1, out_size]) + 0.01)
        with tf.name_scope(f'DenseLayer_Wx_plus_b_{id}'):
            # Wx_plus_b = tf.matmul(features, Weights) + biases
            Wx_plus_b = tf.matmul(features, Weights)
            if isdoupout:
                Wx_plus_b = tf.nn.dropout(Wx_plus_b, keep_prob)
        if activation_function is None:
            outputs = Wx_plus_b
        else:
            outputs = activation_function(Wx_plus_b)
        return outputs

with tf.name_scope('Inputs'):
    x1_adj_input = tf.placeholder(tf.float32,name='adjMatrixInput')
    x2_features_input = tf.placeholder(tf.float32,name='nodesFeaturesMatrixInput')
    keep_prob = tf.placeholder(tf.float32,name='dropout')

# with tf.name_scope('PosNodesPairLabels'):
#     PosNodesPairLabel = tf.placeholder(tf.float32,shape=posNodesPair.shape,name='allNodesLabels')

gcn_layer_1 = add_gcnLayer(x1_adj_input,x2_features_input,id=1,
                           in_size=mapLength,out_size=gcnLayer_1_outputSize,
                           activation_function=tf.nn.tanh)

gcn_layer_2 = add_gcnLayer(x1_adj_input,gcn_layer_1,id=2,
                           in_size=gcnLayer_1_outputSize,out_size=gcnLayer_2_outputSize,
                           activation_function=tf.nn.tanh)

gcn_layer_3 = add_gcnLayer(x1_adj_input,gcn_layer_2,id=3,
                           in_size=gcnLayer_2_outputSize,out_size=gcnLayer_3_outputSize,
                           activation_function=tf.nn.tanh)

gcn_layer_final = add_gcnLayer(x1_adj_input,gcn_layer_2,id=4,
                               in_size=gcnLayer_3_outputSize,out_size=gcnLayer_final_outputSize,
                               activation_function=tf.nn.tanh)

denseLayer = add_denseLayer(gcn_layer_final,id=1,
                            in_size=gcnLayer_final_outputSize,out_size=dense_outputSize,
                            activation_function=tf.nn.tanh)

print('model constructed')

with tf.name_scope('curNegSampleList'):
    negSampleList = tf.placeholder(tf.int64,name='negSampleIDs')

with tf.name_scope('innerMatrix'):
    innerMat = tf.Variable(tf.truncated_normal(
                            shape=[gcnLayer_final_outputSize, gcnLayer_final_outputSize],
                            mean=0, stddev=1,dtype=tf.float32),name='innerMat',trainable=True,dtype=tf.float32)
    innerMat = tf.nn.dropout(innerMat,keep_prob)

with tf.name_scope('loss'):

    baseSamples = tf.gather(gcn_layer_final,indices=posRow,name='baseSamplesMatrix')
    posSamples_T = tf.transpose(tf.gather(gcn_layer_final,indices=posCol,
                                          name='posSamplesMatrix'),
                                name='transposed_posSamplesMatrix')
    negSamples_T = tf.transpose(tf.gather(gcn_layer_final,indices=negSampleList,
                                          name='negSamplesMatrix'),
                                name='transposed_negSamplesMatrix')

    loss = -tf.reduce_sum(tf.log((tf.sigmoid(tf.diag_part(
                                tf.matmul(tf.matmul(baseSamples,innerMat),posSamples_T)))
                                  +0.0000001)) +
                          tf.log((1-tf.sigmoid( tf.diag_part(
                              tf.matmul(tf.matmul(baseSamples,innerMat),negSamples_T)))
                                  +0.0000001)))
    # sample_loss = tf.Variable(tf.zeros(shape=[len(posNodesPair)]))
    # sample_loss.assign(tf.zeros(shape=[len(posNodesPair)]))
    # tf.print(sample_loss)
    # loss = 0

    # print('loss op start')
    # for index,posPair in tqdm(enumerate(posNodesPair)):
    #     # 正例loss
    #     # 用 Variable.assign_add 将两个矩阵相加
    #
    #     pos_val_diff = 1-tf.sigmoid(
    #         tf.reshape(tf.matmul([denseLayer[posPair[0]]],tf.transpose([denseLayer[posPair[1]]])),[-1]))

        # pos_diff_loss = tf.sparse_tensor_to_dense(tf.SparseTensor(indices=[[index]], values=pos_val_diff, dense_shape=[len(posNodesPair)]))

        # sample_loss.assign_add(pos_diff_loss)

        # loss += pos_val_diff


        # 负例loss
        # neg = tf.random_uniform(shape=[1],minval=0,maxval=len(posNodesPair),dtype=tf.int64)
        # for negID in neg:
        # neg_val_diff = tf.sigmoid(
        #     tf.reshape(tf.matmul([denseLayer[posPair[0]]], tf.transpose([denseLayer[negID]])), [-1]))
        # neg_diff_loss = tf.sparse_tensor_to_dense(
        #     tf.SparseTensor(indices=[[index]], values=neg_val_diff, dense_shape=[len(posNodesPair)]))

            # sample_loss.assign_add(neg_diff_loss)
            # loss += neg_val_diff

    # loss = tf.reduce_mean(sample_loss)
    # print('loss op finished')


with tf.name_scope('train'):
    print('train op start')
    train_step = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)
    print('train op end')



losses = []
epochs = []

sess = tf.Session()
sess.run(tf.global_variables_initializer())

for i in tqdm(range(10240)):
    # print(i)
    epochs.append(i)

    negsampleslist = np.random.randint(0,mapLength,size=[len(posRow)])
    # print(negsampleslist)
    # print(nsl)

    # sess.run()
    sess.run(train_step,feed_dict={x1_adj_input:adj,
                                   x2_features_input:features,
                                   negSampleList:negsampleslist,
                                   keep_prob:dropout_keep_prob
                                   })

    cur_loss = sess.run(loss, feed_dict={x1_adj_input: adj,
                                         x2_features_input: features,
                                         negSampleList: negsampleslist,
                                         keep_prob: 1.0
                                         })

    losses.append(cur_loss)

    if i%100 == 0:
        print(cur_loss)


# print('outputs')
# print(outputs)
# print(outputs.shape)
# print('bs')
#
# print(bs)
# print(bs.shape)
#
# print('ps')
# print(ps)
# print(ps.shape)
#
# print('ns')
# print(ns)
# print(ns.shape)

outputs = sess.run(denseLayer,feed_dict={x1_adj_input:adj,
                                        x2_features_input:features,
                                        keep_prob:1.0
                                        })

inner_mat = sess.run(innerMat,feed_dict={x1_adj_input:adj,
                                        x2_features_input:features,
                                        keep_prob:1.0
                                        })


adj_new = np.zeros(shape=(485,485),dtype=int)

def sigmoid(x):
    s = 1 / (1 + np.exp(-x))
    return s

for index1,node1 in tqdm(enumerate(outputs)):
    for index2,node2 in enumerate(outputs):
        if index2!=index1:
            p = sigmoid(np.dot(np.dot(node1,inner_mat),node2.T))
            if p>0.99:
                adj_new[index1][index2] = 1

np.savetxt('newDrugGraph.txt',adj_new, fmt='%d', delimiter="\t")

plt.plot(epochs,losses)
plt.xlabel('epochs')
plt.ylabel('loss')
plt.show()