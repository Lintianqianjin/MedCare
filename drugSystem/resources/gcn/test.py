import numpy as np
import tensorflow as tf
# a = tf.sigmoid(
#             tf.reshape(tf.matmul([[1.,1.,1.,1.,1.]],tf.transpose([[1.,1.,1.,1.,2.]])),[-1]))
# c = 1-a
#
#
# sess = tf.Session()
# sess.run(tf.initialize_all_variables())
# d = sess.run(c)
# b = sess.run(a)
# print(b)
# print(d)

# pos_diff_loss = tf.sparse_tensor_to_dense(tf.SparseTensor(indices=[[2]], values=[0.5], dense_shape=[10]))
# neg = tf.random_uniform(shape=[10],minval=0,maxval=10,dtype=tf.int64)
a = tf.constant([[1,2,3],[3,4,5],[6,7,8]],dtype=tf.float32)
# c = tf.constant([[1,1,0],[0,1,0],[0,0,1]],dtype=tf.float32)
# d = tf.matmul(a,c)
b = tf.gather(a,indices=[0,8])
#
sess = tf.Session()
print(sess.run(tf.log(b)))
# print(sess.run(1-tf.sigmoid(tf.diag_part(d))+tf.constant([1,1,1],dtype=tf.float32)))

# nsl = np.random.randint(0,10,size=[10])
# print(np.dot([1,2,3],[1,2,3]))
# print(nsl)