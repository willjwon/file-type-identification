from setup import *
import os
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


def get_num_of_data_files():
    """
    get number of csv files for each given data type.
    :return: "train", "validation" and "test" csv files
    """
    num_of_train_files = len(files_in_directory(FLAGS.train_data_path))
    num_of_validation_files = len(files_in_directory(FLAGS.validation_data_path))
    num_of_test_files = len(files_in_directory(FLAGS.test_data_path))
    return num_of_train_files, num_of_validation_files, num_of_test_files


def make_files_queue():
    """
    make files queue
    :return: train, validation, test files queue
    """
    try:
        train_files_list = files_in_directory(FLAGS.train_data_path)
        train_files_queue = tf.train.string_input_producer(train_files_list, shuffle=True)

        validation_files_list = files_in_directory(FLAGS.validation_data_path)
        validation_files_queue = tf.train.string_input_producer(validation_files_list, shuffle=False)

        test_files_list = files_in_directory(FLAGS.test_data_path)
        test_files_queue = tf.train.string_input_producer(test_files_list, shuffle=False)

        return train_files_queue, validation_files_queue, test_files_queue

    except:
        print("Error: cannot make files queue.")
        exit()


def read_a_csv(files_queue):
    """
    read the data folder and returns a single csv file.
    :param data_type: "train", "validation" or "test".
    :return: a csv file's parsed result
    """
    try:
        # Read the queue
        reader = tf.TextLineReader()
        _, read_value = reader.read(files_queue)

        # Decoder
        record_defaults = [[0.]] * (FLAGS.input_dimension + FLAGS.num_of_groups)
        return tf.decode_csv(read_value, record_defaults=record_defaults)

    except:
        print("Error: cannot read input data.")
        exit()


def get_batch(batch_size: int, files_queue):
    """
    get batch for a given type, read from csv files.
    :param data_type: "train", "validation" or "test"
    :param batch_size: batch size to get
    :return: batcn tensor read from csv
    """
    input_data = read_a_csv(files_queue)
    frequency_value = input_data[:FLAGS.input_dimension]
    file_type_in_one_hot = input_data[FLAGS.input_dimension:]

    return tf.train.batch([frequency_value, file_type_in_one_hot], batch_size=batch_size)


def next_train_batch(batch_size: int, train_queue):
    """
    read a data file, and returns batch data.
    :param batch_size: bach size to get
    :return: batch value and file type encoded by one-hot encoding
    """
    return get_batch(batch_size, train_queue)


def get_data_set(files_queue):
    """
    return concatenated validatoin
    :return: termination of iteration
    """
    return get_batch(FLAGS.num_of_fragments_per_csv, files_queue)


class Test(unittest.TestCase):
    def setUp(self):
        pass

    # def test_batch(self):
    #     batch_byte_value, batch_file_type = validation_data_set()
    #
    #     sess = tf.Session()
    #
    #     # Start populating the filename queue.
    #     coord = tf.train.Coordinator()
    #     tf.train.start_queue_runners(sess=sess, coord=coord)
    #
    #     x_batch, y_batch = sess.run([batch_byte_value, batch_file_type])
    #     print(x_batch, y_batch)

    def test_validation_data_set(self):
        sess = tf.Session()

        # Start populating the filename queue.
        coord = tf.train.Coordinator()
        tf.train.start_queue_runners(sess=sess, coord=coord)

        a, b, c = make_files_queue()
        print(sess.run(get_batch(1, b)))

