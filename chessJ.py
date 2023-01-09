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
from typing import Iterable, List
from chessJModel import create_model
from chessJUtil import input_int, select_folder, iter_path

board_size = 8

moves_conv_tbl = {(fromx * board_size**3
                   + fromy * board_size**2
                   + tox * board_size + toy):
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


def path_valid_old(board: List[List[int]], fromx: int, fromy: int, tox: int, toy: int):
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
    while (fromy != toy or fromx != tox):
        if not (fromy >= 0 and fromx >= 0 and fromy < board_size and fromx < board_size):
            return False
        if board[fromy][fromx]:
            return False
        fromy += stepy
        fromx += stepx
    return True


def path_valid(board: List[List[int]], fromx: int, fromy: int, tox: int, toy: int):
    for x, y in iter_path(fromx, fromy, tox, toy):
        if not (y >= 0 and x >= 0 and y < board_size and x < board_size):
            return False
        if board[y][x]:
            return False
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
                return ((x, y - 1),), ((x - 1, y - 1), (x + 1, y - 1))
        case 7:  # * black pawn
            if y == 1:
                return ((x, y + 2), (x, y + 1)), ((x - 1, y + 1), (x + 1, y + 1))
            else:
                return ((x, y + 1),), ((x - 1, y + 1), (x + 1, y + 1))
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


def find_2d_list(l2d, item):
    for y, l1d in enumerate(l2d):
        for x, i in enumerate(l1d):
            if i == item:
                return y, x
    return -1, -1


def get_king_dangers(board: List[List[int]], kingX: int, kingY: int):
    dangers = []
    for p in range(1, 17):
        moves_n, moves_c = get_piece_moves(board, kingX, kingY, p)
        for mx, my in moves_c:
            ax, ay = mx + kingX, my + kingY
            if 0 <= ax < board_size and 0 <= ay < board_size:
                if board[ay][ax] == p:
                    dangers.append([p, ax, ay])
    return dangers


def move_keeps_king_safe(board: List[List[int]], king_value: int, cell: int, fromx: int, fromy: int, tox: int, toy: int) -> bool:
    ky, kx = find_2d_list(board, king_value)
    dangers = get_king_dangers(board, kx, ky)
    if not dangers:
        return True
    if cell != king_value:
        for piece, ax, ay in dangers:
            for x, y in iter_path(kx, ky, ax, ay):
                if tox == x and toy == y:
                    break
                else:
                    return False
        return True
    else:
        new_dangers = get_king_dangers(board, tox, toy)
        return len(new_dangers) == 0


def is_valid_move(board: List[List[int]], fromx: int, fromy: int, tox: int, toy: int):
    cell = board[fromy][fromx]
    moves_n, moves_c = get_piece_moves(board, fromx, fromy)
    if board[toy][tox] == 0:
        can_move_cell = (tox, toy) in moves_n
        can_move_dest = True
    else:
        can_move_cell = (tox, toy) in moves_c
        can_move_dest = board[toy][tox] <= 6 if cell >= 7 else board[toy][tox] >= 7
    can_move_path = cell == 3 or cell == 9 or path_valid(
        board, fromx, fromy, tox, toy)
    king_saved = move_keeps_king_safe(
        board, 6 if cell < 7 else 12, cell, fromx, fromy, tox, toy)
    return can_move_dest and can_move_cell and can_move_path and king_saved


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
        print(f'{8 - i} |', end='')
        for cell in row:
            print(f' {get_piece_repr(cell)} ', end='|')
        print(f' {8 - i}\n  ---------------------------------')
    print('    a   b   c   d   e   f   g   h  ')
    print()


def move_to_str(fromx, fromy, tox, toy):
    return f'{chr(fromx + 97)}{8 - fromy}{chr(tox + 97)}{8 - toy}'


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
        if len(inp) != 4:
            print(color_text('Invalid input: input has the wrong size', 160))
            print('Format moves as a1a2')
            continue
        try:
            fromx, fromy, tox, toy = inp
            fromx, fromy, tox, toy = ord(
                fromx) - 97, 8 - int(fromy), ord(tox) - 97, 8 - int(toy)
            if not (0 <= fromx < board_size and 0 <= fromy < board_size
                    and 0 <= tox < board_size and 0 <= toy < board_size):
                print(color_text(
                    f'Invalid input: position {move_to_str(fromx, fromy, tox, toy)} is not on the board', 160))
                continue
            if not is_valid_move(board, fromx, fromy, tox, toy):
                print(color_text(
                    f'Invalid input: {move_to_str(fromx, fromy, tox, toy)} is not a valid move', 160))
                continue
            else:
                return fromx, fromy, tox, toy
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
    create_advanced = input_int(
        'choose the level of the model to run (0-1): ')
    model = create_model(create_advanced == 1)
    model_load_folder = select_folder(
        'model/cache/' + ('advanced' if create_advanced == 1 else 'simple'))
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
        print(f'the AI chose the move {move_to_str(fromx, fromy, tox, toy)}')
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
