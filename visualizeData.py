# import csv
# import matplotlib.pyplot as plt

# def visualize_csv_data(csv_filename):
#     # Initialize lists to store data
#     distance_to_pipe = []
#     height_of_first_pipe = []
#     height_of_bird = []
#     velocity_y = []
#     bird_passed_pipe = []
#     player_jumped = []

#     # Read data from CSV file
#     with open(csv_filename, 'r', newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             distance_to_pipe.append(float(row['distance_to_pipe']))
#             height_of_first_pipe.append(float(row['height_of_first_pipe']))
#             height_of_bird.append(float(row['height_of_bird']))
#             velocity_y.append(float(row['velocity_y']))
#             bird_passed_pipe.append(int(row['bird_passed_pipe']))
#             player_jumped.append(int(row['player_jumped']))

#     # Visualize the data
#     fig, axs = plt.subplots(2, 3, figsize=(15, 10))

#     axs[0, 0].plot(distance_to_pipe)
#     axs[0, 0].set_title('Distance to Pipe')

#     axs[0, 1].plot(height_of_first_pipe)
#     axs[0, 1].set_title('Height of First Pipe')

#     axs[0, 2].plot(height_of_bird)
#     axs[0, 2].set_title('Height of Bird')

#     axs[1, 0].plot(velocity_y)
#     axs[1, 0].set_title('Velocity Y')

#     axs[1, 1].plot(bird_passed_pipe)
#     axs[1, 1].set_title('Bird Passed Pipe')

#     axs[1, 2].plot(player_jumped)
#     axs[1, 2].set_title('Player Jumped')

#     plt.tight_layout()
#     plt.show()

# # Example usage:
# csv_filename = 'your_csv_file.csv'
# visualize_csv_data(csv_filename)

import csv
import matplotlib.pyplot as plt

def visualize_csv_data(csv_filename):
    # Initialize a dictionary to store data for each column
    data = {}

    # Read data from CSV file and populate the dictionary
    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key, value in row.items():
                if key not in data:
                    data[key] = []
                data[key].append(float(value))

    # Determine the number of subplots based on the number of columns
    num_columns = len(data)
    num_rows = (num_columns + 1) // 2  # Ensure at least two rows for better layout
    fig, axs = plt.subplots(num_rows, 2, figsize=(15, num_rows * 5))

    # Plot data for each column
    for i, (column, values) in enumerate(data.items()):
        row = i // 2
        col = i % 2
        ax = axs[row, col]
        ax.plot(values)
        ax.set_title(column)
        ax.set_xlabel('Index')
        ax.set_ylabel(column)

    # Hide any unused subplots
    for i in range(num_columns, num_rows * 2):
        row = i // 2
        col = i % 2
        axs[row, col].axis('off')

    plt.tight_layout()
    plt.show()

# Example usage:
csv_filename = 'collected_data.csv'
visualize_csv_data(csv_filename)