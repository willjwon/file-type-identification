from setup import *
import os
import tensorflow as tf
import unittest


def files_in_directory(directory_path: str):
    """
    read a directory and returns a list of included file paths.
    :param directory_path: path's directory to read
    :return: filename's list in the data directory
    """
    filename_list = os.listdir(directory_path)
    filename_list = list(filter(lambda filename: filename.endswith(".csv"), filename_list))
    if not directory_path.endswith("/"):
        directory_path += "/"
    return list(map(lambda filename: directory_path + filename, filename_list))


def read_a_csv(data_type: str):
    """
    read the data folder and returns a single csv file.
    :param data_type: "train", "validation" or "test".
    :return: a csv file's parsed result
    """
    try:
        # Make files queue
        if data_type.lower() == "train":
            files_list = files_in_directory(FLAGS.train_data_path)
            files_queue = tf.train.string_input_producer(files_list, shuffle=True)
        elif data_type.lower() == "validation":
            files_list = files_in_directory(FLAGS.train_data_path)
            files_queue = tf.train.string_input_producer(files_list, shuffle=False)
        elif data_type.lower() == "test":
            files_list = files_in_directory(FLAGS.train_data_path)
            files_queue = tf.train.string_input_producer(files_list, shuffle=False)
        else:
            raise AttributeError("only train, validation or test data is available.")

        # Read the queue
        reader = tf.TextLineReader()
        _, read_value = reader.read(files_queue)

        # Decoder
        record_defaults = [[0.]] * 261
        return tf.decode_csv(read_value, record_defaults=record_defaults)

    except:
        print("Error: cannot read input data")
        exit()


def next_train_batch(batch_size: int):
    """
    read a data file, and returns batch data.
    :param batch_size: bach size to get
    :return: batch value and file type encoded by one-hot encoding
    """
    input_data = read_a_csv("train")
    frequency_value = input_data[:256]
    file_type_in_one_hot = input_data[256:]

    batch_frequency_value, batch_file_type_in_one_hot \
        = tf.train.batch([frequency_value, file_type_in_one_hot], batch_size=batch_size)

    return batch_frequency_value, batch_file_type_in_one_hot


class Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_batch(self):
        batch_byte_value, batch_file_type = next_train_batch(1)

        sess = tf.Session()

        # Start populating the filename queue.
        coord = tf.train.Coordinator()

        tf.train.start_queue_runners(sess=sess, coord=coord)

        x_batch, y_batch = sess.run([batch_byte_value, batch_file_type])
        print(x_batch, y_batch)
