import tensorflow as tf
import numpy as np

tf.set_random_seed(1234)

# constants
learning_rate = 0.001
training_data_ratio = 0.7
num_of_epochs = 15
batch_size = 1000

# read inputs from csv file
input_data = np.loadtxt('frequency_test.csv', delimiter=',', dtype=np.float32)

data_size = int(input_data.size / 261)  # 261 : 256(byte value) + 5(file types)
training_data_size = int(data_size * training_data_ratio)

training_data = input_data[0:training_data_size, :]
testing_data = input_data[training_data_size:, :]

# input placeholders
# x: byte value (0 ~ 255)
# y: 5 file types in one hot encoding
X = tf.placeholder(tf.float32, [None, 256])
Y = tf.placeholder(tf.float32, [None, 5])

# keep probability placeholder for dropout
keep_prob = tf.placeholder(tf.float32)

# weights & bias
with tf.variable_scope("layer1"):
    W1 = tf.get_variable(name="W1", shape=[256, 512], initializer=tf.contrib.layers.xavier_initializer())
    b1 = tf.Variable(tf.random_normal([512]))
    L1 = tf.nn.relu(tf.matmul(X, W1) + b1)
    L1 = tf.nn.dropout(L1, keep_prob=keep_prob)

with tf.variable_scope("layer2"):
    W2 = tf.get_variable(name="W2", shape=[512, 512], initializer=tf.contrib.layers.xavier_initializer())
    b2 = tf.Variable(tf.random_normal([512]))
    L2 = tf.nn.relu(tf.matmul(L1, W2) + b2)
    L2 = tf.nn.dropout(L2, keep_prob=keep_prob)

with tf.variable_scope("layer3"):
    W3 = tf.get_variable(name="W3", shape=[512, 512], initializer=tf.contrib.layers.xavier_initializer())
    b3 = tf.Variable(tf.random_normal([512]))
    L3 = tf.nn.relu(tf.matmul(L2, W3) + b3)
    L3 = tf.nn.dropout(L3, keep_prob=keep_prob)

with tf.variable_scope("layer4"):
    W4 = tf.get_variable(name="W4", shape=[512, 512], initializer=tf.contrib.layers.xavier_initializer())
    b4 = tf.Variable(tf.random_normal([512]))
    L4 = tf.nn.relu(tf.matmul(L3, W4) + b4)
    L4 = tf.nn.dropout(L4, keep_prob=keep_prob)

with tf.variable_scope("layer5"):
    W5 = tf.get_variable(name="W5", shape=[512, 512], initializer=tf.contrib.layers.xavier_initializer())
    b5 = tf.Variable(tf.random_normal([512]))
    L5 = tf.nn.relu(tf.matmul(L4, W5) + b5)
    L5 = tf.nn.dropout(L5, keep_prob=keep_prob)

with tf.variable_scope("layer6"):
    W6 = tf.get_variable(name="W6", shape=[512, 512], initializer=tf.contrib.layers.xavier_initializer())
    b6 = tf.Variable(tf.random_normal([512]))
    L6 = tf.nn.relu(tf.matmul(L5, W6) + b6)
    L6 = tf.nn.dropout(L6, keep_prob=keep_prob)

with tf.variable_scope("layer7"):
    W7 = tf.get_variable(name="W7", shape=[512, 512], initializer=tf.contrib.layers.xavier_initializer())
    b7 = tf.Variable(tf.random_normal([512]))
    L7 = tf.nn.relu(tf.matmul(L6, W7) + b7)
    L7 = tf.nn.dropout(L7, keep_prob=keep_prob)

with tf.variable_scope("layer8"):
    W8 = tf.get_variable(name="W8", shape=[512, 10], initializer=tf.contrib.layers.xavier_initializer())
    b8 = tf.Variable(tf.random_normal([10]))
    hypothesis = tf.nn.relu(tf.matmul(L7, W8) + b8)

# cost function & optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
    logits=hypothesis, labels=Y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

sess = tf.Session()
sess.run(tf.global_variables_initializer())

# train the model
for epoch in range(num_of_epochs):
    avg_cost = 0
    batches_per_epoch = int(data_size / batch_size)

    min_queue_examples = batch_size * 100
    capacity = min_queue_examples + 3 * batch_size

    for batch in range(batches_per_epoch):
        batch_data = tf.train.shuffle_batch_join(
            training_data,
            batch_size=batch_size,
            min_queue_examples=min_queue_examples,
            capacity=capacity)

        batch_x = batch_data[:, 0:256]
        batch_y = batch_data[:, 256:]

        feed_dict = {X: batch_x, Y: batch_y}
        c, _ = sess.run([cost, optimizer], feed_dict=feed_dict)
        avg_cost += c / batches_per_epoch

    print("Epoch:", "{:0>4}".format(epoch + 1), "cost:", "{:.9f}".format(avg_cost))

print("Learning Completed")

# test the model
test_x = testing_data[:, 0:256]
test_y = testing_data[:, 256:]

correct_prediction = tf.equal(tf.argmax(hypothesis, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

feed_dict = {X: test_x, Y: test_y, keep_prob: 1}
print("Accuracy:", sess.run(accuracy, feed_dict=feed_dict))
