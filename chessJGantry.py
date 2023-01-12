import threading
from time import sleep
from gpiozero import OutputDevice, Button


class Stepper:
    def __init__(self, pin1: int, pin2: int, pin3: int, pin4: int):
        self.motorPins = [
            OutputDevice(pin1),
            OutputDevice(pin2),
            OutputDevice(pin3),
            OutputDevice(pin4)
        ]
        self.sequence = [
            [1, 0, 0, 1],
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1]
        ]
        self.step = 0
        self.steps = len(self.sequence)
        self.pointsDone = 0
        self.running = False
        self.mustRun = False
        self.thread = None

    def stop(self):
        if self.running and self.thread:
            self.mustRun = False
            self.thread.join()
        return self.pointsDone

    def move(self, points: int, speed: int):
        if self.running:
            self.stop()
        if points == 0:
            return

        self.running = True
        self.mustRun = True
        self.thread = threading.Thread(
            target=self.moveSync, args=(points, speed))
        self.thread.daemon = True
        self.thread.start()

    def moveSync(self, points: int, speed: int):
        delay = 1 / speed
        direction = 1 if points >= 0 else -1
        self.pointsDone = 0
        pointsAbs = abs(points)
        while self.mustRun:
            for i, pin in enumerate(self.motorPins):
                if self.sequence[self.step][i]:
                    pin.on()
                else:
                    pin.off()
            sleep(delay)
            self.step += direction
            if self.step >= self.steps:
                self.step = 0
            if self.step < 0:
                self.step = self.steps - 1
            self.pointsDone += 1
            if self.pointsDone >= pointsAbs:
                break
        self.running = False


class Gantry:
    def __init__(self, stepper1: Stepper, stepper2: Stepper, stopper11: Button, stopper12: Button, stopper21: Button, stopper22: Button, speed=5):
        self.stepper1 = stepper1
        self.stepper2 = stepper2
        self.stopper11 = stopper11
        self.stopper12 = stopper12
        self.stopper21 = stopper21
        self.stopper22 = stopper22
        self.speed = speed

    def initialize(self):
        speed = 2
        self.stepper1.move(-10e30, speed)
        self.stopper11.wait_for_active()
        self.stepper1.stop()
        self.stepper1.move(10e30, speed)
        self.stopper12.wait_for_active()
        self.rangeX = self.stepper1.stop()
        self.posX = self.rangeX
        self.stepper2.move(-10e30, speed)
        self.stopper21.wait_for_active()
        self.stepper2.stop()
        self.stepper2.move(10e30, speed)
        self.stopper22.wait_for_active()
        self.rangeY = self.stepper2.stop()
        self.posY = self.rangeY
        self.move(0, 0)

    def move(self, percentX: int, percentY: int):
        if not (0 <= percentX <= 100 and 0 <= percentY <= 100):
            raise ValueError('percentX and percentY must be in range [0, 100]')
        pointsX = self.rangeX * (percentX / 100)
        pointsY = self.rangeY * (percentY / 100)
        moveX = pointsX - self.posX
        moveY = pointsY - self.posY
        self.stepper1.move(moveX, self.speed)
        self.stepper2.move(moveY, self.speed)
        while self.stepper1.running or self.stepper2.running:
            sleep(0.05)
        self.posX += moveX
        self.posY += moveY


class ChessBoardGantry:
    def __init__(self, gantry: Gantry, magnet: OutputDevice):
        self.gantry = gantry
        self.magnet = magnet
        gantry.initialize()

    def toPercentage(self, cell: int):
        return (100 // 16) + cell * (100 // 8)

    def moveToCell(self, cellX: int, cellY: int):
        percentX = self.toPercentage(cellX)
        percentY = self.toPercentage(cellY)
        self.gantry.move(percentX, percentY)

    def movePiece(self, fromx, fromy, tox, toy):
        self.moveToCell(fromx, fromy)
        self.magnet.on()
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
        self.magnet.off()


def createGantry():
    return ChessBoardGantry(
        Gantry(
            Stepper(1, 2, 3, 4),
            Stepper(5, 6, 7, 8),
            Button(9),
            Button(10),
            Button(11),
            Button(12)),
        OutputDevice(13))
