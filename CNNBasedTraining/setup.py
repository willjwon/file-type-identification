import tensorflow as tf

"""
==================================================
================== Constants =====================
==================================================
"""

# Flags to use. DO NOT MODIFY HERE!
# =================================
FLAGS = tf.app.flags.FLAGS
# =================================


# DEFINE CONSTANTS HERE!
# =================================

# input directory
FLAGS.train_data_path = "./train_data"
FLAGS.validation_data_path = "./validation_data"
FLAGS.test_data_path = "./test_data"

# directory for tensorboard summary
FLAGS.tensorboard_directory = './tensorboard/train1'

# model's output directory
FLAGS.model_output_directory = "./model"

# learning rate
FLAGS.learning_rate = 1e-4

# keep probability for dropout while training
FLAGS.keep_prob_train = 0.5

# global steps to repeat
FLAGS.num_of_total_global_steps = 3000

# checkpoint steps to save and validate
FLAGS.checkpoint_steps = 100

# a mini batch's size
FLAGS.batch_size = 100

# csv information
FLAGS.num_of_fragments_per_csv = 100
# =================================
