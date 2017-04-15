from pyparsing import *
from math import copysign,radians,degrees,cos,sin,fabs
#import turtle_program
#http://stackoverflow.com/questions/10168935/parsing-nested-function-calls-using-pyparsing

class DYPL_turtle:
  def __init__(self,drawer):
    print("/**************Entering parser**************/")
    self._penDown=True
    self._x=0
    self._y=0
    self._angle=0
    self._drawer=drawer
    self._lastWasMove=False
    self._lastXPos=0
    self._lastYPos=0
    self._variationEval=0
    self._items = ['(', ',', '+', '-', '*', ')'] #Items defining a variable
  
  def parseExp(self, expr):

    self.parseLines(expr)
    self.applyMoves()
    
  def parseLines(self, expr):
    lines = expr.split('\n')
    arithOp = "+-*"
    wordInFuncName=Word(alphanums, alphanums+"=")
    
    funcName=wordInFuncName+ZeroOrMore(wordInFuncName)

    argument=Word(arithOp + alphanums, alphanums + arithOp)
    args=argument+ZeroOrMore(","+ argument)

    func=funcName+ZeroOrMore(Literal("(")+args+Literal(")"))
    completeExpr=func+ZeroOrMore(func)
    i=0
    #print("Parsing done.")
    
    while i < len(lines) :
      line = lines[i]
      print(line)
      if line == " " or line == "" :
       i+=1
       continue
      parsedExp=completeExpr.parseString(line)
      lineTmp = ""

      if parsedExp[0]=="pen" :
        self.parsePen(parsedExp[1:])
      elif parsedExp[0]=="move":
          self.move(parsedExp[1:])
          if not self._lastWasMove:
            self._lastWasMove=True
      elif parsedExp[0]=="turn":
        self.applyMoves()
        self.turn(parsedExp[1:])
      elif parsedExp[0]=="put":
        self.applyMoves()
        self.put(parsedExp[1:])

      elif parsedExp[0]=="for":
        while ("".join(line).strip() != "end"):
          lineTmp += "\n"
          lineTmp += line
          i += 1
          line = lines[i]
        self.parseFor(lineTmp)
        self.applyMoves()
      
      i += 1
      """if the cursor has moved continously more than roughly 1 pixel,
      without any drawing, trace a line immediately
      """
      if self._variationEval >= 1:
        self.applyMoves()
        self._variationEval=0
    
  def parseForExp(self, expr,varName,value):
   index = expr.find(varName)
   if index == -1:
    return expr
   print("mais qu'est-ce que tu fous ?")
   while(index != -1) :
    #print(index)
    expr=expr.replace(" ","")
    print("%s %s %s"%(expr[index-1],expr[index],expr[index+1]))
    
    if self.isAVariable(expr,index): 
     expr=expr[:index]+str(value)+expr[index+1:]
     index=expr.find(varName)
    #print(expr)
   return expr
    
     
  def parseFor(self,expr):
   arithOp = "+-*"
   wordInFuncName=Word(alphanums, alphanums+"=")    
   funcName=wordInFuncName+ZeroOrMore(wordInFuncName)
   argument=Word(arithOp + alphanums, alphanums + arithOp)
   args=argument+ZeroOrMore(","+ argument)
   func=funcName+ZeroOrMore(Literal("(")+args+Literal(")"))
   
   
   forParser = "for" +Word(alphanums) + "=" + Word(nums) + "to" + Word(nums) + "do" + ZeroOrMore(func)
   #for it in range(int(expr[6]),int(11)):
   tmp = forParser.parseString(expr)
   varName=tmp[1]
   endOfFor=int(tmp[5])+1
   splitExpr= expr.split("\n")[2:]
   print("avant boucle du parse for")
   for it in range(int(tmp[3]),endOfFor):
    print(it)
    for line in splitExpr :
     line=self.parseForExp(line,varName,it)
     print("sortie parseforexp")
     self.parseLines(line)
     print("line est %s" % line)
   #print("Le retour est :")
   #print(tmp)
   
  def parsePen(self,expr):
    if expr[0]=="up":
      self._penDown=False
    elif expr[0]=="down":
      self._penDown=True
    
    #print("pen is %r" % self._penDown)

  def move_fwd_or_bckwd(self,isBackward=False):
    #print("l'angle vaut %f" % degrees(self._angle))
    if isBackward :
      self._lastXPos=cos(self._angle)+self._lastXPos
      self._lastYPos=-sin(self._angle)+self._lastYPos
      #print("j'ai fait %f:%f" % (cos(self._angle),-sin(self._angle)))
    else :
      self._lastXPos=cos(self._angle)+self._lastXPos
      self._lastYPos=sin(self._angle)+self._lastYPos
      #print("j'ai fait %f:%f" % (cos(self._angle),sin(self._angle)))
    #print("le resultat est %d:%d" % (self._lastXPos,self._lastYPos))
    self._variationEval+=1

  def move(self,expr):
    if expr[0]=="forward":
      self.move_fwd_or_bckwd()
      
    elif expr[0]=="backward":
      self.move_fwd_or_bckwd(True)
 
    
    #move(steps,angle)  
    elif expr[0]=="(":
      self.turn(["ccw","(",expr[3],")"]) 
      
      for it in range(0,int(expr[1])):
        self.move_fwd_or_bckwd()
  
  #http://stackoverflow.com/questions/20202418
  def cmp(self,a,b):
    return (a>b)-(a<b)
  
  #https://en.wikipedia.org/wiki/Bresenham's_line_algorithm    
  def applyMoves(self):
    print("Bresen %d:%d" % (self._lastXPos,self._lastYPos))
    deltax=self._lastXPos-self._x
    deltay=self._lastYPos-self._y
    if deltax != 0:
      deltaerr=fabs(deltay/deltax)
    
    x=int(self._x)
    y=int(self._y)
    
    print("deltax : %f" %deltax)
    print("deltay : %f"% deltay)
    if deltax != 0 and fabs(deltax) >= fabs(deltaerr):
      print("first kill %f, %f,%f,%f" % (abs(x) ,fabs(self._lastXPos -1),fabs(self._lastXPos-x),fabs(deltaerr)))
      error=-1

      while(fabs(self._lastXPos-x) >= 1 ):
        print("%f:%f:%f:%r"%(x,fabs(self._lastXPos-x),fabs(deltaerr),fabs(self._lastXPos-x) >= fabs(deltaerr)))
        self.write(x,y)
        error=error+deltaerr
        if error >= 0.0:
          y+=self.cmp(self._lastYPos-y,0)*1
          error=error-1
        x+=self.cmp(self._lastXPos-x,0)*1
    
    else:
      print("y: %f, lastY: %f"%(y,self._lastYPos))
      while(fabs(self._lastYPos-y) >= 1 and y!= self._lastYPos):
        print("%f:%f"%(y,self._lastYPos-y))
        y+=self.cmp(self._lastYPos-y,0)*1
        self.write(int(self._x),y)
        
    self._lastWasMove=False
    self._x=x
    self._y=y
    print("Now at %d:%d" % (self._x,self._y))
    
  def isVariable(self, expr, index):
    return not expr[index-1] == "(" and expr[index-1] in self._items and expr[index+1] in self_items
    
  def add_angle(self,second_angle):
    self._angle+=radians(second_angle)

  def turn(self, expr):

    if expr[0]=="cw":
      self.add_angle(-int(expr[2]))
    elif expr[0]=="ccw":
      self.add_angle(int(expr[2]))
    
  def write(self, x, y):
    print("writing...")
    if not self._penDown:
      return
    
    self._drawer.setPixel(x,y)
    
  def put(self, expr):
    self._x=int(eval(expr[1]))
    self._y=int(eval(expr[3]))
    self._lastXPos=self._x
    self._lastYPos=self._y
    self._angle=radians(float(eval(expr[5])))

    
 
"""
parser=DYPL_turtle(None)


parser.parseLines("for X=1 to 10 do\nmove(X,0) \nend\n")
"""