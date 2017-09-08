from setup import *

# input placeholders
# x: byte value (0 ~ 255)
# y: 5 file types in one hot encoding
X = tf.placeholder(tf.float32, [None, 256])
Y = tf.placeholder(tf.float32, [None, 5])

# keep probability placeholder for dropout
keep_prob = tf.placeholder(tf.float32)

# weights & bias
with tf.variable_scope("layer1"):
    W1 = tf.get_variable(name="W1", shape=[256, 512], initializer=tf.contrib.layers.xavier_initializer())
    b1 = tf.Variable(tf.random_normal([512]))
    L1 = tf.nn.relu(tf.matmul(X, W1) + b1)
    L1 = tf.nn.dropout(L1, keep_prob=keep_prob)

    tf.summary.histogram("X", X)
    tf.summary.histogram("weights", W1)
    tf.summary.histogram("bias", b1)
    tf.summary.histogram("layer", L1)

with tf.variable_scope("layer2"):
    W2 = tf.get_variable(name="W2", shape=[512, 512], initializer=tf.contrib.layers.xavier_initializer())
    b2 = tf.Variable(tf.random_normal([512]))
    L2 = tf.nn.relu(tf.matmul(L1, W2) + b2)
    L2 = tf.nn.dropout(L2, keep_prob=keep_prob)

    tf.summary.histogram("weights", W2)
    tf.summary.histogram("bias", b2)
    tf.summary.histogram("layer", L2)

with tf.variable_scope("layer3"):
    W3 = tf.get_variable(name="W3", shape=[512, 512], initializer=tf.contrib.layers.xavier_initializer())
    b3 = tf.Variable(tf.random_normal([512]))
    L3 = tf.nn.relu(tf.matmul(L2, W3) + b3)
    L3 = tf.nn.dropout(L3, keep_prob=keep_prob)

    tf.summary.histogram("weights", W3)
    tf.summary.histogram("bias", b3)
    tf.summary.histogram("layer", L3)

with tf.variable_scope("layer4"):
    W4 = tf.get_variable(name="W4", shape=[512, 512], initializer=tf.contrib.layers.xavier_initializer())
    b4 = tf.Variable(tf.random_normal([512]))
    L4 = tf.nn.relu(tf.matmul(L3, W4) + b4)
    L4 = tf.nn.dropout(L4, keep_prob=keep_prob)

    tf.summary.histogram("weights", W4)
    tf.summary.histogram("bias", b4)
    tf.summary.histogram("layer", L4)

with tf.variable_scope("layer5"):
    W5 = tf.get_variable(name="W5", shape=[512, 512], initializer=tf.contrib.layers.xavier_initializer())
    b5 = tf.Variable(tf.random_normal([512]))
    L5 = tf.nn.relu(tf.matmul(L4, W5) + b5)
    L5 = tf.nn.dropout(L5, keep_prob=keep_prob)

    tf.summary.histogram("weights", W5)
    tf.summary.histogram("bias", b5)
    tf.summary.histogram("layer", L5)

with tf.variable_scope("layer6"):
    W6 = tf.get_variable(name="W6", shape=[512, 512], initializer=tf.contrib.layers.xavier_initializer())
    b6 = tf.Variable(tf.random_normal([512]))
    L6 = tf.nn.relu(tf.matmul(L5, W6) + b6)
    L6 = tf.nn.dropout(L6, keep_prob=keep_prob)

    tf.summary.histogram("weights", W6)
    tf.summary.histogram("bias", b6)
    tf.summary.histogram("layer", L6)

with tf.variable_scope("layer7"):
    W7 = tf.get_variable(name="W7", shape=[512, 512], initializer=tf.contrib.layers.xavier_initializer())
    b7 = tf.Variable(tf.random_normal([512]))
    L7 = tf.nn.relu(tf.matmul(L6, W7) + b7)
    L7 = tf.nn.dropout(L7, keep_prob=keep_prob)

    tf.summary.histogram("weights", W7)
    tf.summary.histogram("bias", b7)
    tf.summary.histogram("layer", L7)

with tf.variable_scope("layer8"):
    W8 = tf.get_variable(name="W8", shape=[512, 5], initializer=tf.contrib.layers.xavier_initializer())
    b8 = tf.Variable(tf.random_normal([5]))
    hypothesis = tf.nn.relu(tf.matmul(L7, W8) + b8)

    tf.summary.histogram("weights", W8)
    tf.summary.histogram("bias", b8)
    tf.summary.histogram("hypothesis", hypothesis)
