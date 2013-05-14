from Tkinter import *
from Canvas import *
import sys
import math
#import whrandom

WIDTH  = 400 # width of canvas
HEIGHT = 400 # height of canvas

HPSIZE = 1 # double of point size (must be integer)
COLOR = "#0000FF" # blue

NOPOINTS = 1000

scaledPoints = []
#finalPoints  = []
pointList = [] # list of points (used by Canvas.delete(...))

def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()

def draw():
    """ draw points """
    for point in pointList:
        x,y = point
        can.create_oval(x-HPSIZE, y-HPSIZE, x+HPSIZE, y+HPSIZE, fill=COLOR, outline=COLOR)

def rotYp():
    """ rotate counterclockwise around y axis """
    #global NOPOINTS
    #NOPOINTS += 100
    #print "In rotYp: ", NOPOINTS 
    
    global scaledPoints
    global pointList
    #global finalPoints
    alpha = 10 * math.pi / 180
    rotatedPoints = rotateYMatrix(alpha, scaledPoints)
    finalPoints = scaleFrame(rotatedPoints)
    pointList = finalPoints
    
    can.delete(*pointList)
    draw()

def rotYn():
    """ rotate clockwise around y axis """
    global NOPOINTS
    NOPOINTS -= 100
    print "In rotYn: ", NOPOINTS 
    can.delete(*pointList)
    draw()

def createBoundingBox(points):
    "Bounding Box erstellen indem die min und max Werte des Modells ausgerechnet werden"
    
    # Min-Werte berechnen
    xMin = min([x[0] for x in points])
    yMin = min([x[1] for x in points])
    zMin = min([x[2] for x in points])
    
    # Max-Werte berechnen
    xMax = max([x[0] for x in points])
    yMax = max([x[1] for x in points])
    zMax = max([x[2] for x in points])
    
    return xMin, yMin, zMin, xMax, yMax, zMax

# Verschieben Sie den Mittelpunkt der Boundingbox des Modells in den Ursprung
def calcDeltas(boundingBox):
    "Berechnen der Deltas, die zum verschieben der Bounding Box benoetigt werden"
    xMin, yMin, zMin, xMax, yMax, zMax = boundingBox
    
    deltaX = calcDeltaHelper(xMin, xMax)
    deltaY = calcDeltaHelper(yMin, yMax)
    deltaZ = calcDeltaHelper(zMin, zMax)
    
    return deltaX, deltaY, deltaZ

def calcDeltaHelper(min, max):
    "Helper zum Berechnen der Delta Werte"
    return min + ((max - min) / 2)

def moveBoundingBox(deltaValues, points):
    "Verschieben der Bounding Box durch Abzug der Delta Werte auf den jeweils x,y,z Werten"
    deltaX, deltaY, deltaZ = deltaValues
    movedX = [x[0] - deltaX for x in points]
    movedY = [x[1] - deltaY for x in points]
    movedZ = [x[2] - deltaZ for x in points]
    
    return zip(movedX, movedY, movedZ)

def scaleBoundingBox(movedPoints):
    "Skalieren der Bounding Box indem jeder x,y,z Wert durch den xMax oder yMax geteilt wird"
    xMax = max([x[0] for x in movedPoints])
    yMax = max([x[1] for x in movedPoints])
    zMax = max([x[2] for x in movedPoints])
    
    if xMax > yMax:
        div = xMax
    else:
        div = yMax

    return [[x[0]/div, x[1]/div, x[2]/div] for x in movedPoints]

def scaleFrame(scaledPoints):
    "Punkte an Bildschirmaufloesung anpassen"
    print "scaleFrame: ", scaledPoints[:3]
    #print [[x[0] * WIDTH/2 + WIDTH/2, HEIGHT - (x[1] * HEIGHT/2 + HEIGHT/2)] for x in scaledPoints]
    return [[x[0] * WIDTH/2.0 + WIDTH/2,HEIGHT - (x[1] * HEIGHT/2.0 + HEIGHT/2.0)] for x in scaledPoints]


def rotateYMatrix(alpha,scaledPoints):
    "Matrix zum Rotieren um die Y-Achse"
    
#    x_new = [[math.cos(alpha) * x[0] for x in scaledPoints] + [math.sin(alpha) * x[2] for x in scaledPoints]]
 #   y_new = [1 * x[1] for x in scaledPoints] 
  #  z_new = [[-math.sin(alpha) * x[0] for x in scaledPoints] + [math.cos(alpha) * x[2] for x in scaledPoints]]

#    return [x_new,y_new,z_new]

    return [[math.cos(alpha)*p[0] - math.sin(alpha)*p[2], p[1], math.sin(alpha) * p[0]+math.cos(alpha) * p[2]] for p in scaledPoints]

if __name__ == "__main__":
    #check parameters
    if len(sys.argv) == 1:
        print "pointViewer.py"
        sys.exit(-1)
    
    # Einlesen
    print "Dateiname: ", sys.argv[1]
    points = [map(float, x.split()) for x in file(sys.argv[1]).readlines()]
    
    # Bounding Box, verschieben zum Mittelpunkt, skalieren und anpassen an Aufloesung
    deltaValues = calcDeltas(createBoundingBox(points))
    movedPoints = moveBoundingBox(deltaValues, points)
    scaledPoints = scaleBoundingBox(movedPoints)
    print "scaledPoints: ", scaledPoints[:3]
    finalPoints = scaleFrame(scaledPoints)
    print "finalPoints: ", finalPoints[:3]

    # Globale pointList neu setzen
    pointList = finalPoints

    # create main window
    mw = Tk()
    mw._root().wm_title("Point Viewer")

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.pack()
    bFr = Frame(mw)
    bFr.pack(side="left")
    bRotYn = Button(bFr, text="<-", command=rotYn)
    bRotYn.pack(side="left")
    bRotYp = Button(bFr, text="->", command=rotYp)
    bRotYp.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()

    # draw points
    draw()

    # start
    mw.mainloop()