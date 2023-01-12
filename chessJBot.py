from chessJ import main as chessJ
from chessJGantry import createGantry


def get_move():
    pass


def move_callback(fromx, fromy, tox, toy):
    gantry.movePiece(fromx, fromy, tox, toy)


gantry = createGantry()
chessJ(get_move, move_callback)
