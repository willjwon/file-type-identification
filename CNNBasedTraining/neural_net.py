from setup import *

# input placeholders
# x: byte value (0 ~ 255)
# y: 5 file types in one hot encoding
X = tf.placeholder(tf.float32, [None, 4096])
Y = tf.placeholder(tf.float32, [None, FLAGS.num_of_file_types])

X_2d = tf.reshape(X, shape=[-1, 64, 64, 1])

# keep probability placeholder for dropout
keep_prob = tf.placeholder(tf.float32)


def weight_variable(shape, name):
    return tf.get_variable(shape=shape, initializer=tf.contrib.layers.xavier_initializer(), name=name)


def bias_variable(shape, name):
    return tf.Variable(tf.zeros(shape), name=name)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding="SAME")


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")


# weights & bias
with tf.name_scope("layer1"):
    W1 = weight_variable([5, 5, 1, 32], name="W1")
    b1 = bias_variable([32], name="b1")
    L1 = tf.nn.relu(conv2d(X_2d, W1) + b1)
    L1_out = max_pool_2x2(L1)

    tf.summary.histogram("X_2d", X_2d)
    tf.summary.histogram("weights", W1)
    tf.summary.histogram("bias", b1)
    tf.summary.histogram("layer", L1_out)

with tf.name_scope("layer2"):
    W2 = weight_variable([5, 5, 32, 64], name="W2")
    b2 = bias_variable([64], name="b2")
    L2 = tf.nn.relu(conv2d(L1_out, W2) + b2)
    L2_out = max_pool_2x2(L2)

    tf.summary.histogram("weights", W2)
    tf.summary.histogram("bias", b2)
    tf.summary.histogram("layer", L2_out)


with tf.name_scope("layer3"):
    W3 = weight_variable([5, 5, 64, 128], name="W3")
    b3 = bias_variable([128], name="b3")
    L3 = tf.nn.relu(conv2d(L2_out, W3) + b3)
    L3_out = max_pool_2x2(L3)

    tf.summary.histogram("weights", W3)
    tf.summary.histogram("bias", b3)
    tf.summary.histogram("layer", L3_out)


with tf.name_scope("layer4"):
    W4 = weight_variable([5, 5, 128, 256], name="W4")
    b4 = bias_variable([256], name="b4")
    L4 = tf.nn.relu(conv2d(L3_out, W4) + b4)
    L4_out = max_pool_2x2(L4)
    L4_flat_out = tf.reshape(L4_out, [-1, 4 * 4 * 256])

    tf.summary.histogram("weights", W4)
    tf.summary.histogram("bias", b4)
    tf.summary.histogram("layer", L4_flat_out)


with tf.name_scope("layer5"):
    W5 = weight_variable([4 * 4 * 256, 512], name="W5")
    b5 = bias_variable([512], name="b5")
    L5 = tf.nn.relu(tf.matmul(L4_flat_out, W5) + b5)
    L5_out = tf.nn.dropout(L5, keep_prob)

    tf.summary.histogram("weights", W5)
    tf.summary.histogram("bias", b5)
    tf.summary.histogram("layer", L5_out)


with tf.name_scope("layer6"):
    W6 = weight_variable([512, FLAGS.num_of_file_types], name="W6")
    b6 = bias_variable([FLAGS.num_of_file_types], name="b6")
    hypothesis = tf.matmul(L5_out, W6) + b6

    tf.summary.histogram("weights", W6)
    tf.summary.histogram("bias", b6)
    tf.summary.histogram("hypothesis", hypothesis)
