from chessJGantry import createGantry
from serial import Serial
import socket


HOST = 'joelv@laptopjoel'
PORT = 12321
pcSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pcSocket.connect((HOST, PORT))


def get_move():
    fx = fy = tx = ty = 0
    val = 1
    while val == 1:
        fy, fx, val = arduinoSerial.readline().decode('utf-8').split(' ')
        fx, fy, val = int(fx), int(fy), int(val)
    while val == 0:
        ty, tx, val = arduinoSerial.readline().decode('utf-8').split(' ')
        tx, ty, val = int(tx), int(ty), int(val)
    return fx, fy, tx, ty


def move_callback(fromx, fromy, tox, toy):
    gantry.movePiece(fromx, fromy, tox, toy)


arduinoSerial = Serial('/dev/ttyACM0', 9600, timeout=1)
arduinoSerial.reset_input_buffer()
gantry = createGantry()

while True:
    cmd = pcSocket.recv(1024).decode('utf-8')
    if cmd == 'q':
        break
    parts = cmd.split(' ')
    if parts[0] == 'get':
        fx, fy, tx, ty = get_move()
        res = f'{fx} {fy} {tx} {ty}\n'.encode('utf-8')
        pcSocket.send(res)
    elif parts[0] == 'do':
        move_callback(int(parts[1]), int(parts[2]),
                      int(parts[3]), int(parts[4]))
        pcSocket.send('\n')
