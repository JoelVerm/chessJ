from chessJ import main as chessJ
from chessJGantry import createGantry
from serial import Serial


def get_move():
    fx = fy = tx = ty = 0
    val = 1
    while val == 1:
        fy, fx, val = serial.readline().decode('utf-8').split(' ')
        fx, fy, val = int(fx), int(fy), int(val)
    while val == 0:
        ty, tx, val = serial.readline().decode('utf-8').split(' ')
        tx, ty, val = int(tx), int(ty), int(val)
    return fx, fy, tx, ty


def move_callback(fromx, fromy, tox, toy):
    gantry.movePiece(fromx, fromy, tox, toy)


serial = Serial('/dev/ttyACM0', 9600, timeout=1)
serial.reset_input_buffer()
gantry = createGantry()
chessJ(get_move, move_callback)
