import tensorflow as tf

from ByteFrequencyBasedTraining.setup import *
from ByteFrequencyBasedTraining.read_data import *
from ByteFrequencyBasedTraining.neural_net import *

def main():
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
        logits=hypothesis, labels=Y))
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

    train_batch_byte_value, train_batch_file_type = read_data_batch("train", batch_size)

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        # set the threads for reading data
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)

        # train the model
        for epoch in range(num_of_epochs):
            avg_cost = 0

            for batch in range(batch_per_epoch):
                batch_byte_value, batch_file_type = sess.run([train_batch_byte_value, train_batch_file_type])
                feed_dict = {X: batch_byte_value, Y: batch_file_type, keep_prob: 0.7}
                c, _ = sess.run([cost, optimizer], feed_dict=feed_dict)
                avg_cost += c / batch_per_epoch

            print("Epoch:", "{:0>4}".format(epoch + 1), "cost:", "{:.9f}".format(avg_cost))

        print("Learning Completed")

        # test.csv the model
        # TODO: modify read_data_batch for testing (batch_size)
        test_x, test_y = read_data_batch("test.csv", 1000)

        correct_prediction = tf.equal(tf.argmax(hypothesis, 1), tf.argmax(Y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        feed_dict = {X: test_x, Y: test_y, keep_prob: 1}
        print("Accuracy:", sess.run(accuracy, feed_dict=feed_dict))

        coord.request_stop()
        coord.join(threads)

if __name__ == "__main__":
    main()