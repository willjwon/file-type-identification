import os
import tensorflow as tf
import unittest


def get_filename_list(path_dir: str):
    """
    read a directory and returns a list of included file paths.
    :param path_dir: path's directory to read
    :return: filename's list in the data directory
    """
    filename_list = os.listdir(path_dir)
    filename_list = list(filter(lambda x: x.endswith(".csv"), filename_list))
    if not path_dir.endswith("/"):
        path_dir += "/"
    return list(map(lambda x: path_dir + x, filename_list))


def read_data(data_type: str):
    """
    read the data folder and returns a single csv file.
    :param data_type: "train" or "test.csv"
    :return: a csv file's parsed result
    """
    try:
        # Filename queue
        if data_type.lower() == "train":
            filename_list = get_filename_list("./train_data")
        elif data_type.lower() == "test":
            filename_list = get_filename_list("./test_data")
        else:
            raise ValueError("only train or test.csv data is available.")

        filename_queue = tf.train.string_input_producer(
            filename_list,
            shuffle=True)

        # Reader
        reader = tf.TextLineReader()
        key, value = reader.read(filename_queue)

        # Decoder
        record_defaults = [[0.]] * 261
        input_data = tf.decode_csv(value, record_defaults=record_defaults)
        return input_data
    except:
        print("Error: cannot read input data")
        exit()


def read_data_batch(data_type: str, batch_size: int):
    """
    read a data file, and returns batch data.
    :param data_type: "train" or "test.csv"
    :param batch_size: bach size to get
    :return: batch value and file type encoded by one-hot encoding
    """
    input_data = read_data(data_type)
    byte_value = input_data[0:256]
    file_type = input_data[256:]

    batch_byte_value, batch_file_type = tf.train.batch([byte_value, file_type], batch_size=batch_size)

    return batch_byte_value, batch_file_type


class Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_batch(self):
        batch_byte_value, batch_file_type = read_data_batch("train", 10)

        sess = tf.Session()
        # Start populating the filename queue.
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)
        for i in range(10):
            x_batch, y_batch = sess.run([batch_byte_value, batch_file_type])
            print(x_batch, y_batch)
