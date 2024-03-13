# import pygame
# import random
# import tensorflow as tf
# from utils import draw_debug_info
# from globals import WINDOW_WIDTH, WINDOW_HEIGHT
# pygame.init()

# window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# pygame.display.set_caption('Flappy Bird')

# # Game variables
# background_image = pygame.image.load('assets/Objects/background.png').convert()
# background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))  # Resize background image

# bird_rect = pygame.Rect(50, WINDOW_HEIGHT // 2, 50, 50)  # Bird rectangle
# bird_dy = 0
# gravity = 0.3
# jump_strength = -5
# pipes = []
# pipe_speed = 3
# pipe_gap = 200
# last_pipe_added = 0
# bird_dead = False
# # died_after_jump = False
# # TFRecord file name
# tfrecord_filename = 'collected_data.tfrecord'

# def collect_data():
#     global bird_dead
#     if pipes and not bird_dead:
#         first_pipe = pipes[0]
#         distance_to_pipe = first_pipe.x - bird_rect.x
#         height_of_first_pipe = first_pipe.height
#         height_of_bird = bird_rect.y
#         velocity_y = bird_dy
 
#         data = {
#             'distance_to_pipe': distance_to_pipe,
#             'height_of_first_pipe': height_of_first_pipe,
#             'height_of_bird': height_of_bird,
#             'velocity_y': velocity_y,
#             'died_after_jump': 1 if bird_dead else 0
#         }
#         return data

# # Game loop
# clock = pygame.time.Clock()
 
# # Create TFRecord writer
# with tf.io.TFRecordWriter(tfrecord_filename) as writer:
#     while not bird_dead:
#         # Handle events
#         mouse_pos = pygame.mouse.get_pos()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 bird_dead = True
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_SPACE and not bird_dead  :
#                     bird_dy = jump_strength

#         # Update bird position
#         bird_dy += gravity
#         bird_rect.y += bird_dy

 
 
#         # Add pipes
#         if pygame.time.get_ticks() - last_pipe_added > 1500:
#             pipe_height = random.randint(100, 400)
#             pipes.append(pygame.Rect(WINDOW_WIDTH, 0, 50, pipe_height))
#             pipes.append(pygame.Rect(WINDOW_WIDTH, pipe_height + pipe_gap, 50, WINDOW_HEIGHT - pipe_height - pipe_gap))
#             last_pipe_added = pygame.time.get_ticks()

#         # Move pipes
#         for pipe in pipes:
#             pipe.x -= pipe_speed

#         # Remove off-screen pipes
#         pipes = [pipe for pipe in pipes if pipe.x > -50]

#         # Check for collisions
#         if not bird_dead:
#             for pipe in pipes:
#                 if bird_rect.colliderect(pipe):
#                     bird_dead = True
#             if not bird_rect.y > 0 and not bird_rect.y < WINDOW_HEIGHT:
#                 bird_dead = True
 

#         # Draw everything
#         window.fill((255, 255, 255))  # Clear the screen
#         window.blit(background_image, (0, 0))
#         pygame.draw.rect(window, (0, 255, 0), bird_rect)  # Draw bird rectangle
#         for pipe in pipes:
#             pygame.draw.rect(window, (0, 0, 255), pipe)  # Draw pipe rectangles
#         draw_debug_info(
#         {
#             'Player Y:':round( bird_rect.y),
#             'Mouse PositionY': (round(mouse_pos[0]),round(mouse_pos[1])),
#         },
#         window
#     )
#         # Update display
#         pygame.display.update()

#         # Cap the frame rate
#         clock.tick(60)

#         # Collect and write data
#         data = collect_data()
#         if data:
#             example = tf.train.Example(features=tf.train.Features(feature={
#                 'distance_to_pipe': tf.train.Feature(float_list=tf.train.FloatList(value=[data['distance_to_pipe']])),
#                 'height_of_first_pipe': tf.train.Feature(float_list=tf.train.FloatList(value=[data['height_of_first_pipe']])),
#                 'height_of_bird': tf.train.Feature(float_list=tf.train.FloatList(value=[data['height_of_bird']])),
#                 'velocity_y': tf.train.Feature(float_list=tf.train.FloatList(value=[data['velocity_y']])),
#                 'died_after_jump': tf.train.Feature(int64_list=tf.train.Int64List(value=[int(data['died_after_jump'])]))
#             }))
#             writer.write(example.SerializeToString())

#         # Check if the bird is dead and all data is collected
#         if bird_dead and len(pipes) == 0:
#             break

