print("""
                                                                                                                        
                                                                                                                        
       ............************                                                                                         
       ............************                                                                                         
       ............************           ******,     **     **    **********    *******     *******       .......      
       ............************         ***     **    **     **    **           **     **   **     **           ..      
       ............************         **.           **     **    **           **          **                  ..      
      ************............          **.           *********    *********     *******     *******            ..      
      ************............          **.           **     **    **                  **          **           ..      
      ************............           **    ***    **     **    **           **     **   **     **   ...    ...      
      ************............            ******      **     **    **********    *******     *******      ......        
      ************                                                                                                      
                                                                                                                        
                                                                                                                        
""")

from math import lcm
from re import L
from typing import Iterable, List
from chessJModel import create_model
from chessJUtil import select_folder

board_size = 8

moves_conv_tbl = {(fromx * board_size**3 + fromy *
                  board_size**2 + tox * board_size + toy):
                  (fromx, fromy, tox, toy) for fromx in range(
    board_size) for fromy in range(board_size)
    for tox in range(board_size)
    for toy in range(board_size)}


def get_pieces_conv_tbl_list(i: int):
    conv_tbl_list = [0] * (pieces_types_num * 2 + 1)
    conv_tbl_list[i] = 1
    return conv_tbl_list


pieces_types_num = 6

pieces_conv_tbl = [get_pieces_conv_tbl_list(
    i) for i in range(pieces_types_num * 2 + 1)]


def argmax(x: Iterable):
    return max(range(len(x)), key=lambda i: x[i])


def path_valid(board: List[List[int]], fromx: int, fromy: int, tox: int, toy: int):
    if fromx == tox and fromy == toy:
        return False
    dy = toy - fromy
    dx = tox - fromx
    if dy and dx:
        step = lcm(abs(dx), abs(dy))
    else:
        step = max(abs(dx), abs(dy))
    stepx = dx // step
    stepy = dy // step
    fromy += stepy
    fromx += stepx
    while fromy != toy or fromx != tox:
        if board[fromy][fromx]:
            return False
        fromy += stepy
        fromx += stepx
    return True


def get_piece_moves(board: List[List[int]], x: int, y: int, piece: int = None):
    if piece is None:
        piece = board[y][x]
    match piece:
        case 0:
            return (), ()
        case 1:  # * white pawn
            if y == 6:
                return ((x, y - 2), (x, y - 1)), ((x - 1, y - 1), (x + 1, y - 1))
            else:
                return ((x, y - 1)), ((x - 1, y - 1), (x + 1, y - 1))
        case 7:  # * black pawn
            if y == 1:
                return ((x, y + 2), (x, y + 1)), ((x - 1, y + 1), (x + 1, y + 1))
            else:
                return ((x, y + 1)), ((x - 1, y + 1), (x + 1, y + 1))
        case 2 | 8:  # * rook
            return (tuple((x, i) for i in range(board_size))
                    + tuple((i, y) for i in range(board_size)),) * 2
        case 3 | 9:  # * knight
            return (((x + 1, y + 2), (x - 1, y + 2), (x + 1, y - 2), (x - 1, y - 2),
                     (x + 2, y + 1), (x - 2, y + 1), (x + 2, y - 1), (x - 2, y - 1)),) * 2
        case 4 | 10:  # * bishop
            return (tuple((x + i, y + i) for i in range(-board_size, board_size)
                          if 0 <= x + i < board_size and 0 <= y + i < board_size)
                    + tuple((x + i, y - i) for i in range(-board_size, board_size)
                            if 0 <= x + i < board_size and 0 <= y - i < board_size),) * 2
        case 5 | 11:  # * queen
            rook_m, rook_c = get_piece_moves(board, x, y, 2)
            bsp_m, bsp_c = get_piece_moves(board, x, y, 4)
            return rook_m + bsp_m, rook_c + bsp_c
        case 6 | 12:  # * king
            return (tuple(e for e in (
                (x, y), (x, y + 1), (x, y - 1), (x + 1, y), (x + 1, y + 1),
                (x + 1, y - 1), (x - 1, y), (x - 1, y + 1), (x - 1, y - 1)
            ) if 0 <= e[0] < board_size and 0 <= e[1] < board_size),) * 2


