from read_data import *
from neural_net import *


def main():
    train_queue, validation_queue, test_queue = make_files_queue()
    train_batch_byte_value, train_batch_file_type = next_train_batch(FLAGS.batch_size, train_queue)
    validation_batch_byte_value, validation_batch_file_type = get_data_set(validation_queue)
    test_batch_byte_value, test_batch_file_type = get_data_set(test_queue)
    _, num_of_validation_files, num_of_test_files = get_num_of_data_files()

    # global step for train
    global_step = tf.Variable(0, trainable=False, name="global_step")

    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=hypothesis, labels=Y))

    classify_result = tf.argmax(hypothesis, 1)

    def classify_count(tensor, value):
        return tf.reduce_sum(tf.cast(tf.equal(tensor, value), tf.int32))

    def accuracy(result):
        file_type = tf.argmax(Y, 1)[0]
        return file_type, tf.reduce_mean(tf.cast(tf.equal(result, tf.argmax(Y, 1)), tf.float32))

    optimizer = tf.train.AdamOptimizer(learning_rate=FLAGS.learning_rate).minimize(cost, global_step=global_step)
    tf.summary.scalar(name="cost", tensor=cost)

    saver = tf.train.Saver(max_to_keep=3)

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
            print("Checkpoint at step {} is found. That model is loaded and used.\n".format(current_step))
        else:
            sess.run(tf.global_variables_initializer())
            sess.run(tf.local_variables_initializer())
            current_step = 0
            print("No saved checkpoint is found. The model is initialized.\n")

        # train the model
        for step in range(current_step, FLAGS.num_of_total_global_steps + 1):
            # train step
            batch_byte_value, batch_file_type = sess.run([train_batch_byte_value, train_batch_file_type])
            c, _, s = sess.run([cost, optimizer, summary],
                               feed_dict={X: batch_byte_value, Y: batch_file_type, keep_prob: FLAGS.keep_prob_train})

            if step % 100 == 0:
                print("At step {:>5}, cost: {:2.9f}".format(step, c))

            # validation and save at checkpoint
            if step % FLAGS.checkpoint_steps == 0:
                print("\nStep {:>5}: Checkpoint.".format(step))
                # saving model
                model_saved_path = saver.save(sess, model_save_path, global_step=step)
                print("Model successfully saved at {}.\n".format(model_saved_path))

                # validation
                print("\nValidating. Please wait...".format(step))

                average_accuracy = 0.
                accuracy_each_type = [[0] * FLAGS.num_of_file_types for _ in range(FLAGS.num_of_file_types)]
                # for i in range(FLAGS.num_of_file_types):
                #     accuracy_each_type.append([0] * FLAGS.num_of_file_types)

                for i in range(1, num_of_validation_files + 1):
                    validation_byte_value, validation_file_type \
                        = sess.run([validation_batch_byte_value, validation_batch_file_type])
                    result = sess.run(classify_result,
                                      feed_dict={X: validation_byte_value, keep_prob: 1.0})

                    current_file_type, current_accuracy = sess.run(accuracy(result), feed_dict={Y: validation_file_type})
                    average_accuracy += current_accuracy

                    for j in range(FLAGS.num_of_file_types):
                        accuracy_each_type[current_file_type][j] += sess.run(classify_count(result, j),
                                                                             feed_dict={Y: validation_file_type})

                print("Validation Result Table:")
                print("\t | ", end="")
                for i in range(FLAGS.num_of_file_types):
                    print("{:<5}\t\t".format(FLAGS.file_type_name[i]), end="")
                print("")
                print("----------" * (FLAGS.num_of_file_types + 1))
                for i in range(FLAGS.num_of_file_types):
                    print("{:<5}\t | ".format(FLAGS.file_type_name[i]), end="")
                    for j in range(FLAGS.num_of_file_types):
                        print("{:2.2f}%\t\t".format(
                            accuracy_each_type[i][j] /
                            (FLAGS.num_of_validation_files_per_type * FLAGS.num_of_fragments_per_csv)
                            * 100),
                            end="")
                    print("")
                print("----------" * (FLAGS.num_of_file_types + 1))
                print("Validation Accuracy: {:2.9f}%\n".format(average_accuracy / num_of_validation_files * 100))

            # add summary to tensorboard
            writer.add_summary(s, global_step=step)

        # test the model
        print("Testing. Please wait...\n")

        average_accuracy = 0.
        accuracy_each_type = [[0] * FLAGS.num_of_file_types for _ in range(FLAGS.num_of_file_types)]
        # for i in range(FLAGS.num_of_file_types):
        #     accuracy_each_type.append([0] * FLAGS.num_of_file_types)

        for i in range(1, num_of_test_files + 1):
            test_byte_value, test_file_type = sess.run([test_batch_byte_value, test_batch_file_type])
            result = sess.run(classify_result, feed_dict={X: test_byte_value, keep_prob: 1.0})

            current_file_type, current_accuracy = sess.run(accuracy(result), feed_dict={Y: test_file_type})
            average_accuracy += current_accuracy
            for j in range(FLAGS.num_of_file_types):
                accuracy_each_type[current_file_type][j] += sess.run(classify_count(result, j), feed_dict={Y: test_file_type})

        print("\t | ", end="")
        for i in range(FLAGS.num_of_file_types):
            print("{:<5}\t\t".format(FLAGS.file_type_name[i]), end="")
        print("")
        print("----------" * (FLAGS.num_of_file_types + 1))

        for i in range(FLAGS.num_of_file_types):
            print("{:<5}\t | ".format(FLAGS.file_type_name[i]), end="")
            for j in range(FLAGS.num_of_file_types):
                print("{:2.2f}%\t\t".format(
                    accuracy_each_type[i][j] /
                    (FLAGS.num_of_test_files_per_type * FLAGS.num_of_fragments_per_csv)
                    * 100),
                    end="")
            print("")

        print("----------" * (FLAGS.num_of_file_types + 1))
        print("Test Result: accuracy: {:2.9f}%\n".format(average_accuracy / num_of_test_files * 100))

        coord.request_stop()
        coord.join(threads)


if __name__ == "__main__":
    main()

