import os

# Settings
WIDTH = 380
HEIGHT = 560
TITLE = 'My Game'
FPS = 60
DEBUG = False

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Properties
BIRD_VEL = 100
BIRD_ACC = 20
BIRD_JUMP_VEL = 350
BIRD_ROT_SPEED = 60
BIRD_JUMP_ROT = 18

# Folders
game_folder = os.path.dirname(__file__)
assets_folder = os.path.join(game_folder, "assets")
fonts_folder = os.path.join(assets_folder, "fonts")
sprites_folder = os.path.join(assets_folder, "sprites")
sounds_folder = os.path.join(assets_folder, "sounds")

# Sprite Coordinates
class Sprite:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

BG_DAY = Sprite(0, 0, 144, 256)
BG_NIGHT = Sprite(146, 0, 144, 256)
BASE = Sprite(292, 0, 168, 56)
BIRD_1 = Sprite(31, 491, 17, 12)
BIRD_2 = Sprite(59, 491, 17, 12)
BIRD_3 = Sprite(3, 491, 17, 12)
PIPE_TOP = Sprite(56, 323, 26, 160)
GET_READY = Sprite(295, 59, 92, 25)
FLAPPY_BIRD_TEXT = Sprite(351, 91, 89, 24)
GAME_OVER_TEXT = Sprite(395, 59, 96, 21)
LEADERBOARD = Sprite(414, 118, 52, 29)
YELLOW_BIRD = Sprite(31, 491, 17, 12)
PLAY_BTN = Sprite(354, 118, 52, 29)