def is_valid_move(board: List[List[int]], fromx: int, fromy: int, tox: int, toy: int):
    cell = board[fromy][fromx]
    moves_n, moves_c = get_piece_moves(board, fromx, fromy)
    if board[toy][tox] == 0:
        can_move_cell = (tox, toy) in moves_n
        can_move_dest = True
    else:
        can_move_cell = (tox, toy) in moves_c
        can_move_dest = board[toy][tox] <= 6 if cell >= 7 else board[toy][tox] >= 7
    return can_move_dest and can_move_cell and (
        cell == 3 or cell == 9 or path_valid(board, fromx, fromy, tox, toy))


def convert_board(board: List[List[int]]):
    return [[[pieces_conv_tbl[e] for e in row] for row in board]]


def color_text(str, color) -> str:
    return f'\x1b[38;5;{color}m{str}\x1b[0;0m'


import os
os.system("")


# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
def get_piece_repr(piece_num: int):
    return color_text({
        0: ' ',
        1: '♟︎',
        2: '♜',
        3: '♞',
        4: '♝',
        5: '♛',
        6: '♚',
        7: '♙',
        8: '♖',
        9: '♘',
        10: '♗',
        11: '♕',
        12: '♔',
    }[piece_num], 255 if piece_num < 7 else 59)


def print_board(board: List[List[int]]) -> None:
    print()
    print('    a   b   c   d   e   f   g   h  ')
    print('  ---------------------------------')
    for i, row in enumerate(board):
        print(f'{i+1} |', end='')
        for cell in row:
            print(f' {get_piece_repr(cell)} ', end='|')
        print(f' {i+1}\n  ---------------------------------')
    print('    a   b   c   d   e   f   g   h  ')
    print()


def get_ai_move(board: List[List[int]], model, ai_is_black):
    predictions: list = model.predict(convert_board(board)).tolist()[0]
    while True:
        position = argmax(predictions)
        fromx, fromy, tox, toy = moves_conv_tbl[position]
        if is_valid_move(board, fromx, fromy, tox, toy):
            if (board[fromy][fromx] < 7) ^ ai_is_black:
                return fromx, fromy, tox, toy
        predictions[position] = -100


def get_player_move(board: List[List[int]]):
    while True:
        inp = input('next move > ')
        if inp.find('exit') >= 0 or inp.find('x') >= 0:
            return None, None, None, None
        if inp.find('quit') >= 0 or inp.find('q') >= 0:
            return None, None, None, None
        if len(inp) == 4:
            try:
                fromx, fromy, tox, toy = inp
                fromx, fromy, tox, toy = ord(
                    fromx) - 97, int(fromy) - 1, ord(tox) - 97, int(toy) - 1
                if (0 <= fromx < board_size and 0 <= fromy < board_size
                        and 0 <= tox < board_size and 0 <= toy < board_size):
                    if is_valid_move(board, fromx, fromy, tox, toy):
                        return fromx, fromy, tox, toy
                    else:
                        print(color_text(
                            f'Invalid input: ({fromx},{fromy}-{tox},{toy}) is not a valid move', 160))
                else:
                    print(color_text(
                        f'Invalid input: position ({fromx},{fromy}-{tox},{toy}) not on the board', 160))
            except ValueError:
                print(color_text('Invalid input: input has the wrong size', 160))
                print('Format moves as a1a2')


def main():
    print('Starting the AI...')
    board = [
        [8, 9, 10, 11, 12, 10, 9, 8],
        [7, 7, 7, 7, 7, 7, 7, 7],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [2, 3, 4, 5, 6, 4, 3, 2]
    ]
    model = create_model()
    model_load_folder = select_folder('model')
    model.load_weights(f'{model_load_folder}/cp.ckpt')
    ai_is_black = bool(input("Type anything if the AI plays as black: "))
    print('The AI is playing as', 'black' if ai_is_black else 'white')
    print_board(board)
    if ai_is_black:
        # Player
        fromx, fromy, tox, toy = get_player_move(board)
        if fromx is None:
            return
        board[toy][tox] = board[fromy][fromx]
        board[fromy][fromx] = 0
        print_board(board)
    while True:
        # AI
        fromx, fromy, tox, toy = get_ai_move(board, model, ai_is_black)
        board[toy][tox] = board[fromy][fromx]
        board[fromy][fromx] = 0
        print_board(board)
        # Player
        fromx, fromy, tox, toy = get_player_move(board)
        if fromx is None:
            return
        board[toy][tox] = board[fromy][fromx]
        board[fromy][fromx] = 0
        print_board(board)


if __name__ == '__main__':
    main()