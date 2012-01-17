from Xlib import X, display
import time

class MouseLogger(object):
    def __init__(self):
        self.mouse_positions = list()
        self.display = display.Display()
        Xscreen = self.display.screen()
        self.root = Xscreen.root

    def log_mouse(self):
        time.sleep(0.01)
        self.display.sync()
        mouse_pos = self.root.query_pointer()._data
        self.__log_position(mouse_pos["root_x"],
            mouse_pos["root_y"])

    def __log_position(self, x, y):
        self.mouse_positions.append(Coordinate(x, y))

    def write_log(self):
        for pos in self.mouse_positions:
            print pos

class Coordinate(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "%d\t%d" % (self.x, self.y)
