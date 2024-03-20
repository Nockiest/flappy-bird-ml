from tensorflow import keras
# Set up the game window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)

MIN_PIPE_DIST = 150 # Minimum distance between two pipes
PIPE_GAP = 200

DEFAULT_MODEL = keras.models.load_model("nn.h5")