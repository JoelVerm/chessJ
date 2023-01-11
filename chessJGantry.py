import threading
from time import sleep
from gpiozero import OutputDevice


class Stepper:
    def __init__(self, pin1, pin2, pin3, pin4):
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
        self.running = False
        self.mustRun = False
        self.thread = None

    def stop(self):
        if self.running and self.thread:
            self.mustRun = False
            self.thread.join()

    def move(self, points, speed):
        if self.running:
            self.stop()
        if points == 0:
            return

        self.running = True
        self.mustRun = True
        self.thread = threading.Thread(
            target=self.moveThreaded, args=(points, speed))
        self.thread.daemon = True
        self.thread.start()

    def moveThreaded(self, points, speed):
        delay = 1 / speed
        direction = 1 if points >= 0 else -1
        pointsDone = 0
        pointsAbs = abs(points)
        step = 0
        steps = len(self.sequence)
        while self.mustRun:
            for i, pin in enumerate(self.motorPins):
                if self.sequence[step][i]:
                    pin.on()
                else:
                    pin.off()
            sleep(delay)
            step += direction
            if step >= steps:
                step = 0
            if step < 0:
                step = steps - 1
            pointsDone += 1
            if pointsDone >= pointsAbs:
                break
        self.running = False


class Gantry:
    def __init__(self, motor1pins=[1, 2, 3, 4], motor2pins=[5, 6, 7, 8]):
        self.stepper1 = Stepper(*motor1pins)
        self.stepper2 = Stepper(*motor2pins)
        self.speed = 5

    def move(self, percentX, percentY):
        pass


def main():
    pass


if __name__ == '__main__':
    main()
