import re
import math

class Angle:
    def __init__(self, angle, x, y):
        self.angle = angle
        self.x = x
        self.y = y

class DYPL_turtle:
    def __init__(self, application):
        self.application = application
        self.pen = False
        self.angle = 90
        self.x = 150
        self.y = 150
        self.angles = [
            Angle(0, 0, -1),
            Angle(45, 1, -1),
            Angle(90, 1, 0),
            Angle(135, 1, 1),
            Angle(180, 0, 1),
            Angle(225, -1, 1),
            Angle(270, -1, 0),
            Angle(315, -1, -1),
            Angle(360, 0, -1)
        ]
    def get_closest_angle(self, angle_):
        a = list(map(lambda x: abs(angle_ - x.angle), self.angles))
        return self.angles[a.index(min(a))]
    def pen_down(self):
        self.pen = True
    def pen_up(self):
        self.pen = False
    def turn_cw(self, angle_):
        self.angle += angle_
        self.angle %= 360
    def turn_ccw(self, angle_):
        self.angle -= angle_
        self.angle %= 360
    def put(self, x, y, angle_):
        self.x = x
        self.y = y
        self.angle = angle_
        self.angle %= 360
    def move_forward(self):
        self.move(1, 0)
    def move_backward(self):
        self.move(-1, 0)
    def move(self, steps, angle_):
        self.turn_cw(angle_)
        if (self.pen):
            rad = math.radians((self.angle + 270) % 360)
            dx = math.cos(rad)
            dy = math.sin(rad)
            for i in range (0, steps):
                self.x += dx
                self.y += dy
                self.application.setPixel(round(max(self.x, 0)), round(max(self.y, 0)))
    def parseExp(self, text):
        text = (re.sub(r"for (?P<var>\D.*) *= *(?P<begin>\d+) to (?P<end>\d+) do\n(?P<statement>((pen|move|turn|put).*\n)+)end", f ,text))
        text = re.sub(r"(?P<inst1>(pen|move|turn)) (?P<inst2>\D+)",r"\g<inst1>_\g<inst2>",text)
        text = re.sub(r"(?P<inst1>(pen|move|turn|put))",r"self.\g<inst1>",text)
        text = re.sub(r"(?P<inst1>(pen|move)_\D+)(?P<esp>[\t|\n| ])",r"\g<inst1>()\g<esp>",text)
        print(text)
        exec(text)

def f(matchobj):
    s = "for "+matchobj.group('var')+" in range("+matchobj.group('begin')+","+matchobj.group('end')+"):\n"
    s += re.sub(r"(?P<line>.*\n)", r"\t\g<line>",matchobj.group('statement'))
    return s

#r"for \g<var> in range(\g<begin>,\g<end>):\n\t\g<statement>\n"