# # Clean up
# pygame.quit()
import pygame
import random
import tensorflow as tf
from utils import draw_debug_info
from globals import WINDOW_WIDTH, WINDOW_HEIGHT

# Initialize Pygame
pygame.init()

# Set window dimensions
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Load background image
background_image = pygame.image.load('assets/Objects/background.png').convert()
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Bird rectangle properties
bird_rect = pygame.Rect(50, WINDOW_HEIGHT // 2, 50, 50)
bird_dy = 0
gravity = 0.3
jump_strength = -5

# Pipe properties
pipes = []
pipe_speed = 3
pipe_gap = 200
last_pipe_added = 0
distance_to_pipe = -1
# Game loop variables
bird_dead = False
last_jump_died = False
tfrecord_filename = 'collected_data.tfrecord'

# Array to collect data
data_array = []

# Function to collect data
def collect_data():
    if pipes and not bird_dead:
        first_pipe = pipes[0]
        
        height_of_first_pipe = first_pipe.height
        height_of_bird = bird_rect.y
        velocity_y = bird_dy

        data = {
            'distance_to_pipe': distance_to_pipe,
            'height_of_first_pipe': height_of_first_pipe,
            'height_of_bird': height_of_bird,
            'velocity_y': velocity_y,
            'died_after_jump': int(last_jump_died),
            'bird_passed_pipe': 0
        }
        data_array.append(data)
        # print(data_array[-1 ])

# Game loop
clock = pygame.time.Clock()

while not bird_dead:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bird_dead = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not bird_dead:
                
                collect_data( )
                bird_dy = jump_strength

    # Update bird position
    bird_dy += gravity
    bird_rect.y += bird_dy

    # Add pipes
    if pygame.time.get_ticks() - last_pipe_added > 1500:
        pipe_height = random.randint(100, 400)
        pipes.append(pygame.Rect(WINDOW_WIDTH, 0, 50, pipe_height))
        pipes.append(pygame.Rect(WINDOW_WIDTH, pipe_height + pipe_gap, 50, WINDOW_HEIGHT - pipe_height - pipe_gap))
        last_pipe_added = pygame.time.get_ticks()

    # Move pipes
    for pipe in pipes:
        pipe.x -= pipe_speed
    if len(pipes) > 0:
        if abs(distance_to_pipe)   < 2 and    len(data_array) > 0:
           data_array[-1]['bird_passed_pipe'] = 1
    if pipes:
        distance_to_pipe = pipes[0].x - bird_rect.x

    # Remove off-screen pipes
    pipes = [pipe for pipe in pipes if pipe.x > -50]

    # Check for collisions
    if not bird_dead:
        for pipe in pipes:
            if bird_rect.colliderect(pipe) or not 0 < bird_rect.y < WINDOW_HEIGHT:  # Bird hits pipe or ceiling/ground
                if len(data_array) > 0:
                    data_array[-1]['bird_passed_pipe'] = -1
                bird_dead = True

    # Draw everything
    window.fill((255, 255, 255))  # Clear the screen
    window.blit(background_image, (0, 0))
    pygame.draw.rect(window, (0, 255, 0), bird_rect)  # Draw bird rectangle
    for pipe in pipes:
        pygame.draw.rect(window, (0, 0, 255), pipe)  # Draw pipe rectangles
    draw_debug_info({
        'Player Y:': round(bird_rect.y),
    }, window)
    # Update display
    pygame.display.update()

    # Cap the frame rate
    clock.tick(60)

    # Collect data
    collect_data()

# Create TFRecord writer and write collected data
with tf.io.TFRecordWriter(tfrecord_filename) as writer:
    for data in data_array:
        example = tf.train.Example(features=tf.train.Features(feature={
            'distance_to_pipe': tf.train.Feature(float_list=tf.train.FloatList(value=[data['distance_to_pipe']])),
            'height_of_first_pipe': tf.train.Feature(float_list=tf.train.FloatList(value=[data['height_of_first_pipe']])),
            'height_of_bird': tf.train.Feature(float_list=tf.train.FloatList(value=[data['height_of_bird']])),
            'velocity_y': tf.train.Feature(float_list=tf.train.FloatList(value=[data['velocity_y']])),
            'bird_passed_pipe': tf.train.Feature(int64_list=tf.train.Int64List(value=[data['bird_passed_pipe']]))
        }))
        writer.write(example.SerializeToString())

# Clean up
pygame.quit()
 