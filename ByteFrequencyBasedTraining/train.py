from read_data import *
from neural_net import *


def main():
    train_queue, validation_queue, test_queue = make_files_queue()
    train_batch_byte_value, train_batch_file_type = next_train_batch(FLAGS.batch_size, train_queue)
    validation_batch_byte_value, validation_batch_file_type = get_data_set(validation_queue)
    test_batch_byte_value, test_batch_file_type = get_data_set(test_queue)

    # global step for train
    global_step = tf.Variable(0, trainable=False, name="global_step")

    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=hypothesis, labels=Y))
    accuracy = tf.reduce_mean(tf.cast(tf.equal(tf.argmax(hypothesis, 1), tf.argmax(Y, 1)), tf.float32))
    optimizer = tf.train.AdamOptimizer(learning_rate=FLAGS.learning_rate).minimize(cost, global_step=global_step)
    tf.summary.scalar(name="cost", tensor=cost)

    saver = tf.train.Saver(max_to_keep=5)

    # tensorboard summary
    summary = tf.summary.merge_all()
    writer = tf.summary.FileWriter(FLAGS.tensorboard_directory)

    # model save path
    if not FLAGS.model_output_directory.endswith("/"):
        FLAGS.model_output_directory += "/"
    model_save_path = FLAGS.model_output_directory + "model.ckpt"

    with tf.Session() as sess:
        writer.add_graph(sess.graph)

        # set the threads for reading data
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)

        # restore the data
        latest_checkpoint = tf.train.latest_checkpoint(FLAGS.model_output_directory)
        if latest_checkpoint is not None:
            saver.restore(sess, latest_checkpoint)
            current_step = sess.run(global_step)
            print("Checkpoint at step {} is found. That model is loaded and used.".format(current_step))
        else:
            sess.run(tf.global_variables_initializer())
            sess.run(tf.local_variables_initializer())
            current_step = 0
            print("No saved checkpoint is found. The model is initialized.")

        # train the model
        for step in range(current_step, FLAGS.num_of_total_global_steps):
            # validation and save at checkpoint
            if step % FLAGS.checkpoint_steps == 0:
                validation_byte_value, validation_file_type \
                    = sess.run([validation_batch_byte_value, validation_batch_file_type])
                computed_accuracy = \
                    sess.run(accuracy, feed_dict={X: validation_byte_value, Y: validation_file_type, keep_prob: 1.0})
                print("\tAt step {:>5}, accuracy: {:2.9f}%".format(step, computed_accuracy * 100))
                saver.save(sess, model_save_path, global_step=step)

            # train step
            batch_byte_value, batch_file_type = sess.run([train_batch_byte_value, train_batch_file_type])
            c, _, s = sess.run([cost, optimizer, summary],
                               feed_dict={X: batch_byte_value, Y: batch_file_type, keep_prob: FLAGS.keep_prob_train})

            # add summary to tensorboard
            writer.add_summary(s, global_step=step)

            print("step {:>5}, cost: {:2.9f}".format(step, c))

        # test the model
        test_byte_value, test_file_type = sess.run([test_batch_byte_value, test_batch_file_type])
        computed_accuracy = sess.run(accuracy, feed_dict={X: test_byte_value, Y: test_file_type, keep_prob: 1.0})
        print("=== Test Result, accuracy: {:2.9f}%".format(computed_accuracy * 100))

        coord.request_stop()
        coord.join(threads)


if __name__ == "__main__":
    main()
