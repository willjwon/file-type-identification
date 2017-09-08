### Constants

learning_rate = 0.001

# the ratio of training data out of total data
training_data_ratio = 0.7

num_of_epochs = 15

batch_size = 10
# TODO: data_size
data_size = 5000
batch_per_epoch = int(data_size / batch_size)

# keep probability for dropout while training
keep_prob_train = 0.7