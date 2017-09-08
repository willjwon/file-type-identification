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

# learning rate
FLAGS.learning_rate = 0.001

# the ratio of training data out of total data
FLAGS.training_data_ratio = 0.7

# number of epochs to repeat training
FLAGS.num_of_epochs = 15

# a mini batch's size
FLAGS.batch_size = 10

# total data size
FLAGS.data_size = 5000

# number of mini batches per one epoch
FLAGS.batch_per_epoch = int(FLAGS.data_size / FLAGS.batch_size)

# keep probability for dropout while training
keep_prob_train = 0.7

# directory for tensorboard summary
FLAGS.tensorboard_directory = './tensorboard/train1'
# =================================
