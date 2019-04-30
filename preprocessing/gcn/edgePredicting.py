from keras import activations, initializers, constraints
from keras import regularizers
from keras.engine.topology import Layer
import keras.backend as K

import math
import json

# 该层接受的输入应该是两个INPUT类，分别是邻接矩阵和特征矩阵
class gcnlayer(Layer):

    def __init__(self, output_dim,
                 activation=None,
                 # 偏置项，即常数项
                 use_bias=True,
                 # 核矩阵，对输入X的变化矩阵，权矩阵
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 # 施加在权重上的正则项
                 kernel_regularizer=None,
                 # 施加在偏置向量上的正则项
                 bias_regularizer=None,
                 # 施加在输出上的正则项
                 activity_regularizer=None,
                 # 对主权重矩阵进行约束
                 kernel_constraint=None,
                 # 对偏置向量进行约束
                 bias_constraint=None,
                 **kwargs):
        # 初始化各参数
        self.output_dim = output_dim
        self.activation = activations.get(activation)
        self.use_bias = use_bias
        self.kernel_initializer = initializers.get(kernel_initializer)
        self.bias_initializer = initializers.get(bias_initializer)
        self.kernel_regularizer = regularizers.get(kernel_regularizer)
        self.bias_regularizer = regularizers.get(bias_regularizer)
        self.activity_regularizer = regularizers.get(activity_regularizer)
        self.kernel_constraint = constraints.get(kernel_constraint)
        self.bias_constraint = constraints.get(bias_constraint)
        self.supports_masking = True


        super(gcnlayer, self).__init__(**kwargs)
        pass

    # todo: 定义该层需要训练的权重矩阵
    def build(self, input_shape):
        # 0是选中特征矩阵
        input_feature_dim = input_shape[0][1]

        # 定义卷积核
        self.kernel = self.add_weight(shape=(input_feature_dim, self.output_dim),
                                      initializer=self.kernel_initializer,
                                      name='kernel',
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint)

        # todo: 暂时没有考虑常数项

        super(gcnlayer, self).build(input_shape)

    # todo: 定义该层完成的变换过程
    def call(self, inputs, **kwargs):
        features_matrix = inputs[0]
        adj_matrix = inputs[1]

        # 特征矩阵与邻接矩阵做积，得到接受了邻接节点信息后的新的节点特征
        propagated_feature_matrix = K.dot(adj_matrix, features_matrix)

        # 接下来做卷积转化为新的特征表示
        output = K.dot(propagated_feature_matrix, self.kernel)

        # todo:暂时没有考虑常数项

        # 激活，如果是隐藏层用relu,最后一层softmax或sigmoid
        return self.activation(output)


    # todo: 定义该层输入输出的形状变化
    def compute_output_shape(self, input_shape):
        # 输出为（节点数*新的特征数)
        # 新的特征数也就是该层神经元数，即kernel的宽

        features_matrix = input_shape[0]
        output_shape = (features_matrix[0], self.output_dim)
        return output_shape

    # todo: 返回该层的各参数
    def get_config(self):
        pass

# 用于预测边的损失函数
def lossFunction():
    pass