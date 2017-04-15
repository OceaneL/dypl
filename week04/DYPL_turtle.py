

#from TkTurtle import TkTurtle
import re
import math

class DYPL_turtle:
    def __init__(self, application):
        self.application = application
        self.pen = False
        self.angle = 180
        self.x = 150
        self.y = 150
    def pen_down(self):
        self.pen = True
    def pen_up(self):
        self.pen = False
    def turn_cw(self, angle):
        self.angle += angle
    def turn_ccw(self, angle):
        self.angle -= angle
    def put(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
    def move_forward(self):
        self.move(1, 0)
    def move_backward(self):
        self.move(-1, 0)
    def move(self, steps, angle):
        self.turn_cw(angle)
        x_tmp = 0
        y_tmp = 0
        a = 
        if (self.pen):

    def parseExp(self, text):
        text = (re.sub(r"for (?P<var>\D.*)=(?P<begin>\d+) to (?P<end>\d+) do\n(?P<statement>.+)\nend", r"for \g<var> in range(\g<begin>,\g<end>):\n\t\g<statement>\n",text))
        text = re.sub(r"(?P<inst1>(pen|move|turn)) (?P<inst2>\D+)",r"\g<inst1>_\g<inst2>",text)
        text = re.sub(r"(?P<inst1>(pen|move|turn|put))",r"self.\g<inst1>",text)
        text = re.sub(r"(?P<inst1>(pen|move)_\D+)(?P<esp>[\t|\n| ])",r"\g<inst1>()\g<esp>",text)
        print(text)
