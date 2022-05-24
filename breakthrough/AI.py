import random
from math import inf
from piece import *

def random_move(board):
    moves = board.get_moves()
    if moves:
        return random.choice(moves)

def evaluate(board, max_agent):
    if(max_agent == WHITE):
        score = board.whiteScore - board.blackScore
        print(score)
        return board.whiteScore - board.blackScore
    else:
        score = board.blackScore - board.whiteScore
        print(score)
        return board.blackScore - board.whiteScore

def alpha_beta_minmax(board, depth, alpha, beta, min_agent, max_agent):
    if depth == 0 or board.gameover:
        return None, evaluate(board, max_agent)
    board.bottomPlayerTurn = False
    moves = board.get_moves()
    attacks = board.get_attacks()
    if(attacks):
        best_move = random.choice(attacks)
    best_move = random.choice(moves)
    
    if min_agent:
        max_eval = -inf
        if attacks:
            for attack in attacks:
                if attack[1][1] == 6:   ## 如果下一步就贏，走
                    best_move = attack
                    return best_move, 1000
                board.make_move(attack[0],attack[1])
                current_eval = alpha_beta_minmax(board,depth-1,alpha,beta,False,max_agent)[1]
                board.unmake_move()
                if current_eval > max_eval:
                    max_eval = current_eval
                    best_move = attack

                # alpha beta prune
                alpha = max(alpha, current_eval)
                if beta <= alpha:
                    break
        else:     
            for move in moves:
                if move[1][1] == 6:   ## 如果下一步就贏，走
                    best_move = move
                    return best_move, 1000
                board.make_move(move[0],move[1])
                current_eval = alpha_beta_minmax(board,depth-1,alpha,beta,False,max_agent)[1]
                board.unmake_move()
                if current_eval > max_eval:
                    max_eval = current_eval
                    best_move = move

                # alpha beta prune
                alpha = max(alpha, current_eval)
                if beta <= alpha:
                    break
        board.bottomPlayerTurn = True
        return best_move, max_eval
    else:
        min_eval = inf
        if attacks:
            for attack in attacks:
                if attack[1][1] == 6:    ## 如果下一步就贏，走
                    best_move = attack
                    return best_move, -1000
                board.make_move(attack[0], attack[1])
                current_eval = alpha_beta_minmax(board, depth-1, alpha, beta, True, max_agent)[1]
                board.unmake_move()
    
                if current_eval < min_eval:
                    min_eval = current_eval
                    best_move = attack

                # alpha beta prune
                beta = min(beta, current_eval)
                if beta <= alpha:
                    break
        else:
            for move in moves:
                if move[1][1] == 6:     ## 如果下一步就贏，走
                    best_move = move
                    return best_move, -1000
                board.make_move(move[0], move[1])
                current_eval = alpha_beta_minmax(board, depth-1, alpha, beta, True, max_agent)[1]
                board.unmake_move()
    
                if current_eval < min_eval:
                    min_eval = current_eval
                    best_move = move
    
                # alpha beta prune
                beta = min(beta, current_eval)
                if beta <= alpha:
                    break
        board.bottomPlayerTurn = True
        return best_move, min_eval