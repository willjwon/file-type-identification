from read_data import *
from neural_net import *


def main():
    train_queue, validation_queue, test_queue = make_files_queue()
    train_batch_byte_value, train_batch_file_type = next_train_batch(batch_size, train_queue)
    validation_batch_byte_value, validation_batch_file_type = validation_data_set(validation_queue)
    test_batch_byte_value, test_batch_file_type = test_data_set(test_queue)

    global_step = tf.Variable(0, trainable=False, name="global_step")
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=hypothesis, labels=Y))
    accuracy = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(hypothesis, 1), tf.argmax(Y, 1)), tf.float32))
    optimizer = tf.train.AdamOptimizer(learning_rate=FLAGS.learning_rate).minimize(cost, global_step=global_step)
    tf.summary.scalar(name="cost", tensor=cost)

    saver = tf.train.Saver(max_to_keep=5)

    # tensorboard summary
    summary = tf.summary.merge_all()
    writer = tf.summary.FileWriter(tensorboard_directory)

    with tf.Session() as sess:
        writer.add_graph(sess.graph)

        checkpoint = tf.train.get_checkpoint_state(FLAGS.model_path)
        if checkpoint and checkpoint.model_checkpoint_path:
            saver.restore(sess, checkpoint.model_checkpoint_path)
        else:
            sess.run(tf.global_variables_initializer())

        # set the threads for reading data
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)

        current_step = sess.run(global_step)

        # train the model
        for step in range(current_step, FLAGS.num_of_total_global_steps):
            # validation and save at checkpoint
            if step % FLAGS.checkpoint_steps == 0:
                validation_byte_value, validation_file_type \
                    = sess.run([validation_batch_byte_value, validation_batch_file_type])
                computed_accuracy = \
                    sess.run(accuracy, feed_dict={X: validation_byte_value, Y: validation_file_type, keep_prob: 1.0})
                print("\tAt step {:>5}, accuracy: {:2.9f}".format(step, computed_accuracy))
                saver.save(sess, FLAGS.model_path, global_step=step)

            # train step
            batch_byte_value, batch_file_type = sess.run([train_batch_byte_value, train_batch_file_type])
            cost, _, summary = sess.run([cost, optimizer, summary],
                                        feed_dict={X: batch_byte_value,
                                                   Y: batch_file_type,
                                                   keep_prob: FLAGS.keep_prob_train})

            # add summary to tensorboard
            writer.add_summary(summary, global_step=global_step)

            print("step {:>5}, cost: {:2.9f}".format(step, cost))

        # test the model
        test_byte_value, test_file_type = sess.run([test_batch_byte_value, test_batch_file_type])
        computed_accuracy = sess.run(accuracy, feed_dict={X: test_byte_value, Y: test_file_type, keep_prob: 1.0})
        print("=== Test Result, accuracy: {:2.9f}".format(computed_accuracy))

        coord.request_stop()
        coord.join(threads)


if __name__ == "__main__":
    main()
