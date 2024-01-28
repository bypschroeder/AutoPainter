from logging import Logger
from serial.tools import list_ports
from pydobot import Dobot
import serial
import time


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
            return False

        try:
            device_port = ports[port].device
            serial_connection = serial.Serial()
            serial_connection.port = device_port
            serial_connection.baudrate = 115200
            serial_connection.timeout = 2
            serial_connection.open()

            time.sleep(1)

            device = Dobot(port=device_port, verbose=False)
            device.speed(100, 100)
            self.bot = device
            return True
        except Exception as e:
            self.logger.error("Error: {}".format(e))
            return False

        # device_port = ports[port].device
        # device = Dobot(port=device_port, verbose=False)
        #
        # device.speed(100, 100)

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