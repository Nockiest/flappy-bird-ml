import csv
from tensorflow import keras
import pygame
import random
import tensorflow as tf
from utils import draw_debug_info
from globals import WINDOW_WIDTH, WINDOW_HEIGHT,MIN_PIPE_DIST,PIPE_GAP
import numpy as np
from bird import Bird
from pipe import Pipe
# Initialize Pygame
pygame.init()

# Set window dimensions
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Load background image
background_image = pygame.image.load('assets/Objects/background.png').convert()
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Bird rectangle properties
gravity = 0.1
jump_strength = -5

# Pipe properties
pipes = []
birds = []
dead_birds = []
num_birds = 1 
pipe_speed = 3

distance_to_pipe = -1
 
# Game loop
fieldnames = ['distance_to_pipe', 'top_edge', 'bottom_edge','height_of_bird', 'velocity_y'] # player jumped 'died_after_jump',  'bird_passed_pipe'
new_model = keras.models.load_model("nn.h5")
for _ in range(num_birds):
    bird = Bird(   )
    birds.append(bird)

def add_pipe():
    pipe_height = random.randint(100, 400)
    pipe =  Pipe( pipe_speed, pipe_height)
    pipes.append(pipe)
def spawn_next_generation(dead_birds):
    new_generation = []

    # Sort dead birds by fitness in descending order
    dead_birds_sorted = sorted(dead_birds, key=lambda bird: bird.fitness, reverse=True)

    for _ in range(len(dead_birds)):
        # Calculate cumulative probabilities based on fitness
        cumulative_probabilities = [bird.fitness for bird in dead_birds_sorted]
        cumulative_probabilities = [sum(cumulative_probabilities[:i+1]) for i in range(len(cumulative_probabilities))]

        # Select a random bird based on fitness
        rand_val = random.random()
        selected_bird = None
        for i, prob in enumerate(cumulative_probabilities):
            if rand_val < prob:
                selected_bird = dead_birds_sorted[i]
                break

        # Create a new bird with the brain of the selected bird
        new_bird = Bird(neural_network=selected_bird.neural_network )  # Replace (0, 0) with desired initial position
        new_generation.append(new_bird)

    return new_generation
 
def calculate_fitness():
    total_score = sum(bird.score for bird in dead_birds)
    if total_score != 0:
        for bird in dead_birds:
            bird.fitness = bird.score / total_score
    else:
        # Handle the case where total_score is zero (e.g., set fitness to a default value)
        # For example, you could set fitness to 0 for all birds.
        for bird in dead_birds:
            bird.fitness = 1/dead_birds

# Game loop
clock = pygame.time.Clock()
running  = True
frame_num = 0
batch = 10
add_pipe()
while running:
    
    frame_num += 1

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Add pipes
    if len(pipes) == 0:
        add_pipe()

    if pipes[-1].get_x( ) < WINDOW_WIDTH - MIN_PIPE_DIST :
        add_pipe()

    for pipe in pipes:
        pipe.update()
     
    if pipes:
        distance_to_pipe = pipes[0].rects[0].x - birds[0].rect.x

    # Remove off-screen pipes
    pipes = [pipe for pipe in pipes if pipe.check_in_screen( )]
    for i, bird in enumerate(birds):
        if bird.check_death(pipes):
            dead_birds.append(bird)
            del birds[i]
            print(birds, dead_birds)

    for bird in birds:
        bird.update(pipes)

    # Draw everything
    window.fill((255, 255, 255))  # Clear the screen
    window.blit(background_image, (0, 0))
    for pipe in pipes:
        pipe.draw(window)
    for bird in birds:
        bird.draw(window)
    draw_debug_info({
        'num birds': str(len(birds)),
        # 'Player Y:': round(bird_rect.y),
        # 'Prediction Value:': prediction,
        # 'Should Jump:': str(prediction > 0.5),
    }, window)

    if len(birds)==0:
         
        pipes = []
        calculate_fitness()
        birds = spawn_next_generation(dead_birds)
        dead_birds = []
        print(birds)
        # apply logic to spawn children
    # Update display
    pygame.display.update()

    # Cap the frame rate
    clock.tick(60)



