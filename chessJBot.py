from chessJGantry import createGantry
from serial import Serial
import socket


HOST = 'LaptopJoel'
PORT = 12321
pcSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pcSocket.connect((HOST, PORT))
print("Connected to PC")


def get_move():
    arduinoSerial.reset_input_buffer()
    print("Reading moves")
    fx = fy = tx = ty = 0
    val = 1
    while val == 1:
        data = arduinoSerial.readline().decode('utf-8')
        print("From", data)
        fy, fx, val = data.split(' ')
        fx, fy, val = int(fx), int(fy), int(val)
    while val == 0:
        data = arduinoSerial.readline().decode('utf-8')
        print("To", data)
        ty, tx, val = data.split(' ')
        tx, ty, val = int(tx), int(ty), int(val)
    return fx, fy, tx, ty


def move_callback(fromx, fromy, tox, toy, capture):
    print(
        f"Moving piece from {fromy} {fromx} to {toy} {tox}{' while capturing' if capture else ''}")
    if capture:
        gantry.removePiece(tox, toy)
    gantry.movePiece(fromx, fromy, tox, toy)


arduinoSerial = Serial('/dev/ttyUSB0', 9600, timeout=1)
arduinoSerial.reset_input_buffer()
gantry = createGantry()
print("Connected to Arduino")

while True:
    cmd = pcSocket.recv(1024).decode('utf-8')
    print(f'Received command "{cmd}"')
    if cmd == 'q':
        break
    parts = [p.strip() for p in cmd.split(' ')]
    if parts[0] == 'get':
        fx, fy, tx, ty = get_move()
        res = f'{fx} {fy} {tx} {ty}\n'.encode('utf-8')
        pcSocket.send(res)
    elif parts[0] == 'move' or parts[0] == 'capture':
        move_callback(int(parts[1]), int(parts[2]),
                      int(parts[3]), int(parts[4]), parts[0] == 'capture')
        pcSocket.send('\n'.encode('utf-8'))
