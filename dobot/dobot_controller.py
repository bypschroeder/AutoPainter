from logging import Logger
from serial.tools import list_ports
from pydobot import Dobot


def calculate_points(points):
    """
    Re-calculate the points to fit the Dobot's coordinate system
    :param points: List of points to calculate
    :return: List of calculated points
    """

    from app import CALC_POINTS_OFFSET_X, CALC_POINTS_OFFSET_Y

    output = []
    for point in points:
        print("Calc Input:", point)
        new_point = [point[1] + CALC_POINTS_OFFSET_X, point[0] - CALC_POINTS_OFFSET_Y]
        output.append(new_point)
    return output


class DobotController:

    def __init__(self, logger: Logger, port=2):
        self.logger = logger
        self.is_connected = False
        self.bot = self.init_bot(port)

    def init_bot(self, port):
        """
        Initiate the Dobot and return the device
        :param port: The port the Dobot is connected to
        :return: device
        """

        ports = list_ports.comports()
        self.logger.debug("ports: {}".format(ports))

        if len(ports) == 0:
            self.logger.error("No Dobot detected")
            return False

        device_port = ports[port].device
        device = Dobot(port=device_port, verbose=False)

        device.speed(100, 100)
        self.is_connected = True
        return device

    def draw_line(self, x1, y1, x2, y2):
        """
        Draw a line with the Dobot from point 1 to point 2
        :param x1: x coordinate of point 1
        :param y1: y coordinate of point 1
        :param x2: x coordinate of point 2
        :param y2: y coordinate of point 2
        """

        from app import Z_AXIS_HEIGHT

        try:
            print("drawing:", x1, y1, "to", x2, y2)

            self.bot.move_to(x1, y1, 0, 0, wait=True)
            self.bot.move_to(x1, y1, Z_AXIS_HEIGHT, 0, wait=True)
            self.bot.move_to(x2, y2, Z_AXIS_HEIGHT, 0, wait=True)
            self.bot.move_to(x2, y2, 0, 0, wait=True)
        except Exception as e:
            print('Error:', e)
            print("Coordinates out of range!")

    def draw_dot_to_dot(self, points):
        """
        Draw multiple lines with the Dobot from point to point
        :param points: List of points to draw
        """

        points = calculate_points(points)
        for x in range(0, len(points) - 1):
            print("drawing:", points[x][0], points[x][1], points[x + 1][0], points[x + 1][1])
            self.draw_line(points[x][0], points[x][1], points[x + 1][0], points[x + 1][1])

    def draw_area(self, points):
        """
        Color an area with the Dobot by connecting the points and filling the area
        :param points: List of points that form the area
        """

        calculated_points = calculate_points(points)

        for i in range(len(calculated_points) -1):
            x1, y1 = calculated_points[i]
            x2, y2 = calculated_points[i + 1]
            self.draw_line(x1, y1, x2, y2)

        x1, y1 = calculated_points[-1]
        x2, y2 = calculated_points[0]
        self.draw_line(x1, y1, x2, y2)
        self.bot.move_to(x2, y2, -20, 0, wait=True)

        top_y = max([point[1] for point in calculated_points])

        farthest_x = max(point[0] for point in calculated_points if point[1] == top_y)
        nearest_x = min(point[0] for point in calculated_points if point[1] == top_y)

        current_y = top_y
        while current_y > min([point[1] for point in calculated_points]):
            self.draw_line(farthest_x, current_y, x2, current_y)
            current_y -= 2
