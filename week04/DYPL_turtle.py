

#from TkTurtle import TkTurtle
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
        self.angle = 180
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
            y1 = self.y - round(math.sin(math.radians(360-self.angle)) * steps)
            x1 = self.x + round(math.cos(math.radians(360-self.angle)) * steps)
            print(self.x,self.y,x1,y1)
            if self.x < x1:
                if self.y< y1:
                    self.plotLine(self.x, self.y, x1, y1)
                else:
                    self.plotLine2(self.x, self.y, x1, y1)
            else:
                if self.y< y1:
                    self.plotLine2(x1, y1, self.x, self.y)
                else:
                    self.plotLine(x1, y1, self.x, self.y)

            self.x = x1
            self.y = y1
            #done = 0.0
            # n = round(abs(math.sin(math.radians(self.angle))) * steps + abs(math.cos(math.radians(self.angle))) * steps)
            # tmp_angle = self.angle
            # # for i in range (0, n):
            # while (done < n):
            #     next_angle = self.get_closest_angle(tmp_angle)
            #     tmp_angle += self.angle - next_angle.angle
            #     self.x += next_angle.x
            #     self.y += next_angle.y
            #     self.application.setPixel(max(self.x, 0), max(self.y, 0))
            #     done += abs(next_angle.x) + abs(next_angle.y)


    def parseExp(self, text):
        text = (re.sub(r"for (?P<var>\D.*) *= *(?P<begin>\d+) to (?P<end>\d+) do\n(?P<statement>((pen|move|turn|put).*\n)+)end", f ,text))
        text = re.sub(r"(?P<inst1>(pen|move|turn)) (?P<inst2>\D+)",r"\g<inst1>_\g<inst2>",text)
        text = re.sub(r"(?P<inst1>(pen|move|turn|put))",r"self.\g<inst1>",text)
        text = re.sub(r"(?P<inst1>(pen|move)_\D+)(?P<esp>[\t|\n| ])",r"\g<inst1>()\g<esp>",text)
        #print(text)
        exec(text)

    def plotLine(self,x0,y0,x1,y1):
      dx = x1 - x0
      dy = y1 - y0
      if (dx > dy):
          D = 2*dy - dx
          y = y0
          for x in range(x0,x1):
            self.application.setPixel(max(x, 0), max(y, 0))
            if D > 0 :
               y = y + 1
               D = D - 2*dx
            D = D + 2*dy
      else:
          D = 2*dx - dy
          x = x0
          for y in range(y0,y1):
            self.application.setPixel(max(x, 0), max(y, 0))
            if D > 0 :
               x = x + 1
               D = D - 2*dy
            D = D + 2*dx

    def plotLine2(self,x0,y0,x1,y1):
      dx = x1 - x0
      dy = y0 - y1
      if (dx > abs(dy)):
          D = 2*dy - dx
          y = y0
          for x in range(x0,x1):
            self.application.setPixel(max(x, 0), max(y, 0))
            if D > 0 :
               y = y - 1
               D = D + 2*dx
            D = D - 2*dy
      else:
          D = 2*dx - dy
          x = x0
          for y in range(y0,y1,-1):
            self.application.setPixel(max(x, 0), max(y, 0))
            if D > 0 :
               x = x + 1
               D = D + 2*dy
            D = D - 2*dx

def f(matchobj):
    s = "for "+matchobj.group('var')+" in range("+matchobj.group('begin')+","+matchobj.group('end')+"):\n"
    s += re.sub(r"(?P<line>.*\n)", r"\t\g<line>",matchobj.group('statement'))
    return s



#r"for \g<var> in range(\g<begin>,\g<end>):\n\t\g<statement>\n"
