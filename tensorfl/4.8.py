import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf

# 加载数据
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
trX, trY, teX, teY = mnist.train.images, mnist.train.labels, mnist.test.images, mnist.test.labels
X = tf.placeholder("float", [None, 784])
Y = tf.placeholder("float", [None, 10])


# 定义权重函数
def init_weights(shape):
    return tf.Variable(tf.random_normal(shape, stddev=0.01))

# 初始化权重参数
w_h = init_weights([784, 625])
w_h2 = init_weights([625, 625])
w_o = init_weights([625, 10])

# 定义模型
def model(X, w_h, w_h2, w_o, p_keep_input, p_keep_hidden):
    # 第一个全连接层
    X = tf.nn.dropout(X, p_keep_input)
    h = tf.nn.relu(tf.matmul(X, w_h))
    h = tf.nn.dropout(h, p_keep_hidden)
    # 第二个全连接层
    h2 = tf.nn.relu(tf.matmul(h, w_h2))
    h2 = tf.nn.dropout(h2, p_keep_hidden)
    return tf.matmul(h2, w_o) #输出预测值

p_keep_input = tf.placeholder("float")
p_keep_hidden = tf.placeholder("float")
py_x = model(X, w_h, w_h2, w_o, p_keep_input, p_keep_hidden)

#定义损失函数
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=py_x, labels=Y))
train_op = tf.train.RMSPropOptimizer(0.001, 0.9).minimize(cost)
predict_op = tf.argmax(py_x, 1)

ckpt_dir = "./ckpt_dir"
if not os.path.exists(ckpt_dir):
     os.makedirs(ckpt_dir)
# 计数器变量，设置它的trainable=False，不需要被训练
global_step = tf.Variable(0, name='global_step', trainable=False)

# 在声明完所有变量后，调用tf.train.Saver
saver = tf.train.Saver()
# 位于tf.train.Saver之后的变量将不会被存储
non_storable_variable = tf.Variable(777)



# with tf.Session() as sess:
#     tf.initialize_all_variables().run()
#
#     start = global_step.eval() # 得到global_step的初始值
#     print("Start from:", start)
#     for i in range(start, 100):
#         # 以128作为batch_size
#         for start, end in zip(range(0, len(trX), 128), range(128, len(trX)+1, 128)):
#             sess.run(train_op, feed_dict={X: trX[start:end], Y: trY[start:end],
#                       p_keep_input: 0.8, p_keep_hidden: 0.5})
#             global_step.assign(i).eval() # 更新计数器
#             saver.save(sess, ckpt_dir + "/model.ckpt", global_step=global_step) # 存储模型


model_checkpoint_path: "model.ckpt-60"
all_model_checkpoint_paths: "model.ckpt-56"
all_model_checkpoint_paths: "model.ckpt-57"
all_model_checkpoint_paths: "model.ckpt-58"
all_model_checkpoint_paths: "model.ckpt-59"
all_model_checkpoint_paths: "model.ckpt-60"


with tf.Session() as sess:
    tf.initialize_all_variables().run()
    ckpt = tf.train.get_checkpoint_state(ckpt_dir)
    if ckpt and ckpt.model_checkpoint_path:
        print(ckpt.model_checkpoint_path)
        saver.restore(sess, ckpt.model_checkpoint_path) # 加载所有的参数
            # 从这里开始就可以直接使用模型进行预测，或者接着继续训练了
    v = tf.Variable(0, name='my_variable')
    sess = tf.Session()
    tf.train.write_graph(sess.graph_def, '/tmp/tfmodel', 'train.pbtxt')



# with tf.Session() as _sess:
#     with gfile.FastGFile("/tmp/tfmodel/train.pbtxt", 'rb') as f:
#         graph_def = tf.GraphDef()
#         graph_def.ParseFromString(f.read())
#         _sess.graph.as_default()
#         tf.import_graph_def(graph_def, name='tfgraph')