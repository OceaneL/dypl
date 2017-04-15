

#from TkTurtle import TkTurtle
import re

class DYPL_turtle:
    def __init__(self, application):
        self.application = application
    def parseExp(self, text):
        text = (re.sub(r"for (?P<var>\D.*)=(?P<begin>\d+) to (?P<end>\d+) do\n(?P<statement>.+)\nend", r"for \g<var> in range(\g<begin>,\g<end>):\n\t\g<statement>\n",text))
        text = re.sub(r"(?P<inst1>(pen|move|turn)) (?P<inst2>\D+)",r"\g<inst1>_\g<inst2>",text)
        text = re.sub(r"(?P<inst1>(pen|move|turn|put))",r"self.\g<inst1>",text)
        text = re.sub(r"(?P<inst1>(pen|move)_\D+)(?P<esp>[\t|\n| ])",r"\g<inst1>()\g<esp>",text)
        print(text)
