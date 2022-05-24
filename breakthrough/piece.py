## 參考程式：https://github.com/aiatuci/ChessAI/blob/main/piece.py
import os
from screen import *

white = pygame.image.load(os.path.join("img", "pawn-white.png"))
black = pygame.image.load(os.path.join("img", "pawn-black.png"))

IMAGES = [pygame.transform.scale(white, IMG_SCALE),
          pygame.transform.scale(black, IMG_SCALE),]

class Piece:

    def __init__(self, x, y, color,image):
        self.x = x
        self.y = y
        self.color = color
        self.image = image
    
    def draw(self):
        if(self.color == WHITE):
            SCREEN.blit(IMAGES[self.image],to_coords(self.x, self.y))
        else:
            SCREEN.blit(IMAGES[self.image],to_coords(self.x, self.y))
    def move(self,x,y):
        self.x = x
        self.y = y

    def copy(self):
        copy = type(self)(self.x, self.y, self.color, self.image)
        return copy


    # 回傳所以可以移動的地方
    def valid_moves(self, board):
        moves = []
        attacks = []
        # Player Move
        if(board.bottomPlayerTurn):
            # move forward
            if(board.valid_move((self.x, self.y-1), self.color) \
                and not board.piece_at_coords((self.x, self.y-1)) \
                    and not board.enemy_at_coords((self.x, self.y-1), self.color)):
                moves.append((self.x, self.y-1))
            # Attack diagonal left
            if board.valid_move((self.x-1, self.y-1), self.color) \
                    or board.enemy_at_coords((self.x-1, self.y-1), self.color):
                moves.append((self.x-1, self.y-1))
                attacks.append((self.x-1, self.y-1))
            # Attack diagonal right
            if board.valid_move((self.x+1, self.y-1), self.color) \
                    or board.enemy_at_coords((self.x+1, self.y-1), self.color):
                moves.append((self.x+1, self.y-1))
                attacks.append((self.x+1, self.y-1))
        else:        # AI Move
            # move forward
            if(board.valid_move((self.x, self.y+1), self.color) \
                and not board.piece_at_coords((self.x, self.y+1))\
                    and not board.enemy_at_coords((self.x, self.y+1), self.color)):
                moves.append((self.x, self.y+1))
            # Attack diagonal left
            if board.valid_move((self.x-1, self.y+1), self.color) \
                    or board.enemy_at_coords((self.x-1, self.y+1), self.color):
                moves.append((self.x-1, self.y+1))
                attacks.append((self.x-1, self.y+1))
            # Attack diagonal right
            if board.valid_move((self.x+1, self.y+1), self.color) \
                    or board.enemy_at_coords((self.x+1, self.y+1), self.color):
                moves.append((self.x+1, self.y+1))
                attacks.append((self.x+1, self.y+1))
        return list(set(moves))

    ## 回傳所有可以攻擊的地方
    def valid_attacks(self, board):
        moves = []
        attacks = []
        # Player Move
        if(board.bottomPlayerTurn):
            # move forward
            if(board.valid_move((self.x, self.y-1), self.color) \
                and not board.piece_at_coords((self.x, self.y-1)) \
                    and not board.enemy_at_coords((self.x, self.y-1), self.color)):
                moves.append((self.x, self.y-1))
            # Attack diagonal left
            if board.valid_move((self.x-1, self.y-1), self.color) \
                    and board.enemy_at_coords((self.x-1, self.y-1), self.color):
                moves.append((self.x-1, self.y-1))
                attacks.append((self.x-1, self.y-1))
            # Attack diagonal right
            if board.valid_move((self.x+1, self.y-1), self.color) \
                    and board.enemy_at_coords((self.x+1, self.y-1), self.color):
                moves.append((self.x+1, self.y-1))
                attacks.append((self.x+1, self.y-1))
        else:        # AI Move
            # move forward
            if(board.valid_move((self.x, self.y+1), self.color) \
                and not board.piece_at_coords((self.x, self.y+1))\
                    and not board.enemy_at_coords((self.x, self.y+1), self.color)):
                moves.append((self.x, self.y+1))
            # Attack diagonal left
            if board.valid_move((self.x-1, self.y+1), self.color) \
                    and board.enemy_at_coords((self.x-1, self.y+1), self.color):
                moves.append((self.x-1, self.y+1))
                attacks.append((self.x-1, self.y+1))
            # Attack diagonal right
            if board.valid_move((self.x+1, self.y+1), self.color) \
                    and board.enemy_at_coords((self.x+1, self.y+1), self.color):
                moves.append((self.x+1, self.y+1))
                attacks.append((self.x+1, self.y+1))
        return list(set(attacks))

