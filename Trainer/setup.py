import tensorflow as tf


# Flags to use. DO NOT MODIFY HERE!
# =================================
FLAGS = tf.app.flags.FLAGS
# =================================


# DEFINE CONSTANTS HERE!
# =================================

# model name
FLAGS.model_name = "frequency_symmetric_10_layer"

# input directory
FLAGS.train_data_path = "./TrainData/1g-nogroup-train"
FLAGS.validation_data_path = "./TrainData/1g-nogroup-validation"
FLAGS.test_data_path = "./TrainData/1g-nogroup-test"

# learning rate
FLAGS.learning_rate = 1e-4

# keep probability for dropout while training
FLAGS.keep_prob_train = 0.5

# global steps to repeat
FLAGS.num_of_total_global_steps = 40000

# checkpoint steps to save and validate
FLAGS.checkpoint_steps = 2000

# a mini batch's size
FLAGS.batch_size = 100

# csv information
FLAGS.num_of_fragments_per_csv = 100

# file information
FLAGS.num_of_validation_files_per_type = 50
FLAGS.num_of_test_files_per_type = 100

# type information
FLAGS.num_of_groups = 7
FLAGS.group_name = ["html", "exe", "mp3", "hwp", "pdf", "jpg", "png"]
# =================================
