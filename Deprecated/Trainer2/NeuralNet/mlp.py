from layer import *

# input placeholders
# x: byte value (0 ~ 255)
# y: 5 file types in one hot encoding
X = tf.placeholder(tf.float32, [None, FLAGS.input_dimension])
Y = tf.placeholder(tf.float32, [None, FLAGS.num_of_groups])

# keep probability placeholder for dropout
keep_prob = tf.placeholder(tf.float32)

# List that contains size of each layer.
# size[i]: output_size of i-th layer
size = [FLAGS.input_dimension, 1024, 512, 256, 128, 64, 32, 16, FLAGS.num_of_groups]

# Layers
L1 = simple_layer("1", input_tensor=X, input_size=size[0], output_size=size[1], relu=True, dropout=True, keep_prob=keep_prob)
L2 = simple_layer("2", input_tensor=L1, input_size=size[1], output_size=size[2], relu=True, dropout=True, keep_prob=keep_prob)
L3 = simple_layer("3", input_tensor=L2, input_size=size[2], output_size=size[3], relu=True, dropout=True, keep_prob=keep_prob)
L4 = simple_layer("4", input_tensor=L3, input_size=size[3], output_size=size[4], relu=True, dropout=True, keep_prob=keep_prob)
L5 = simple_layer("5", input_tensor=L4, input_size=size[4], output_size=size[5], relu=True, dropout=True, keep_prob=keep_prob)
L6 = simple_layer("6", input_tensor=L5, input_size=size[5], output_size=size[6], relu=True, dropout=True, keep_prob=keep_prob)
L7 = simple_layer("7", input_tensor=L6, input_size=size[6], output_size=size[7], relu=True, dropout=True, keep_prob=keep_prob)

hypothesis = simple_layer("8", input_tensor=L7, input_size=size[7], output_size=size[8], relu=False, dropout=False, keep_prob=keep_prob)
