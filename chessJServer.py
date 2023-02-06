from chessJ import main as chessJ
import socket

HOST = 'LaptopJoel'
PORT = 12321
piSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Waiting for connection with RPi...')

piSocket.bind((HOST, PORT))
piSocket.listen(5)
connection, address = piSocket.accept()

print('Connected')


def get_move():
    connection.send('get\n'.encode('utf-8'))
    res = connection.recv(1024).decode('utf-8')
    fx, fy, tx, ty = res.split(' ')
    fx, fy, tx, ty = int(fx), int(fy), int(tx), int(ty)
    return fx, fy, tx, ty


def move_callback(fromx, fromy, tox, toy, capture):
    msg = f'{"capture" if capture else "move"} {fromx} {fromy} {tox} {toy}\n'.encode(
        'utf-8')
    connection.send(msg)
    connection.recv(1024)


chessJ(get_move, move_callback)

connection.send('q'.encode('utf-8'))

connection.close()
