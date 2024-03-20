import tensorflow as tf
 
from sklearn.model_selection import train_test_split
import numpy as np
import csv

# Read and parse the CSV file
csv_filename = 'collected_data2.csv'

# Define lists to store features and labels
features = []
labels = []

# Open the CSV file and read data row by row
with open(csv_filename, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Convert each row to the appropriate data type and append to the lists
        features.append([float(row['distance_to_pipe']),
                         float(row['height_of_first_pipe']),
                         float(row['height_of_bird']),
                         float(row['velocity_y']),
                         int(row['bird_passed_pipe'])])
        labels.append(int(row['player_jumped']))

# Convert lists to numpy arrays
X = np.array(features)
y = np.array(labels)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the model
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X.shape[1],)),  # Define input shape explicitly
    tf.keras.layers.Dense(6, activation='relu'),
    tf.keras.layers.Dense(6, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

# Make predictions
predictions = model.predict(X_test)
# model.save("nn")  # no file ending = SavedModel
model.save("nn.h5")  # .h5 = HDF5

# from sklearn.preprocessing import MinMaxScaler

# # Define the MinMaxScaler
# scaler = MinMaxScaler(feature_range=(-1, 1))

# # Normalize the features
# X_normalized = scaler.fit_transform(X)

# # Split the normalized data into training and testing sets
# X_train_norm, X_test_norm, y_train, y_test = train_test_split(X_normalized, y, test_size=0.2, random_state=42)

# # Define the model
# model_norm = tf.keras.Sequential([
#     tf.keras.layers.Input(shape=(X_normalized.shape[1],)),  # Define input shape explicitly
#     tf.keras.layers.Dense(64, activation='relu'),
#     tf.keras.layers.Dense(32, activation='relu'),
#     tf.keras.layers.Dense(1, activation='sigmoid')
# ])

# # Compile the model
# model_norm.compile(optimizer='adam',
#                    loss='binary_crossentropy',
#                    metrics=['accuracy'])

# # Train the model with normalized data
# model_norm.fit(X_train_norm, y_train, epochs=20, batch_size=32, validation_data=(X_test_norm, y_test))

# # Evaluate the model with normalized data
# loss_norm, accuracy_norm = model_norm.evaluate(X_test_norm, y_test)
# print(f'Test Loss with normalized data: {loss_norm}, Test Accuracy with normalized data: {accuracy_norm}')

# # Make predictions with normalized data
# predictions_norm = model_norm.predict(X_test_norm)
# model_norm.save('nn.h5')
# # two formats: SavedModel or HDF5
