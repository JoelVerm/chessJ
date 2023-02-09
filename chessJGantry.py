import threading
from time import sleep
from gpiozero import Servo
from RpiMotorLib import RpiMotorLib


class Stepper:
    def __init__(self, pin1, pin2, pin3, pin4):
        self.motor = RpiMotorLib.BYJMotor("Motor1", "Nema")
        self.pins = [pin1, pin2, pin3, pin4]
        self.running = False
        self.thread = None

    def stop(self):
        if self.running and self.thread:
            self.motor.motor_stop()
            self.thread.join()

    def move(self, points: int, speed: int):
        if self.running:
            self.stop()
        if points == 0:
            return

        self.running = True
        self.thread = threading.Thread(
            target=self.moveSync, args=(points, speed))
        self.thread.daemon = True
        self.thread.start()

    def moveSync(self, points: int, speed: int):
        delay = 1 / speed
        self.motor.motor_run(self.pins, delay, abs(points), points < 0)
        self.running = False


class Gantry:
    def __init__(self, stepper1: Stepper, stepper2: Stepper, rangeX: int, rangeY: int, speed=1000):
        self.stepper1 = stepper1
        self.stepper2 = stepper2
        self.rangeX = rangeX
        self.rangeY = rangeY
        self.speed = speed
        self.posX = 0
        self.posY = 0

    def move(self, percentX: int, percentY: int):
        pointsX = self.rangeX * (percentX / 100)
        pointsY = self.rangeY * (percentY / 100)
        moveX = pointsX - self.posX
        moveY = pointsY - self.posY
        move1 = moveX * 0.5 + moveY * 0.5
        move2 = moveX * 0.5 + moveY * -0.5
        self.stepper1.move(move1, self.speed)
        self.stepper2.move(move2, self.speed)
        while self.stepper1.running or self.stepper2.running:
            sleep(0.05)
        self.posX += moveX
        self.posY += moveY


class ChessBoardGantry:
    def __init__(self, gantry: Gantry, magnet: Servo, removeX: float, removeY: float):
        self.gantry = gantry
        self.magnet = magnet
        self.magnet.value = -1
        self.removeX = removeX
        self.removeY = removeY

    def toPercentage(self, cell: int):
        return (100 // 16) + cell * (100 // 8)

    def moveToCell(self, cellX: int, cellY: int):
        percentX = self.toPercentage(cellX)
        percentY = self.toPercentage(cellY)
        self.gantry.move(percentX, percentY)

    def movePiece(self, fromx, fromy, tox, toy):
        self.moveToCell(fromx, fromy)
        self.magnet.value = 1
        dx = tox - fromx
        dy = toy - fromy
        if dx and dy:
            if abs(dx) == abs(dy):
                self.moveToCell(tox, toy)
            elif dx == 1 or dx == -1:
                halfStep = 0.5 if dx > 0 else -0.5
                self.moveToCell(fromx + halfStep, fromy)
                self.moveToCell(fromx + halfStep, toy)
                self.moveToCell(tox, toy)
            elif dy == 1 or dy == -1:
                halfStep = 0.5 if dy > 0 else -0.5
                self.moveToCell(fromx, fromy + halfStep)
                self.moveToCell(tox, fromy + halfStep)
                self.moveToCell(tox, toy)
        else:
            self.moveToCell(tox, toy)
        self.magnet.value = -1

    def removePiece(self, x, y):
        self.movePiece(x, y, self.removeX, self.removeY)


def createGantry():
    return ChessBoardGantry(
        Gantry(
            Stepper(6, 13, 19, 26),
            Stepper(24, 23, 3, 2),
            950, 900, 700
        ),
        Servo(25),
        -0.5, 2
    )
