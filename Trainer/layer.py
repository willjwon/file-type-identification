from setup import *


def simple_layer(layer_num, input_tensor, input_size, output_size, relu, dropout, keep_prob):
    with tf.variable_scope("layer" + layer_num):
        weight = tf.get_variable(shape=[input_size, output_size],
                                 initializer=tf.contrib.keras.initializers.he_normal(),
                                 name="W" + layer_num)
        bias = tf.Variable(tf.random_normal([output_size]), name="b" + layer_num)

        output = tf.matmul(input_tensor, weight) + bias
        if relu:
            output = tf.nn.relu(output)
        if dropout:
            output = tf.nn.dropout(output, keep_prob=keep_prob)

        tf.summary.histogram("input", input_tensor)
        tf.summary.histogram("weights", weight)
        tf.summary.histogram("bias", bias)
        tf.summary.histogram("layer", output)

        return output


def reshape_layer(layer_num, input_tensor, shape):
    with tf.variable_scope("layer" + layer_num):
        output = tf.reshape(input_tensor, shape=shape)

        tf.summary.histogram("input", input_tensor)
        tf.summary.histogram("layer", output)

        return output


def cnn_layer(layer_num, input_tensor, filter_size, channel_size, relu, pool_size):
    with tf.variable_scope("layer" + layer_num):
        weight = tf.get_variable(shape=[filter_size[0], filter_size[0], channel_size[0], channel_size[1]],
                                 initializer=tf.contrib.layers.xavier_initializer(),
                                 name="W" + layer_num)
        bias = tf.Variable(tf.random_normal([channel_size[1]]),
                           name="b" + layer_num)

        output = tf.nn.conv2d(input_tensor, weight, strides=[1, 1, 1, 1], padding="SAME") + bias
        if relu:
            output = tf.nn.relu(output)
        if pool_size[0] != 0 and pool_size[1] != 0:
            output = tf.nn.max_pool(output,
                                    ksize=[1, pool_size[0], pool_size[1], 1],
                                    strides=[1, pool_size[0], pool_size[1], 1],
                                    padding="SAME")

        tf.summary.histogram("input", input_tensor)
        tf.summary.histogram("weights", weight)
        tf.summary.histogram("bias", bias)
        tf.summary.histogram("layer", output)

        return output