# Clean up
pygame.quit()

 # if pipes:
    # prediction = predict_jump(distance_to_pipe,  pipes[0].height,  bird_rect.y, bird_dy,  abs(distance_to_pipe) < 2)
    # if len(pipes) > 0:
    #     if abs(distance_to_pipe) < 2 and len(data_array) > 0:
    #         data_array[-1]['bird_passed_pipe'] = 1
    # if frame_num % batch == 0:
    #     print('collecting data      ')
    #     collect_data()
  # Check for collisions
    # if not bird_dead:
    #     for pipe in pipes:
    #         if bird_rect.colliderect(pipe) or not 0 < bird_rect.y < WINDOW_HEIGHT:  # Bird hits pipe or ceiling/ground
    #             if len(data_array) > 0:
    #                 data_array[-1]['bird_passed_pipe'] = -1
    #             bird_dead = True

  # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE and not bird_dead:
        #         # collect_data(True)
        #         if len(data_array) > 0:
        #             data_array[-1]['player_jumped'] = 1
        #         bird_dy = jump_strength
 # Make the bird jump if prediction is higher than 0.5
    # if prediction > 0.5 and not bird_dead:
    #     if len(data_array) > 0:
    #         data_array[-1]['player_jumped'] = 1
    #     bird_dy = jump_strength

    # Move pipes
#  def collect_data(player_jumped: bool = False):
#     # def collect_data(player_jumped: bool = False):
#     if pipes and not bird_dead:
#         first_pipe = pipes[0]

#         height_of_first_pipe = first_pipe.height
#         height_of_bird = bird_rect.y
#         velocity_y = bird_dy

#         data = {
#             'distance_to_pipe': distance_to_pipe,
#             'height_of_first_pipe': height_of_first_pipe,
#             'height_of_bird': height_of_bird,
#             'velocity_y': velocity_y,
#             'died_after_jump': int(last_jump_died),
#             'player_jumped': 1 if  player_jumped else 0,
#             'bird_passed_pipe': 0
#         }
#         data_array.append(data)
    # if pipes and not bird_dead:
    #     first_pipe = pipes[0]

    #     height_of_first_pipe = first_pipe.height
    #     height_of_bird = bird_rect.y
    #     velocity_y = bird_dy

    #     # Normalize the collected data
    #     normalized_distance_to_pipe = scaler.fit_transform(np.array(distance_to_pipe).reshape(-1, 1))[0][0]
    #     normalized_height_of_first_pipe = scaler.fit_transform(np.array(height_of_first_pipe).reshape(-1, 1))[0][0]
    #     normalized_height_of_bird = scaler.fit_transform(np.array(height_of_bird).reshape(-1, 1))[0][0]
    #     normalized_velocity_y = scaler.fit_transform(np.array(velocity_y).reshape(-1, 1))[0][0]

    #     data = {
    #         'distance_to_pipe': normalized_distance_to_pipe,
    #         'height_of_first_pipe': normalized_height_of_first_pipe,
    #         'height_of_bird': normalized_height_of_bird,
    #         'velocity_y': normalized_velocity_y,
    #         'died_after_jump': int(last_jump_died),
    #         'player_jumped': 1 if player_jumped else 0,
    #         'bird_passed_pipe': 0
    #     }
    #     data_array.append(data)
# def preprocess_input_data(distance_to_pipe, height_of_first_pipe, height_of_bird, velocity_y, bird_passed_pipe):
#     # Preprocess the input data as required by the model (e.g., scaling, normalization)
#     # Convert input data into a numpy array with the appropriate shape
#     input_data = np.array([[distance_to_pipe, height_of_first_pipe, height_of_bird, velocity_y, bird_passed_pipe]])
#     return input_data
# def predict_jump(distance_to_pipe, height_of_first_pipe, height_of_bird, velocity_y, bird_passed_pipe):
#     input_data = preprocess_input_data(distance_to_pipe, height_of_first_pipe, height_of_bird, velocity_y, bird_passed_pipe)
#     prediction = new_model.predict(input_data)
#     return prediction

# from sklearn.preprocessing import MinMaxScaler

# # Define the MinMaxScaler
# scaler = MinMaxScaler(feature_range=(-1, 1))


# # Define the CSV filename
# csv_filename = 'collected_data.csv'
# # Array to collect data
# data_array = []

# Write the collected data to the CSV file
# with open(csv_filename, 'a', newline='') as csvfile:  # Open in append mode ('a')
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#     # Write the data
#     for data in data_array:
#         writer.writerow(data)