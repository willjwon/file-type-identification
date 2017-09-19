from layer import *

# input placeholders
# x: byte value (0 ~ 255)
# y: 5 file types in one hot encoding
X = tf.placeholder(tf.float32, [None, 256])
Y = tf.placeholder(tf.float32, [None, FLAGS.num_of_groups])

# keep probability placeholder for dropout
keep_prob = tf.placeholder(tf.float32)

# Layers
L1 = reshape_layer("1", input_tensor=X, shape=[-1, 16, 16, 1])
L2 = cnn_layer("2", input_tensor=L1, filter_size=[5, 5], channel_size=[1, 32], relu=True, pool_size=[2, 2])
L3 = cnn_layer("3", input_tensor=L2, filter_size=[5, 5], channel_size=[32, 64], relu=True, pool_size=[2, 2])
L4 = reshape_layer("4", input_tensor=L3, shape=[-1, 4 * 4 * 64])
L5 = simple_layer("5", input_tensor=L4, input_size=4 * 4 * 64, output_size=256,
                  relu=True, dropout=True, keep_prob=keep_prob)
hypothesis = simple_layer("6", input_tensor=L5, input_size=256, output_size=FLAGS.num_of_groups,
                          relu=False, dropout=False, keep_prob=keep_prob)
