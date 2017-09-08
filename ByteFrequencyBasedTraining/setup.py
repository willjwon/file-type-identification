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

# learning rate
FLAGS.learning_rate = 1e-4

# keep probability for dropout while training
keep_prob_train = 0.7

# number of epochs to repeat training
FLAGS.num_of_epochs = 15

# a mini batch's size
FLAGS.batch_size = 10

# total data size
FLAGS.num_of_total_fragments = 500

# csv information
FLAGS.fragments_per_csv = 100

# keep probability for dropout while training
keep_prob_train = 0.7

# directory for tensorboard summary
FLAGS.tensorboard_directory = './tensorboard/train1'
# =================================
