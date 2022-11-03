import csv
import io
import chess
import chess.pgn
import json


def progress(str, i, end):
    barLen = 30
    print(
        f'{str} {i}/{end}\t[{"="*(i*barLen//end)}>{" "*(barLen-i*barLen//end)}]', end='\r')


class PrintMovesVisitor(chess.pgn.BaseVisitor):
    def __init__(self):
        self.coords = []
        self.chars = 'abcdefgh'

    def visit_move(self, board, move):
        m = chess.Move.uci(move)
        self.coords.append((self.chars.find(m[0]), int(
            m[1])-1, self.chars.find(m[2]), int(m[3])-1))

    def result(self):
        return self.coords


moves = []

with open('200k_blitz_rapid_classical_bullet.csv', newline='') as csvFile:
    reader = csv.reader(csvFile)
    for i, row in enumerate(reader):
        if i == 0:
            continue
        progress('Reading game', i, 200000)
        pgn = io.StringIO(' '.join(row[21:221]))
        coords = chess.pgn.read_game(pgn, Visitor=PrintMovesVisitor)
        moves.append((row[9], coords))
    print()
del moves[0]

print(moves[0])

with open('moves.json', 'w') as f:
    json.dump(moves, f)
