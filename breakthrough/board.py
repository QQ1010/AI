## 參考程式：https://github.com/aiatuci/ChessAI/blob/main/board.py
from screen import *
from tile import *
from piece import *

class Board():
    def __init__(self,player_color):
        self.tilemap = [[None for i in range(8)] for j in range(8)]
        self.player_color = player_color
        self.gameover = None
        self.selected = None
        self.balck_num = 16                                ## 黑棋目前盤面上的數量
        self.white_num = 16                                ## 白棋目前盤面上的數量
        self.turn = BLACK
        if self.player_color == BLACK:
            self.bottomPlayerTurn = True
        else:
            self.bottomPlayerTurn = False
        self.blackScore = 104                              ## for heuristic distance => 每個棋子和底線的距離，越小越好
        self.whiteScore = 104                              ## for heuristic distance => 每個棋子和底線的距離，越小越好
        self.initialize_tiles()
        self.past_moves = []                               ## 將上一步記起來，可以回上一步


    ## 將棋子初始化，繪製在盤面上
    def initialize_piece(self) -> None:
        for x in range(8):
            for y in range(8):
                self.tilemap[x][y].piece = None
        if(self.player_color == WHITE):
            for i in range(8):
                self.tilemap[i][0].piece = Piece(i,0,BLACK,1)
                self.tilemap[i][1].piece = Piece(i,1,BLACK,1)
                self.tilemap[i][6].piece = Piece(i,6,WHITE,0)
                self.tilemap[i][7].piece = Piece(i,7,WHITE,0)
        else:
            for i in range(8):
                self.tilemap[i][0].piece = Piece(i,0,WHITE,0)
                self.tilemap[i][1].piece = Piece(i,1,WHITE,0)
                self.tilemap[i][6].piece = Piece(i,6,BLACK,1)
                self.tilemap[i][7].piece = Piece(i,7,BLACK,1)
    
    ## 將棋盤初始化
    def initialize_tiles(self) -> None:
        cnt = 0
        for x in range(8):
            for y in range(8):
                tile = Tile(None, x, y)
                if cnt % 2 == 0:
                    tile.color = TILE_COLOR_LIGHT
                    tile.fill(TILE_COLOR_LIGHT)
                else:
                    tile.color = TILE_COLOR_DARK
                    tile.fill(TILE_COLOR_DARK)
                self.tilemap[x][y] = tile
                cnt += 1
            cnt += 1
    
    ## 將棋盤畫在螢幕上
    def draw(self) -> None:
        for row in self.tilemap:
            for tile in row:
                tile.draw()
    
    ## 當玩家選擇某個棋子，判斷並移動
    def select(self) -> None:

        # 取得滑鼠位置
        pos = pygame.mouse.get_pos()

        # 將滑鼠位置轉換成格子位置
        x = (pos[0] - BOARD_X) // TILE_SIZE
        y = (pos[1] - BOARD_Y) // TILE_SIZE
        coords = x, y

        # 檢查當前是否為玩家的回合
        if(self.player_color != self.turn):
            return

        # 檢查玩家的選擇是否在棋盤內
        if not self.in_bounds(coords):
            if self.selected:
                self.selected.fill(self.selected.color)
                self.selected = None
            return 

        # 當目前已經選擇了棋子後，移動到玩家下一個點的位置
        if self.selected and coords in self.selected.piece.valid_moves(self):
            self.make_move((self.selected.x, self.selected.y), (x, y))
            self.selected = None
            self.next_turn()
            return

        # 重新恢復棋盤的顏色
        if self.selected:
            self.selected.fill(self.selected.color)
            self.selected = None

        # 選擇某個棋子後，改變棋盤格子的顏色
        if self.piece_at_coords((x, y)) and self.tilemap[x][y].piece.color == self.turn:
            self.tilemap[x][y].select()
            self.selected = self.tilemap[x][y]
            # for move in self.selected.piece.valid_moves(self):
            #     self.tilemap[move[0]][move[1]].fill_alpha(CAN_MOVE_COLOR)
    
    ## 複製當前的棋盤狀況
    def copy(self):
        copy = Board(self.player_color)
        for x in range(8):
            for y in range(8):
                if(self.piece_at_coords((x,y))):
                    copy.tilemap[x][y].piece = self.tilemap[x][y].piece.copy()
        copy.selected = self.selected
        copy.turn = self.turn
        copy.player_color = self.player_color
        copy.gameover = self.gameover
        copy.black_num = self.balck_num
        copy.white_num = self.white_num
        copy.blackScore = self.blackScore
        copy.whiteScore = self.whiteScore

        return copy

    ## 檢查是否在棋盤內
    @staticmethod
    def in_bounds(coords) -> bool:
        if(coords[0] < 0 or coords[0] >= 8 or coords[1] < 0 or coords[1] >= 8):
            return False
        return True
        
    ## 檢查棋子的位置是否在界線內
    def piece_at_coords(self, coords) -> bool:
        if not self.in_bounds(coords) or self.tilemap[coords[0]][coords[1]].piece is None:
            return False
        return True

    ## 檢查斜對角是否為對手的棋子
    def enemy_at_coords(self, coords, color) -> bool:
        if self.piece_at_coords(coords):
            return self.tilemap[coords[0]][coords[1]].piece.color != color
    
    ## 判斷該目的地是否為合法的移動
    def valid_move(self, dest, color) -> bool:
        if self.in_bounds(dest) \
                and (not self.piece_at_coords(dest) \
                    or self.enemy_at_coords(dest, color)):
            return True
        return False


    ## 轉換目前的玩家移動權力
    def next_turn(self) -> None:
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

        self.bottomPlayerTurn = not self.bottomPlayerTurn

    ## 檢查是否吃完敵方全部棋子
    def win_eat_all(self):
        ## check whether eat all the pieces
        if self.balck_num == 0:
            if(self.player_color == BLACK):
                self.gameover = 'AI','EAT ALL'
            else:
                self.gameover = 'Player','EAT ALL'
        elif self.white_num == 0:
            if(self.player_color == BLACK):
                self.gameover = 'Player','EAT ALL'
            else:
                self.gameover = 'AI','EAT ALL'
    
    ## 檢查是否到達底線
    def meet_endline(self,dest_tile):
        ## check whether meet the end line
        if(self.bottomPlayerTurn and dest_tile.y == 0):
            self.gameover = 'Player','REACH LINE'
        
        if(not self.bottomPlayerTurn and dest_tile.y == 7):
            self.gameover = 'AI','REACH LINE'
    
    ## 根據目的地和出發地移動棋子
    def make_move(self, source, dest):
        
        source_tile = self.tilemap[source[0]][source[1]]
        dest_tile = self.tilemap[dest[0]][dest[1]]

        ## store previous state to allow unmake move
        previous_state =   {"blackScore": self.blackScore,
                            "whiteScore": self.whiteScore,
                            "tile1": (source, source_tile.copy()),
                            "tile2": (dest, dest_tile.copy()),
                            "gameover": self.gameover
                            }
        self.past_moves.append(previous_state)
        ## update scores
        if dest_tile.piece:
            if(self.turn == WHITE):
                self.blackScore -= 1
            else:
                self.whiteScore -= 1
        
        if(dest_tile.piece != None):
            if(dest_tile.piece.color != source_tile.piece.color):
                if(dest_tile.piece.color == WHITE):
                    if(self.player_color == WHITE):
                        self.whiteScore += (15 - dest_tile.piece.y)
                    else:
                        self.whiteScore += (dest_tile.piece.y + 7)
                    self.white_num -= 1
                elif(dest_tile.piece.color == BLACK):
                    if(self.player_color == BLACK):
                        self.blackScore += (15 - dest_tile.piece.y)
                    else:
                        self.blackScore += (dest_tile.piece.y + 7)
                    self.balck_num -= 1
        # print(self.balck_num, self.white_num)


        ## move piece from source to destination
        dest_tile.piece = source_tile.piece
        source_tile.piece.move(dest_tile.x, dest_tile.y)
        # dest_tile.piece.firstMove = False

        # Remove piece from source tile
        source_tile.piece = None
        source_tile.fill(source_tile.color)

        ## check win conditions
        self.win_eat_all()
        self.meet_endline(dest_tile)

    ## 回上一步
    def unmake_move(self):
        previous_state = self.past_moves.pop()
        self.blackScore = previous_state["blackScore"]
        self.whiteScore = previous_state["whiteScore"]
        x = previous_state["tile1"][0][0]
        y = previous_state["tile1"][0][1]
        self.tilemap[x][y] = previous_state["tile1"][1]
        x = previous_state["tile2"][0][0]
        y = previous_state["tile2"][0][1]
        self.tilemap[x][y] = previous_state["tile2"][1]
        self.gameover = previous_state["gameover"]

        self.next_turn()



    ## 目前玩家所有的合法移動 => 回傳list
    def get_moves(self):
        moves = []
        for x in range(8):
            for y in range(8):
                if self.piece_at_coords((x, y)) \
                    and self.tilemap[x][y].piece.color == self.turn:
                    for move in self.tilemap[x][y].piece.valid_moves(self):
                        if self.enemy_at_coords(move, self.turn):
                            moves.insert(0, ((x, y), move))
                        else:
                            moves.append(((x, y), move))
        return list(set(moves))          # converting to set then back to list has randomizing effect on moves

    ## 目前玩家所有的合法攻擊移動 => 回傳list
    def get_attacks(self):
        attacks = []
        for x in range(8):
            for y in range(8):
                if self.piece_at_coords((x, y)) \
                    and self.tilemap[x][y].piece.color == self.turn:
                    for move in self.tilemap[x][y].piece.valid_attacks(self):
                        if self.enemy_at_coords(move, self.turn):
                            attacks.insert(0, ((x, y), move))
                        else:
                            attacks.append(((x, y), move))
        return list(set(attacks))          # converting to set then back to list has randomizing effect on moves