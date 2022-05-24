## 參考程式：https://github.com/aiatuci/ChessAI/blob/main/chess.py
import pygame_menu
import pygame
import queue
import threading
from board import Board
from screen import *
import AI
from math import inf

## Initialize pygame
pygame.init()

# Fonts
FONT = pygame.font.Font(pygame_menu.font.FONT_OPEN_SANS_BOLD, 18)
BIG_FONT = pygame.font.Font(pygame_menu.font.FONT_OPEN_SANS_BOLD, 26)

class Game:

    ## 設定初始值，遊戲黑棋先下
    def __init__(self):
        self.p1_name = "Palyer"
        self.p2_name = "alpha-beta AI"
        
        self.p1_color = BLACK
        self.p2_color = WHITE

        self.board = Board(self.p1_color)
        self.board.initialize_piece()

        self.ai_move = queue.Queue()
        self.lock = threading.Lock()
        self.menu_screen()

    ## 顯示遊戲畫面以及控制遊戲流程主要運作
    def game_screen(self):
        ## 決定AI的move
        t = threading.Thread(target=self.determine_move)

        ## display the screen
        while True:
            for event in pygame.event.get():
                # Pygame window was closed
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # Check if any buttons were pressed or pieces were selected
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.board.select()
                    self.board.draw()
                    pygame.display.flip()

            SCREEN.fill(BG_COLOR)
            self.draw_names()
            
            ## 判斷結束條件
            if(self.board.gameover):
                print("GAME OVER: ",self.board.gameover[0])
                return self.end_screen(self.board.gameover[0],self.board.gameover[1])
            
            ## 控制AI移動
            self.lock.acquire()
            if(self.board.turn == self.p2_color and not self.board.gameover \
                and self.ai_move.qsize() == 0):
                t = threading.Thread(target=self.determine_move)
                t.start()
            self.lock.release()
            if(self.board.turn == self.p2_color \
                and self.ai_move.qsize() > 0 \
                    and not self.board.gameover):
                    move = self.ai_move.get()
                    print(move[0],move[1])
                    self.board.make_move(move[0],move[1])
                    self.board.next_turn()
            
            # Update display
            self.board.draw()
            pygame.display.flip()

    ## AI 決定如何移動
    def determine_move(self):
        if(self.p2_name == "alpha-beta AI"):
            self.ai_move.put(AI.alpha_beta_minmax(self.board.copy(), 3, inf, -inf, True, self.p2_color)[0])
        else:
            self.ai_move.put(AI.random_move(self.board))
    
    ## 在螢幕上顯示名字
    def draw_names(self):
        pygame.draw.rect(SCREEN, BG_COLOR_LIGHT, [BOARD_X, BOARD_Y - 36, TILE_SIZE * 2, 28])
        p1name = FONT.render(self.p2_name, True, SMALL_TEXT_COLOR)
        SCREEN.blit(p1name, (BOARD_X + 4, BOARD_Y - 34))
        # Draw bottom name (player 1)
        pygame.draw.rect(SCREEN, BG_COLOR_LIGHT, [BOARD_X, BOARD_Y + BOARD_SIZE + 8, TILE_SIZE * 2, 28])
        p2name = FONT.render(self.p1_name, True, SMALL_TEXT_COLOR)
        SCREEN.blit(p2name, (BOARD_X + 4, BOARD_Y + BOARD_SIZE + 10))
    
    ## 重新開始的初始設定
    def reset(self):
        self.p2_name = "alpha-beta AI"
        self.p1_color = BLACK
        self.p2_color = WHITE
        self.board = Board(self.p1_color)
        self.board.initialize_piece()
        self.ai_move = queue.Queue()

    ## 根據玩家選項設定AI
    def set_ai(self,tup,ai_name):
        self.p2_name = ai_name

    ## 根據玩家輸入的名字設定玩家名字
    def set_name(self,name):
        self.p1_name = name

    ## 根據玩家選擇設定玩家與AI的顏色
    def set_color(self, color ,value):
        self.board.player = value
        self.p1_color = value
        if(value == WHITE):
            self.p2_color = BLACK
            self.board.bottomPlayerTurn = False
        else:
            self.p2_color = WHITE
            self.board.bottomPlayerTurn = True
        self.board = Board(value)
        self.board.initialize_piece()
    
    ## 繪製結束畫面
    def end_screen(self, winner, condition):
        # Create background for end screen
        bg = pygame.Rect(int(BOARD_X + TILE_SIZE * 2.5), int(BOARD_Y + TILE_SIZE * 2.5), TILE_SIZE * 3, TILE_SIZE * 2)
        # Creates collision boxes for rematch and leave buttons
        rematch_button = pygame.Rect(bg.left, bg.bottom - 28, bg.centerx - bg.left - 2, 28)
        leave_button = pygame.Rect(bg.centerx + 2, bg.bottom - 28, bg.centerx - bg.left - 2, 28)

        # Creates fade transitional effect for end screen
        def fade(width, height):
            f = pygame.Surface((width, height))
            f.fill(BG_COLOR)
            for alpha in range(0, 175):
                f.set_alpha(alpha)
                self.board.draw()
                SCREEN.blit(f, (0, 0))
                pygame.display.update()
                pygame.time.delay(1)

        # Controls fade effect
        fading = True

        # End screen loop
        while True:
            for event in pygame.event.get():
                # Pygame window was closed
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # Check if any buttons were pressed
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    # Rematch button was pressed
                    if rematch_button.collidepoint(mouse_pos):
                        self.reset()
                        return self.game_screen()

                    # Leave button was pressed
                    if leave_button.collidepoint(mouse_pos):
                        self.reset()
                        return self.menu_screen()

            # Apply fade effect
            if fading:
                fade(SCREEN_WIDTH, SCREEN_HEIGHT)
                fading = False

            # Draw UI elements
            self.draw_end_message(condition, winner)

            # Update display
            pygame.display.flip()
    

    ## 繪製結束的提示訊息
    @staticmethod
    def draw_end_message(condition, winner):
        # Draw 'Game Over' text
        bg = pygame.draw.rect(SCREEN, BG_COLOR_LIGHT,
                              [int(BOARD_X + TILE_SIZE * 2.5), int(BOARD_Y + TILE_SIZE * 2.5), TILE_SIZE * 3,
                               TILE_SIZE * 2])
        pygame.draw.rect(SCREEN, BLACK,
                         [int(BOARD_X + TILE_SIZE * 2.5), int(BOARD_Y + TILE_SIZE * 2.5), TILE_SIZE * 3, TILE_SIZE * 2],
                         1)
        txt = BIG_FONT.render("Game Over", True, LARGE_TEXT_COLOR)
        SCREEN.blit(txt, (BOARD_X + TILE_SIZE * 3 - 8, int(BOARD_Y + TILE_SIZE * 2.5 + 4)))

        # Draw win condition and winner (if applicable)
        if winner:
            txt = FONT.render(winner + " win", True, SMALL_TEXT_COLOR)
            SCREEN.blit(txt, (BOARD_X + TILE_SIZE * 3, BOARD_Y + TILE_SIZE * 3 + 4))
            txt = FONT.render(f"by {condition}", True, SMALL_TEXT_COLOR)
            SCREEN.blit(txt, (BOARD_X + TILE_SIZE * 3, int(BOARD_Y + TILE_SIZE * 3.4)))
        else:
            txt = FONT.render(f"{condition}", True, SMALL_TEXT_COLOR)
            SCREEN.blit(txt, (int(BOARD_X + TILE_SIZE * 3.2), int(BOARD_Y + TILE_SIZE * 3.3)))

        # Draw Rematch button
        pygame.draw.rect(SCREEN, BLACK, [bg.left, bg.bottom - 28, bg.centerx - bg.left + 3, 28], 1)
        txt = FONT.render("Rematch", True, SMALL_TEXT_COLOR)
        SCREEN.blit(txt, (bg.left + 8, bg.bottom - 28 + 2))

        # Draw Leave button
        pygame.draw.rect(SCREEN, BLACK, [bg.centerx + 2, bg.bottom - 28, bg.centerx - bg.left - 2, 28], 1)
        txt = FONT.render("Leave", True, SMALL_TEXT_COLOR)
        SCREEN.blit(txt, (bg.centerx + 20, bg.bottom - 28 + 2))
    
    ## 繪製首頁
    def menu_screen(self):
        menu = pygame_menu.Menu('Welcome QQ Breakthrough Game', SCREEN_WIDTH, SCREEN_HEIGHT,
                       theme=pygame_menu.themes.THEME_DEFAULT)

        menu.add.text_input('Name :', default=self.p1_name, maxchar = 10,onchange=self.set_name)
        menu.add.selector('AI:', [('alpha-beta-minmax', "alpha-beta AI"), ('random', "Random AI")], onchange=self.set_ai)
        menu.add.selector('Color:', [('Black', BLACK), ('White', WHITE)], onchange=self.set_color)
        menu.add.button('Play', self.game_screen)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            menu.mainloop(SCREEN)
            pygame.display.flip()

if __name__ == "__main__":
    Game()
    