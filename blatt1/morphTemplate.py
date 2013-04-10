'''
Created on 09.04.2013

Generative Computergrafik, Uebungsblatt 1, Aufgabe 5
Hochschule RheinMain, Medieninformatik

@author: soerenkroell
'''

#!/usr/bin/python
# -*-coding: utf-8 -*-


from Tkinter import *
from Canvas import *
import sys
import copy


WIDTH  = 400 # width of canvas
HEIGHT = 400 # height of canvas

HPSIZE = 2 # half of point size (must be integer)
CCOLOR = "#0000FF" # blue

ELEMENT_LIST = [] # list of elements (used by Canvas.delete(...))

#polygon = [[50,50],[350,50],[350,350],[50,350],[50,50]]
#time = 0

DT = 0.01

def drawObjects():
    "draw polygon and points"
    for (p,q) in zip(polygon,polygon[1:]):
        ELEMENT_LIST.append(can.create_line(p[0], p[1], q[0], q[1], fill=CCOLOR))
        ELEMENT_LIST.append(can.create_oval(p[0]-HPSIZE, p[1]-HPSIZE, p[0]+HPSIZE, p[1]+HPSIZE, fill=CCOLOR, outline=CCOLOR))
            
            
def quitProgram(root=None):
    "Programm beenden"
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()

def draw():
    "Elemente zeichnen"
    can.delete(*ELEMENT_LIST)
    del ELEMENT_LIST[:]
    drawObjects()
    can.update()

def forward():
    "Vorwaerts morphen"
    time = 0

    while(time < 1):
        time += DT
        # interpolate 
        # Grundlage: p(t) = (1-t) * p1 + t * p2 
        for i in range(len(polygon)): 
            polygon[i][0] = (1 - time) * polygonAdc[i][0] + time * polygonZdc[i][0]
            polygon[i][1] = (1 - time) * polygonAdc[i][1] + time * polygonZdc[i][1]
            
        draw()

def backward():
    "Rueckwaerts morphen"
    time = 0
  
    while(time < 1):
        time += DT
        # interpolate
        # Grundlage: p(t) = (1-t) * p1 + t * p2 
        for i in range(len(polygon)): 
            polygon[i][0] = (1 - time) * polygonZdc[i][0] + time * polygonAdc[i][0]
            polygon[i][1] = (1 - time) * polygonZdc[i][1] + time * polygonAdc[i][1]
    
        draw()

def readFile(fileName):
    "Datei einlesen und Inhalt als Liste [[x,y]] zurueckgeben"
    # Ausgabe Dateinamen
    print "Polygondatei: ", fileName
    
    f = file(fileName).readlines()
    lis = []
    
    for i in f: 
        n = i.split()
        #x,y Koordinaten als float in Liste schreiben
        lis.append(map(float, n))
    return lis

def localToGlobal(lis):
    "Von lokalem in globales Koordinatensystem umwandeln"
    for i in lis:
        #x und y neu berechnen mit der Canvas Breite und Hoehe
        x = i[0] * WIDTH
        y = HEIGHT - i[1] * HEIGHT
        #die neuen x und y Werte setzen
        i[0] = x
        i[1] = y


if __name__ == "__main__":
    # check parameters
    if len(sys.argv) != 3:
        print "morph.py firstPolygon secondPolygon"
        sys.exit(-1)

    # - read in polygons -
    polygonA = readFile(sys.argv[1])
    polygonZ = readFile(sys.argv[2])
    
    # - transform from local into global coordinate system 
    localToGlobal(polygonA)
    localToGlobal(polygonZ)
    
    # - make both polygons contain same number of points
    if len(polygonA) > len(polygonZ):
        polygonZ.append(polygonZ[0])
    elif len(polygonA) < len(polygonZ):
        polygonA.append(polygonA[0])
    
    # polygonA als Anfang setzen
    polygon = polygonA[:]
    
    # tiefe Kopie von A und Z erstellen
    polygonAdc = copy.deepcopy(polygonA)
    polygonZdc = copy.deepcopy(polygonZ)

    # GUI
    mw = Tk()
    mw._root().wm_title("Morphing")

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.pack()
    cFr = Frame(mw)
    cFr.pack(side="left")
    bClear = Button(cFr, text="backward", command=backward)
    bClear.pack(side="left")
    bClear = Button(cFr, text="forward", command=forward)
    bClear.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quitProgram(root)))
    bExit.pack()
    
    # Objekte zeichnen
    draw()
    
    # start
    mw.mainloop() 