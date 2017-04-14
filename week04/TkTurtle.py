#!/usr/bin/env python

import tkinter as tk
import sys
from DYPL_turtle import DYPL_turtle

WIDTH, HEIGHT = 640, 480

class Application(tk.Frame):
    def __init__(self, filename, master=None):

        self.filename = filename
        self.counter = 0
        tk.Frame.__init__(self, master)
        self.code = self.loadCode(filename)
        self.colour = "#000000"

        print(self.code)
        self.grid()
        self.createWidgets()

    def createWidgets(self):

        self.prevButton = tk.Button(self, text='Previous', command=self.previous)
        self.prevButton.grid(row=0, column=0)

        self.runButton = tk.Button(self, text='Run', command=self.run)
        self.runButton.grid(row=0, column=1)

        self.nxtButton = tk.Button(self, text='Next', command=self.next)
        self.nxtButton.grid(row=0, column=2)

        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row=0, column=3)

        self.codeArea = tk.Text(self, height=20, width=10)
        self.codeArea.grid(row=1, column=0, sticky="N")
        self.codeArea.insert(tk.INSERT, self.code[0])

        self.drawingArea = tk.Canvas(self, width=WIDTH, height=HEIGHT)
        self.drawingArea.grid(row=1, column=1)
        self.img = tk.PhotoImage(width=WIDTH, height=HEIGHT)
        self.drawingArea.create_image((WIDTH/2, HEIGHT/2), image=self.img, state="normal")


        self.turtle = DYPL_turtle(self)


    def loadCode(self, filename):
        code = []
        p_count = 0
        f = open(filename)
        lines = f.readlines()
        for l in lines:
            l = l.strip()
            if l == "":
                p_count += 1
            elif (len(code) > p_count) and code[p_count]:
                code[p_count] = code[p_count] + "\n" + l
            else:
                code.append(l)
        return code

    def previous(self):
        print("previous")
        if self.counter > 0:
            self.counter -= 1
            self.codeArea.delete(1.0,tk.END)
            self.codeArea.insert(tk.INSERT, self.code[self.counter])
        elif self.counter == 0:
            self.counter -= 1
            self.codeArea.delete(1.0,tk.END)
            self.codeArea.insert(tk.INSERT, "No more previous code")

    def next(self):
        if self.counter < len(self.code)-1:
            self.counter += 1
            self.codeArea.delete(1.0,tk.END)
            self.codeArea.insert(tk.INSERT, self.code[self.counter])
        elif self.counter == len(self.code)-1:
            self.counter += 1
            self.codeArea.delete(1.0,tk.END)
            self.codeArea.insert(tk.INSERT, "No more next code")


    def run(self):
        if (self.counter > len(self.code)-1) or (self.counter < 0):
            print("No code loaded")
        else:
            print("run: ", str(self.counter))
            self.turtle.parseExp(self.code[self.counter])

    def setPixel(self, x, y):
        self.img.put(self.colour, (x+100, y) )

    def setColour(self, colour):
        self.colour = colour

def main(filename):

    app = Application(filename)
    app.master.title('DYPL Turtle Drawing Program')
    app.mainloop()

if len(sys.argv) < 2:
    print("Use: turtleprogram <filename>")
else:
    main(sys.argv[1])
