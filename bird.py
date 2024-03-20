import pygame
import numpy as np
import random 
from globals import WINDOW_HEIGHT,PIPE_GAP, DEFAULT_MODEL

class Bird:
    def __init__(self, neural_network =  None,  initial_position=(50, random.randint(0, WINDOW_HEIGHT) ),   gravity=0.3, jump_strength=-5, color=(255, 0, 0)    ):
        
        if neural_network == None:
            print("using default ml")
            self.neural_network = DEFAULT_MODEL
        else:
            self.neural_network = neural_network  # Neural network for making jump decisions
            self.learn( )
        self.rect = pygame.Rect(initial_position[0], initial_position[1], 50, 50)  # Bird rectangle
        self.decision_treshhold = 0.5
        self.velocity_y = 0  # Vertical velocity
        self.gravity = gravity  # Gravity affecting the bird
        self.jump_strength = jump_strength  # Strength of jump
        self.color = color  # Bird color
        self.score = 0
        self.fitness = 0

    def jump(self):
        self.velocity_y = self.jump_strength  # Set velocity to jump strength
    def decide_jump(self,  pipes  ):
        def find_closest_pipe():
            closest = None
            closestD = float('inf')
            for pipe in pipes:
                distance =  pipe.rects[0].x - self.rect.x
                if  distance < closestD and  distance > 0:
                    closest = pipe
                    closestD = distance
            return closest
        pipe = find_closest_pipe()

        input_data = np.array([[pipe.get_x() - self.rect.x, pipe.top_edge,pipe.top_edge +PIPE_GAP, self.rect.y, self.velocity_y ]])
        prediction = self.neural_network.predict(input_data)[0]

        # print(prediction, prediction  > self.decision_treshhold )
        if prediction > self.decision_treshhold  :
            return True  
        else:
            return False  # Don't jump
    def update(self, pipes):
        self.velocity_y += self.gravity  # Apply gravity
        self.rect.y += self.velocity_y  # Update vertical position
        self.score += 1
        if   self.decide_jump(pipes):
            self.jump()
    def check_death(self, pipes):
        # Check for collision with pipes or if bird is out of bounds
        for pipe in pipes:
            for rect in pipe.rects:
                if self.rect.colliderect(rect):
                    return True  # Collision detected

        return not 0 < self.rect.y < WINDOW_HEIGHT  # Out of bounds
    def learn(self):
    # Adjust the weights of the neural network model (mutation)
        print(self.neural_network.weights[2][0])
        # for layer in self.neural_network.layers:
        #     if hasattr(layer, 'weights'):
        #         weights = layer.weights
        #         if not isinstance(weights, np.ndarray):
        #             # Convert each element to a NumPy array and ensure consistent shape
        #             weights = [np.array(w) if isinstance(w, list) else np.array([w]) for w in weights]
        #             max_shape = max(w.shape for w in weights)
        #             weights = [np.pad(w, [(0, max_shape[0] - w.shape[0])] if len(w.shape) == 1 else [(0, 0), (0, max_shape[1] - w.shape[1])]) for w in weights]
                    
        #         noise = np.random.normal(loc=0, scale=0.1, size=weights[0].shape)  # Add random noise to the weights
        #         weights += noise  # Perturb the weights

        #         if not isinstance(layer.weights, np.ndarray):
        #             # Convert the modified weights back to the original format
        #             start = 0
        #             new_weights = []
        #             for original_weight in layer.weights:
        #                 length = len(np.array(original_weight).flatten())
        #                 new_weights.append(weights[start:start + length])
        #                 start += length
        #             weights = new_weights

        #         layer.weights = weights.tolist()  # Convert back to list if necessary

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)  # Draw colored rectangle representing the bird
