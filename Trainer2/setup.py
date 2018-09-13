import tensorflow as tf


# Flags to use. DO NOT MODIFY HERE!
# =================================
FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string('model_name', ' ', ' ')
tf.app.flags.DEFINE_string('train_data_path', ' ', ' ')
tf.app.flags.DEFINE_string('validation_data_path', ' ', ' ')
tf.app.flags.DEFINE_string('test_data_path', ' ', ' ')
tf.app.flags.DEFINE_float('learning_rate', 0.0, ' ')
tf.app.flags.DEFINE_float('keep_prob_train', 0.0, ' ')
tf.app.flags.DEFINE_integer('input_dimension', 0, ' ')
tf.app.flags.DEFINE_integer('num_of_total_global_steps', 0, ' ')
tf.app.flags.DEFINE_integer('checkpoint_steps', 0, ' ')
tf.app.flags.DEFINE_integer('cost_print_step', 0, ' ')
tf.app.flags.DEFINE_integer('batch_size', 0, ' ')
tf.app.flags.DEFINE_integer('num_of_fragments_per_csv', 0, ' ')
tf.app.flags.DEFINE_integer('num_of_validation_files_per_type', 0, ' ')
tf.app.flags.DEFINE_integer('num_of_test_files_per_type', 0, ' ')
tf.app.flags.DEFINE_integer('num_of_groups', 0, ' ')
tf.app.flags.DEFINE_string('group_name', ' ', ' ')
tf.app.flags.DEFINE_string('num_of_types_per_group', ' ', ' ')
# =================================


# DEFINE CONSTANTS HERE!
# =================================

# model name
FLAGS.model_name = "mlp"

# input directory
FLAGS.train_data_path = "/Users/barber/Data/theory_data/train"
FLAGS.validation_data_path = "/Users/barber/Data/theory_data/validation"
FLAGS.test_data_path = "/Users/barber/Data/theory_data/test"

# ln earning rate
FLAGS.learning_rate = 1e-4

# keep probability for dropout while training
FLAGS.keep_prob_train = 0.9

# input dimension
FLAGS.input_dimension = 768

# global steps to repeat
FLAGS.num_of_total_global_steps = 10000

# checkpoint steps to save and validate
FLAGS.checkpoint_steps = 100

# steps to print cost
FLAGS.cost_print_step = 5

# a mini batch's size
FLAGS.batch_size = 100

# csv information
FLAGS.num_of_fragments_per_csv = 100

# file information
FLAGS.num_of_validation_files_per_type = 3
FLAGS.num_of_test_files_per_type = 1

# type information
FLAGS.num_of_groups = 3
FLAGS.group_name = ["a", "b", "c"]
FLAGS.num_of_types_per_group = [1, 1, 1]
# =================================
