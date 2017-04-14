

#from TkTurtle import TkTurtle
import re

class DYPL_turtle:
    def __init__(self, application):
        self.application = application
    def parseExp(self, text):
        print (text)
        print ("\n\n")
        print (re.sub(r"for (?P<var>\D\d*)=(?P<begin>\d+) to (?P<end>\d+) do\n(?P<statement>.+)\nend", r"for \g<var> in range(\g<begin>,\g<end>):\n\t\g<statement>\n",text))
