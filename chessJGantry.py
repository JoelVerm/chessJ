import threading
from time import sleep
from gpiozero import OutputDevice, Button


class Stepper:
    class Resolutions:
        One = (0, 0, 0, 1),
        Two = (1, 0, 0, 2),
        Four = (0, 1, 0, 4),
        Eight = (1, 1, 0, 8),
        Sixteen = (0, 0, 1, 16),
        Thirty_two = (1, 0, 1, 32)

    def __init__(self, directionPin, stepPin, resPin1, resPin2, resPin3):
        self.directionPin = OutputDevice(directionPin)
        self.stepPin = OutputDevice(stepPin)
        self.resPin1 = OutputDevice(resPin1)
        self.resPin2 = OutputDevice(resPin2)
        self.resPin3 = OutputDevice(resPin3)
        self.stepsDone = 0
        self.running = False
        self.mustRun = False
        self.thread = None

    def stop(self):
        if self.running and self.thread:
            self.mustRun = False
            self.thread.join()
        return self.stepsDone

    def move(self, points: int, speed: int, resolution: Resolutions):
        if self.running:
            self.stop()
        if points == 0:
            return

        self.running = True
        self.thread = threading.Thread(
            target=self.moveSync, args=(points, speed, resolution))
        self.thread.daemon = True
        self.thread.start()

    def writePin(pin: OutputDevice, value: bool):
        if value:
            pin.on()
        else:
            pin.off()

    def moveSync(self, points: int, speed: int, resolution: Resolutions):
        delay = 1 / speed / 2 / resolution[3]
        self.writePin(self.directionPin, points >= 0)
        self.writePin(self.resPin1, resolution[0])
        self.writePin(self.resPin2, resolution[1])
        self.writePin(self.resPin3, resolution[2])
        self.stepsDone = 0
        stepsAbs = abs(points)
        self.mustRun = True
        while self.mustRun:
            self.stepPin.on()
            sleep(delay)
            self.stepPin.off()
            sleep(delay)
            self.stepsDone += 1
            if self.stepsDone >= stepsAbs:
                break
        self.running = False


class Gantry:
    def __init__(self, stepper1: Stepper, stepper2: Stepper, rangeX: int, rangeY: int , speed=1000, resolution: Stepper.Resolutions = Stepper.Resolutions.Eight):
        self.stepper1 = stepper1
        self.stepper2 = stepper2
        self.rangeX = rangeX
        self.rangeY = rangeY
        self.speed = speed
        self.resolution = resolution
        self.posX = 0
        self.posY = 0

    def move(self, percentX: int, percentY: int):
        if not (0 <= percentX <= 100 and 0 <= percentY <= 100):
            raise ValueError('percentX and percentY must be in range [0, 100]')
        pointsX = self.rangeX * (percentX / 100)
        pointsY = self.rangeY * (percentY / 100)
        moveX = pointsX - self.posX
        moveY = pointsY - self.posY
        self.stepper1.move(moveX, self.speed, self.resolution)
        self.stepper2.move(moveY, self.speed, self.resolution)
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
            Stepper(5, 6, 13, 19, 26),
            Stepper(2, 3, 14, 15, 18),
            1000, 1000
        ),
        OutputDevice(13)
    )
