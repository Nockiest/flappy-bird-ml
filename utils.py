import pygame
from globals import WINDOW_WIDTH, WINDOW_HEIGHT, WHITE
def draw_debug_info(debug_info, window):
    font = pygame.font.Font(None, 24)  # Choose a font and size
    x_offset = 10  # Offset from the right edge of the window
    y_offset = 10  # Offset from the top of the window
    line_height = 30  # Height of each line
    for label, value in debug_info.items():
        text_surface = font.render(f'{label}: {value}', True, WHITE)
        window.blit(text_surface, (WINDOW_WIDTH - x_offset - text_surface.get_width(), y_offset))
        y_offset += line_height