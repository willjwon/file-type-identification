import tensorflow as tf


# Flags to use. DO NOT MODIFY HERE!
# =================================
FLAGS = tf.app.flags.FLAGS
# =================================


# DEFINE CONSTANTS HERE!
# =================================

# model name
FLAGS.model_name = "simple_cnn"

# input directory
FLAGS.train_data_path = "/Users/barber/Development/GitHub/file-type-identification/Trainer/TrainData/7type-3group-raw-frequency-data/train_data"
FLAGS.validation_data_path = "/Users/barber/Development/GitHub/file-type-identification/Trainer/TrainData/7type-3group-raw-frequency-data/validation_data"
FLAGS.test_data_path = "/Users/barber/Development/GitHub/file-type-identification/Trainer/TrainData/7type-3group-raw-frequency-data/test_data"

# learning rate
FLAGS.learning_rate = 1e-5

# keep probability for dropout while training
FLAGS.keep_prob_train = 0.7

# global steps to repeat
FLAGS.num_of_total_global_steps = 30000

# checkpoint steps to save and validate
FLAGS.checkpoint_steps = 1000

# steps to print cost
FLAGS.cost_print_step = 100

# a mini batch's size
FLAGS.batch_size = 100

# csv information
FLAGS.num_of_fragments_per_csv = 100

# file information
FLAGS.num_of_validation_files_per_type = 50
FLAGS.num_of_test_files_per_type = 250

# type information
FLAGS.num_of_groups = 3
FLAGS.group_name = ["html", "exe", "else"]
FLAGS.num_of_types_per_group = [1, 1, 5]
# =================================
