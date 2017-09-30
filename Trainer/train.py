from read_data import *
from output_function import *
import importlib
import os
neural_net = importlib.import_module("NeuralNet." + FLAGS.model_name)


def main():
    # data for train
    train_file_queue, validation_file_queue, test_file_queue = make_files_queue()
    train_value_from_file, train_file_type_from_file = next_train_batch(FLAGS.batch_size, train_file_queue)
    validation_value_from_file, validation_file_type_from_file = get_data_set(validation_file_queue)
    test_value_from_file, test_file_type_from_file = get_data_set(test_file_queue)
    _, num_of_validation_files, num_of_test_files = get_num_of_data_files()

    # global step for train
    global_step = tf.Variable(0, trainable=False, name="global_step")

    # train results, like cost and accuracy.
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=neural_net.hypothesis, labels=neural_net.Y))
    classify_result = tf.argmax(neural_net.hypothesis, 1)

    def count_value(result, value_to_count):
        return tf.reduce_sum(tf.cast(tf.equal(result, value_to_count), tf.int32))

    def file_type_and_accuracy(result):
        file_type = tf.argmax(neural_net.Y, 1)[0]
        return file_type, tf.reduce_mean(tf.cast(tf.equal(result, tf.argmax(neural_net.Y, 1)), tf.float32))

    # trainer
    optimizer = tf.train.AdamOptimizer(learning_rate=FLAGS.learning_rate).minimize(cost, global_step=global_step)

    # saver
    saver = tf.train.Saver(max_to_keep=3)
    model_output_directory = "./model/" + FLAGS.model_name
    if not os.path.exists(model_output_directory):
        os.makedirs(model_output_directory)
    model_save_path = model_output_directory + "/model.ckpt"

    # tensorboard summary
    tf.summary.scalar(name="cost", tensor=cost)
    summary = tf.summary.merge_all()
    writer = tf.summary.FileWriter("./tensorboard/" + FLAGS.model_name)

    # session
    with tf.Session() as sess:
        writer.add_graph(sess.graph)

        # set the threads for reading data
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)

        # restore the data
        latest_checkpoint = tf.train.latest_checkpoint(model_output_directory)
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
            train_value, train_file_type = sess.run([train_value_from_file, train_file_type_from_file])
            c, _, s = sess.run([cost, optimizer, summary],
                               feed_dict={neural_net.X: train_value,
                                          neural_net.Y: train_file_type,
                                          neural_net.keep_prob: FLAGS.keep_prob_train})

            if step % FLAGS.cost_print_step == 0:
                print("At step {:>5}, cost: {:2.9f}".format(step, c))

            # validation and save at checkpoint
            if step % FLAGS.checkpoint_steps == 0:
                print("\nStep {}: Checkpoint.".format(step))

                # save the model
                model_saved_path = saver.save(sess, model_save_path, global_step=step)
                print("Model successfully saved at {}.\n".format(model_saved_path))

                # validation
                print("Validating. Please wait...".format(step))

                average_accuracy = 0.
                accuracy_table = [[0] * FLAGS.num_of_groups for _ in range(FLAGS.num_of_groups)]

                for i in range(1, num_of_validation_files + 1):
                    print_progress(i, num_of_validation_files)

                    validation_value, validation_file_type \
                        = sess.run([validation_value_from_file, validation_file_type_from_file])
                    result = sess.run(classify_result,
                                      feed_dict={neural_net.X: validation_value, neural_net.keep_prob: 1.0})

                    validated_file_type, current_accuracy = sess.run(file_type_and_accuracy(result),
                                                                     feed_dict={neural_net.Y: validation_file_type})
                    average_accuracy += current_accuracy

                    for j in range(FLAGS.num_of_groups):
                        accuracy_table[validated_file_type][j] += sess.run(count_value(result, j),
                                                                           feed_dict={neural_net.Y: validation_file_type})

                print("\rValidation Result Table:")
                print_accuracy_table(accuracy_table, test_type="validation")
                print("Validation Accuracy: {:2.9f}%\n".format(average_accuracy / num_of_validation_files * 100))

            # add summary to tensorboard
            writer.add_summary(s, global_step=step)

        # train ended. test the model.
        print("Testing. Please wait...\n")

        average_accuracy = 0.
        accuracy_table = [[0] * FLAGS.num_of_groups for _ in range(FLAGS.num_of_groups)]

        for i in range(1, num_of_test_files + 1):
            print_progress(i, num_of_test_files)

            test_byte_value, test_file_type = sess.run([test_value_from_file, test_file_type_from_file])
            result = sess.run(classify_result, feed_dict={neural_net.X: test_byte_value, neural_net.keep_prob: 1.0})

            tested_file_type, current_accuracy = sess.run(file_type_and_accuracy(result),
                                                          feed_dict={neural_net.Y: test_file_type})
            average_accuracy += current_accuracy
            for j in range(FLAGS.num_of_groups):
                accuracy_table[tested_file_type][j] += sess.run(count_value(result, j),
                                                                feed_dict={neural_net.Y: test_file_type})

        print("\rTest Result Table:")
        print_accuracy_table(accuracy_table, test_type="test")
        print("Test Result: accuracy: {:2.9f}%\n".format(average_accuracy / num_of_test_files * 100))

        # stop the session
        coord.request_stop()
        coord.join(threads)


if __name__ == "__main__":
    main()
