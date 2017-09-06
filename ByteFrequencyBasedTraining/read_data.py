import os
import tensorflow as tf
import unittest


def filename_list_in_data_directory(path_dir: str):
    """
    read a directory and returns a list of included file paths.
    :param path_dir: path's directory to read
    :return: filename's list in the data directory
    """
    filename_list = os.listdir(path_dir)
    filename_list = list(filter(lambda x: x.endswith(".csv"), filename_list))
    return filename_list


def read_data(data_type: str):
    """
    read the data folder and returns a single csv file.
    :param data_type: "train" or "test"
    :return: a csv file's parsed result
    """
    try:
        if data_type.lower() == "train":
            filename_list = filename_list_in_data_directory("./train_data")
        elif data_type.lower() == "test":
            filename_list = filename_list_in_data_directory("./test_data")
        else:
            raise ValueError("only train or test data is available.")
        filename_queue = tf.train.string_input_producer(filename_list, shuffle=True)
        reader = tf.TextLineReader()
        key, value = reader.read(filename_queue)
        record_defaults = [[0]] * 261
        input_data = tf.decode_csv(value, record_defaults=record_defaults)
        return input_data
    except:
        print("Error: cannot read input data")
        exit()


def read_data_batch(data_type: str, batch_size: int):
    """
    read a data file, and returns batch data.
    :param data_type: "train" or "test"
    :param batch_size: bach size to get
    :return: batch value and file type encoded by one-hot encoding
    """
    input_data = read_data(data_type)
    byte_value = input_data[:][0:256]
    file_type = input_data[:][256:]

    batch_byte_value, batch_file_type = tf.train.batch([byte_value, file_type], batch_size=batch_size)

    return batch_byte_value, batch_file_type


class Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_read(self):
        with tf.Session() as sess:
            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(sess=sess, coord=coord)

            for step in range(10):
                input_data = read_data("train")

            coord.request_stop()
            coord.join(threads)
