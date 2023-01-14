from chessJ import main as chessJ
from serial import Serial


def get_move():
    piSerial.write('get\n'.encode('utf-8'))
    res = piSerial.readline().decode('utf-8')
    fx, fy, tx, ty = res.split(' ')
    fx, fy, tx, ty = int(fx), int(fy), int(tx), int(ty)
    return fx, fy, tx, ty


def move_callback(fromx, fromy, tox, toy):
    msg = f'do {fromx} {fromy} {tox} {toy}\n'.encode('utf-8')
    piSerial.write(msg)
    piSerial.readline()


piSerial = Serial('/dev/ttyACM0', 9600, timeout=1)
piSerial.reset_input_buffer()
chessJ(get_move, move_callback)
