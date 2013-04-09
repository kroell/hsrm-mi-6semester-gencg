from Tkinter import *
from Canvas import *
import sys
from test.test_mhlib import readFile

WIDTH  = 400 # width of canvas
HEIGHT = 400 # height of canvas

HPSIZE = 2 # half of point size (must be integer)
CCOLOR = "#0000FF" # blue

elementList = [] # list of elements (used by Canvas.delete(...))

polygon = [[50,50],[350,50],[350,350],[50,350],[50,50]]

time = 0
dt = 0.1

def drawObjects():
    """ draw polygon and points """
    # TODO: inpterpolate between polygons and render
    for (p,q) in zip(polygon,polygon[1:]):
        elementList.append(can.create_line(p[0], p[1], q[0], q[1], fill=CCOLOR))
        #print "p ",p
        #print "q ",q
        elementList.append(can.create_oval(p[0]-HPSIZE, p[1]-HPSIZE, p[0]+HPSIZE, p[1]+HPSIZE, fill=CCOLOR, outline=CCOLOR))
            

def quit(root=None):
    "Programm beenden"
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    "Elemente zeichnen"
    can.delete(*elementList)
    del elementList[:]
    drawObjects()
    can.update()


def forward():
    "Vorwaerts morphen"
    global time
    while(time<1):
        time += dt
        # TODO: interpolate
        print time
        draw()

def backward():
    "Rueckwaerts morphen"
    global time
    while(time>0):
        time -= dt
        # TODO: interpolate 
        print time
        draw()

def readFile(fileName):
    "Datei einlesen und Inhalt als Liste [[float,float]] zurueckgeben"
    # Ausgabe Dateinamen
    print "Polygondatei: ", fileName
    
    f = file(fileName).readlines()
    lis = []
    
    for i in f: 
        n = i.split()
        lis.append(map(float, n))
    return lis

def localToGlobal(lis, min=0):
    "Von lokalem in globales Koordinatensystem umwandeln"
    for i in lis:
        x = min + i[0] * WIDTH
        y = min + HEIGHT - i[1] * HEIGHT
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
    
    
    # polygonA als Anfang setzen
    polygon = polygonA   

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
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()
    
    # Objekte zeichnen
    draw()
    
    # start
    mw.mainloop() 