import tensorflow as tf


def layer(layer_num, input_tensor, input_size, output_size, relu, dropout, keep_prob):
    with tf.variable_scope("layer" + layer_num):
        weight = tf.get_variable(shape=[input_size, output_size],
                                 initializer=tf.contrib.layers.xavier_initializer(),
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
