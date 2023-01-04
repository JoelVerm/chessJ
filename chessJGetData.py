import json
import random


def progress(str, i, end):
    barLen = 30
    print(
        f'{str} {i}/{end}\t[{"="*(i*barLen//end)}>{" "*(barLen-i*barLen//end)}]', end='\r')


print('Getting data...')
print('Loading json...')

with open('moves.json', 'r') as f:
    json_moves = json.load(f)

print('Creating conv_tables...')

board_size = 8

moves_conv_tbl = {(fromx, fromy, tox, toy): (fromx * board_size**3 + fromy *
                  board_size**2 + tox * board_size + toy) for fromx in range(
    board_size) for fromy in range(board_size) for tox in range(board_size) for toy in range(board_size)}

pieces_types_num = 6


def get_pieces_conv_tbl_list(i):
    conv_tbl_list = [0] * (pieces_types_num * 2 + 1)
    conv_tbl_list[i] = 1
    return conv_tbl_list


pieces_conv_tbl = [get_pieces_conv_tbl_list(
    i) for i in range(pieces_types_num * 2 + 1)]


def get_boards_moves(winner_index, moves):
    _boards = []
    _moves = []
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
    for row in board:
        for i, cell in enumerate(row):
            row[i] = pieces_conv_tbl[cell]
    for i, m in enumerate(moves):
        if i % 2 == winner_index:
            _boards.append(board)
            _moves.append(moves_conv_tbl[tuple(m)])
        board[m[2]][m[3]] = board[m[0]][m[1]]
        board[m[0]][m[1]] = pieces_conv_tbl[0]
    return _boards, _moves


def get_train_data(train_len=None, test_len=None):
    temp = []
    for i, round in enumerate(json_moves):
        progress('Creating data', i, len(json_moves))
        winner = round[0]
        moves = round[1]
        if winner == '1-0' or winner == '1/2-1/2':
            temp.append(get_boards_moves(0, moves))
        if winner == '0-1' or winner == '1/2-1/2':
            temp.append(get_boards_moves(1, moves))

    print('\nSampling data...')
    if (train_len is not None) and (test_len is not None):
        train = random.sample(temp, train_len)
        test = random.sample(temp, test_len)
    else:
        train = temp
        test = random.sample(temp, len(temp) / 10)
    print('Converting data...')
    train_boards = []
    train_moves = []
    for b, m in train:
        train_boards.extend(b)
        train_moves.extend(m)
    test_boards = []
    test_moves = []
    for b, m in test:
        test_boards.extend(b)
        test_moves.extend(m)

    return train_boards, train_moves, test_boards, test_moves
