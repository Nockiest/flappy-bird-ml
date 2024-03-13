# import tensorflow as tf
# from tensorflow.keras import layers

# # Define the neural network model
# model = tf.keras.Sequential([
#     layers.Dense(64, activation='relu', input_shape=(input_shape,)),
#     layers.Dense(64, activation='relu'),
#     layers.Dense(num_actions, activation='softmax')
# ])

# # Compile the model
# model.compile(optimizer='adam',
#               loss='sparse_categorical_crossentropy',
#               metrics=['accuracy'])

# # Train the model
# model.fit(X_train, y_train, epochs=num_epochs, batch_size=batch_size, validation_data=(X_val, y_val))

# # Evaluate the model
# test_loss, test_accuracy = model.evaluate(X_test, y_test)
# print('Test accuracy:', test_accuracy)

import tensorflow as tf

# Define the feature description for parsing the TFRecord
feature_description = {
    'distance_to_pipe': tf.io.FixedLenFeature([], tf.float32),
    'height_of_first_pipe': tf.io.FixedLenFeature([], tf.float32),
    'height_of_bird': tf.io.FixedLenFeature([], tf.float32),
    'velocity_y': tf.io.FixedLenFeature([], tf.float32),
     'bird_passed_pipe': tf.io.FixedLenFeature([], tf.int64)
}

# Function to parse a single example from the TFRecord
def parse_tfrecord_fn(example):
    example = tf.io.parse_single_example(example, feature_description)
    features = {
        'distance_to_pipe': example['distance_to_pipe'],
        'height_of_first_pipe': example['height_of_first_pipe'],
        'height_of_bird': example['height_of_bird'],
        'velocity_y': example['velocity_y'],
        'bird_passed_pipe': example['bird_passed_pipe']
    }
    return features

# Read and parse the TFRecord file
tfrecord_filename = 'collected_data.tfrecord'
dataset = tf.data.TFRecordDataset(tfrecord_filename)
parsed_dataset = dataset.map(parse_tfrecord_fn)

# Example usage: Iterate through the parsed dataset and print each example
for example in parsed_dataset:
    print("Distance to pipe:", example['distance_to_pipe'].numpy())
    print("Height of first pipe:", example['height_of_first_pipe'].numpy())
    print("Height of bird:", example['height_of_bird'].numpy())
    print("Velocity y:", example['velocity_y'].numpy())
    print('bird_passed_pipe', example['bird_passed_pipe'].numpy())
    print()