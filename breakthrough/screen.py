# 參考資料：https://github.com/aiatuci/ChessAI/blob/main/settings.py
import pygame

# Screen大小與格子大小
TILE_SIZE = 64
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_SIZE = TILE_SIZE * 8
BOARD_X = (SCREEN_WIDTH-BOARD_SIZE)//2
BOARD_Y = int((SCREEN_HEIGHT / 2) - (BOARD_SIZE / 2))
IMG_SCALE = (TILE_SIZE, TILE_SIZE)

# 選手的Color
WHITE = (255,255,255)
BLACK = (0,0,0)

# Game colors
SMALL_TEXT_COLOR = (241, 250, 238)
LARGE_TEXT_COLOR = (230, 57, 70)
BG_COLOR = (100, 66, 55)
BG_COLOR_LIGHT = (100, 70, 70)
TILE_COLOR_LIGHT = (232, 208, 170)
TILE_COLOR_DARK = (166, 125, 93)
HIGHLIGHT_COLOR = (243, 202, 82)
CAN_MOVE_COLOR = (255, 230, 140)

# Create screen
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 轉換螢幕位置為格子位置
def to_coords(x, y):
    return BOARD_X + x * TILE_SIZE, BOARD_Y + y * TILE_SIZE