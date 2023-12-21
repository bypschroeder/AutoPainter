from logging import Logger
from serial.tools import list_ports
from pydobot import Dobot


def calculate_points(points):
    output = []
    for point in points:
        print("Calc Input:", point)
        new_point = [point[1] + 200, point[0] - 50]
        output.append(new_point)
    return output


class DobotController:

    def __init__(self, logger: Logger, port=2):
        self.logger = logger
        self.bot = self.init_bot(port)

    def init_bot(self, port):
        ports = list_ports.comports()
        self.logger.debug("ports: {}".format(ports))

        if len(ports) == 0:
            self.logger.error("No Dobot detected")
            return None

        device_port = ports[port].device
        device = Dobot(port=device_port, verbose=False)

        device.speed(100, 100)

        return device

    def homing(self):
        print("homing")
        self.bot.move_to(250, 0, 0, 0, wait=True)
        print("finished homing")

    def draw_line(self, x1, y1, x2, y2):
        try:
            print("drawing:", x1, y1, "to", x2, y2)

            self.bot.move_to(x1, y1, 0, 0, wait=True)
            self.bot.move_to(x1, y1, -50, 0, wait=True)
            self.bot.move_to(x2, y2, -50, 0, wait=True)
            self.bot.move_to(x2, y2, 0, 0, wait=True)
        except Exception as e:
            print('Error:', e)
            print("Coordinates out of range!")

    def draw_dot_to_dot(self, points):
        points = calculate_points(points)
        for x in range(0, len(points) - 1):
            print("drawing:", points[x][0], points[x][1], points[x + 1][0], points[x + 1][1])
            self.draw_line(points[x][0], points[x][1], points[x + 1][0], points[x + 1][1])
