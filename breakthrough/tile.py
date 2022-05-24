## 參考程式：https://github.com/aiatuci/ChessAI/blob/main/tile.py
from  screen import *

class Tile:
    def __init__(self,piece,x,y):
        self.piece = piece
        self.x = x
        self.y = y
        self.color = BLACK
        self.surface = pygame.Surface((TILE_SIZE, TILE_SIZE))

    ## 畫顏色
    def fill(self, color):
        self.surface.fill(color)

    ## 將選擇到的格子畫顏色
    def select(self):
        if self.contains_piece():
            self.fill(HIGHLIGHT_COLOR)
            self.draw()

    ## 將格子繪製在螢幕上
    def draw(self):
        SCREEN.blit(self.surface, to_coords(self.x, self.y))
        if self.piece:
            self.piece.draw()

    ## 檢查這個格子上有沒有棋子
    def contains_piece(self):
        if self.piece.image is None:
            return False
        return True

    ## 將這個格子的狀態複製
    def copy(self):
        piece = None
        if self.piece:
            piece = self.piece.copy()
        copy = Tile(piece, self.x, self.y)
        copy.fill(self.color)
        return copy