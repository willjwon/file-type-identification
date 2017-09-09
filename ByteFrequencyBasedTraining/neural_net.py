from setup import *

# input placeholders
# x: byte value (0 ~ 255)
# y: 5 file types in one hot encoding
X = tf.placeholder(tf.float32, [None, 256])
Y = tf.placeholder(tf.float32, [None, 3])

# keep probability placeholder for dropout
keep_prob = tf.placeholder(tf.float32)

# weights & bias
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
    W2 = tf.get_variable(shape=[512, 512], initializer=tf.contrib.layers.xavier_initializer(), name="W2")
    b2 = tf.Variable(tf.random_normal([512]), name="b2")
    L2 = tf.nn.relu(tf.matmul(L1, W2) + b2)
    L2 = tf.nn.dropout(L2, keep_prob=keep_prob)

    tf.summary.histogram("weights", W2)
    tf.summary.histogram("bias", b2)
    tf.summary.histogram("layer", L2)

with tf.variable_scope("layer3"):
    W3 = tf.get_variable(shape=[512, 512], initializer=tf.contrib.layers.xavier_initializer(), name="W3")
    b3 = tf.Variable(tf.random_normal([512]), name="b3")
    L3 = tf.nn.relu(tf.matmul(L2, W3) + b3)
    L3 = tf.nn.dropout(L3, keep_prob=keep_prob)

    tf.summary.histogram("weights", W3)
    tf.summary.histogram("bias", b3)
    tf.summary.histogram("layer", L3)

with tf.variable_scope("layer4"):
    W4 = tf.get_variable(shape=[512, 512], initializer=tf.contrib.layers.xavier_initializer(), name="W4")
    b4 = tf.Variable(tf.random_normal([512]), name="b4")
    L4 = tf.nn.relu(tf.matmul(L3, W4) + b4)
    L4 = tf.nn.dropout(L4, keep_prob=keep_prob)

    tf.summary.histogram("weights", W4)
    tf.summary.histogram("bias", b4)
    tf.summary.histogram("layer", L4)

with tf.variable_scope("layer5"):
    W5 = tf.get_variable(shape=[512, 3], initializer=tf.contrib.layers.xavier_initializer(), name="W5")
    b5 = tf.Variable(tf.random_normal([3]), name="b5")
    hypothesis = tf.matmul(L4, W5) + b5

    tf.summary.histogram("weights", W5)
    tf.summary.histogram("bias", b5)
    tf.summary.histogram("hypothesis", hypothesis)
