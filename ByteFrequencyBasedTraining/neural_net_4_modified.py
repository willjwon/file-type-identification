from setup import *
from layer import *

# input placeholders
# x: byte value (0 ~ 255)
# y: 5 file types in one hot encoding
X = tf.placeholder(tf.float32, [None, 256])
Y = tf.placeholder(tf.float32, [None, 3])

# keep probability placeholder for dropout
keep_prob = tf.placeholder(tf.float32)

# weights & bias
# L1 = layer("1", input_tensor=X, input_size=256, output_size=512, relu=True, dropout=True, keep_prob=keep_prob)
# L2 = layer("2", input_tensor=L1, input_size=512, output_size=256, relu=True, dropout=True, keep_prob=keep_prob)
# L3 = layer("3", input_tensor=L2, input_size=256, output_size=20, relu=True, dropout=True, keep_prob=keep_prob)
# hypothesis = layer("4", input_tensor=L3, input_size=20, output_size=5, relu=False, dropout=False, keep_prob=keep_prob)

with tf.variable_scope("layer1"):
    W1 = tf.get_variable(shape=[256, 512], initializer=tf.contrib.layers.xavier_initializer(), name="W1")
    b1 = tf.Variable(tf.random_normal([512]), name="b1")
    L1 = tf.nn.relu(tf.matmul(X, W1) + b1)
    L1 = tf.nn.dropout(L1, keep_prob=keep_prob)

    tf.summary.histogram("X", X)
    tf.summary.histogram("weights", W1)
    tf.summary.histogram("bias", b1)
    tf.summary.histogram("layer", L1)

with tf.variable_scope("layer2"):
    W2 = tf.get_variable(shape=[512, 256], initializer=tf.contrib.layers.xavier_initializer(), name="W2")
    b2 = tf.Variable(tf.random_normal([256]), name="b2")
    L2 = tf.nn.relu(tf.matmul(L1, W2) + b2)
    L2 = tf.nn.dropout(L2, keep_prob=keep_prob)

    tf.summary.histogram("weights", W2)
    tf.summary.histogram("bias", b2)
    tf.summary.histogram("layer", L2)

with tf.variable_scope("layer3"):
    W3 = tf.get_variable(shape=[256, 20], initializer=tf.contrib.layers.xavier_initializer(), name="W3")
    b3 = tf.Variable(tf.random_normal([20]), name="b3")
    L3 = tf.nn.relu(tf.matmul(L2, W3) + b3)
    L3 = tf.nn.dropout(L3, keep_prob=keep_prob)

    tf.summary.histogram("weights", W3)
    tf.summary.histogram("bias", b3)
    tf.summary.histogram("layer", L3)

with tf.variable_scope("layer4"):
    W4 = tf.get_variable(shape=[20, 3], initializer=tf.contrib.layers.xavier_initializer(), name="W4")
    b4 = tf.Variable(tf.random_normal([3]), name="b4")
    hypothesis = tf.matmul(L3, W4) + b4

    tf.summary.histogram("weights", W4)
    tf.summary.histogram("bias", b4)
    tf.summary.histogram("hypothesis", hypothesis)
