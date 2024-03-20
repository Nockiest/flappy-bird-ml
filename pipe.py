import pygame
from globals import WINDOW_WIDTH,PIPE_GAP
class Pipe:
    def __init__(self, speed, top_edge, gap=PIPE_GAP,  color=(0, 0, 255)):
        self.rects = [pygame.Rect(WINDOW_WIDTH + 200, 0, 50, top_edge), pygame.Rect(WINDOW_WIDTH + 200, top_edge + PIPE_GAP, 50, top_edge  - PIPE_GAP) ] # Bird rectangle
        self.color = color  # Bird color
        self.speed = speed
        self.gap = gap
        self.top_edge = top_edge

    def get_x(self):
        return self.rects[0].x
    def jump(self):
        self.velocity_y = self.jump_strength  # Set velocity to jump strength

    def update(self):
        for rect in self.rects:
           rect.x -= self.speed

    def check_in_screen(self):
        return self.rects[0].x > 0


    def draw(self, window):
        for rect in self.rects:
           pygame.draw.rect(window, self.color, rect)  # Draw colored rectangle representing the bird
