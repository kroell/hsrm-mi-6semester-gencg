from Tkinter import *
from Canvas import *
import sys
import math
import numpy

WIDTH  = 400 # width of canvas
HEIGHT = 400 # height of canvas
FOW = 60

HPSIZE = 1 # double of point size (must be integer)
COLOR = "#ff6cbb" # blue

ALPHA = 10 * math.pi / 180 # Winkel fuer Drehung

pointList = [] # list of points

def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    """ draw points """
    for item in can.find_all():
        can.delete(item)
    for point in scaleFrame(pointList):
        x,y = point
        can.create_oval(x-HPSIZE, y-HPSIZE, x+HPSIZE, y+HPSIZE, fill=COLOR, outline=COLOR)


def rotYp():
    """ rotate counterclockwise around y axis """    
    global ALPHA
    global pointList
    
    #cameraVectors = createCamera()
    #lookAtMatrix = createLookAtMatrix(cameraVectors)
    #trafoMatrix = createTransformMatrix()
    
    #transformedPoints = []
    #for i in pointList:
    #    transformedPoints.append(useTrafoMatrix(trafoMatrix, useLookAtMatrix(lookAtMatrix,i)))
    
    #fp = dividePerspective(pointList)
    #pointList = rotateMatrix(ALPHA, fp)
    print "bla"
    draw()


def rotYn():
    """ rotate clockwise around y axis """
    global ALPHA
    global pointList
 
    rotMatrix = createRotateMatrix(-ALPHA)

    rotatedPoints = [useRotateMatrix(rotMatrix, p) for p in pointList ]
    transformedPoints = [useTrafoMatrix(trafoMatrix, useLookAtMatrix(lookAtMatrix,p)) for p in rotatedPoints]

    pointList = dividePerspective(transformedPoints)
    
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
    return [[x[0] * WIDTH/2.0 + WIDTH/2,HEIGHT - (x[1] * HEIGHT/2.0 + HEIGHT/2.0)] for x in scaledPoints]


def rotateMatrix(alpha,scaledPoints):
    "Matrix zum Rotieren"
    return [[math.cos(alpha)*p[0] - math.sin(alpha)*p[2], p[1], math.sin(alpha) * p[0]+math.cos(alpha) * p[2] ] for p in scaledPoints]

def createRotateMatrix(alpha):
    rotMatrix = numpy.matrix([ 
                              [math.cos(alpha), 0, -math.sin(alpha), 0 ] , 
                              [0, 1, 0, 0] , 
                              [ -math.sin(alpha), 0, math.cos(alpha), 0 ] ,
                              [0, 0, 0, 1] 
                              ])
    return rotMatrix

def useRotateMatrix(rotMatrix,p):
    "Rotieren mittels einer 4*4 Matrix"    
    pointAsMatrix = numpy.matrix([[p[0]],[p[1]],[p[2]],[p[3]]])
    ret = (rotMatrix * pointAsMatrix).tolist()

    return [ret[0][0], ret[1][0], ret[2][0], ret[3][0]]


# ------------- BEGIN ----------
#
# VECTOR FUNCTIONS
def norm(v):
    'Norm des Vektors berechnen -> passt'
    return math.sqrt(sum(math.pow(v[i],2)for i in range(len(v))))

def sub(v, vector):
    'Zwei Vektoren subtrahieren'
    return [v[i] - vector[i] for i in range(len(v))]
    
def div(v, scalar):
    'Division Vektor durch Skalar'
    return [v[i] / scalar for i in range (len(v))]

def cross(v, vector):
    'Kreuzprodukt zweier Vektoren im 3-dimensionalen Raum'
    v_e = [0,0,0]
    v_e[0] = v[1] * vector[2] - v[2] * vector[1]
    v_e[1] = v[2] * vector[0] - v[0] * vector[2]
    v_e[2] = v[0] * vector[1] - v[1] * vector[0]
    return v_e

def mul(v, scalar):
    return [scalar * v[i] for i in range (len(v))]

def dot(v, vector):
    'Skalarprodukt -> Vektor * Vektor = Wert'
    return float(sum(v[i] * vector[i] for i in range (len(v))))
#
# ------------- END ----------

# ------------- Pipeline ----------
def createCamera():
    'Kameravektoren berechnen'
    c = [0,0,0]
    up = [0,1,0]
    e = [0,0,2]
    
    # calc up'
    up_ = div(up,norm(up))
    
    # calc f
    f_temp = sub(c,e)
    f = div(f_temp,norm(f_temp))
    
    # calc s
    s_temp = cross(f, up_)
    s = div(s_temp,norm(s_temp))
    
    # calc u
    u = cross(s,f)
    
    return s,e,u,f 
    
def createLookAtMatrix(cameraVectors):
    s,e,u,f = cameraVectors
    a = -dot(s,e)
    b = -dot(u,e)
    c = dot(f,e)
    return numpy.matrix([ [s[0],s[1],s[2],a] , [u[0],u[1],u[2],b] , [-f[0],-f[1],-f[2],c] , [0,0,0,1] ])

def useLookAtMatrix(lookAtMatrix, p):
    pointAsMatrix = numpy.matrix([[p[0]],[p[1]],[p[2]],[p[3]]])
    return lookAtMatrix * pointAsMatrix

def createTransformMatrix():
    global WIDTH
    global HEIGHT
    
    f = 6
    n = 2
    
    aspect = WIDTH / HEIGHT
    alpha = math.pi * 30 / 180

    cot = ((math.cos(alpha))/(math.sin(alpha)))/aspect
    
    temp3 = f+n
    temp4 = f-n
    temp5 = f*n
    temp1 = (-temp3) /temp4
    temp2 = (-2*temp5) / temp4
    
    return numpy.matrix( [ [ cot,0,0,0 ] , [ 0,cot,0,0 ] , [ 0,0,temp1,temp2 ] , [ 0,0,-1,0 ] ] )

def useTrafoMatrix(trafoMatrix, p):
    pointAsMatrix = numpy.matrix(p)
    
    ret = (trafoMatrix * pointAsMatrix).tolist()
    return [ret[0][0], ret[1][0], ret[2][0], ret[3][0]]


def dividePerspective(transformedPoints):
    return [ [x[0]/x[3], x[1]/x[3] , x[2]/x[3] , x[3]/x[3]] for x in transformedPoints ]

# ------------- END ----------


if __name__ == "__main__":
    #check parameters
    if len(sys.argv) == 1:
        print "pointViewer.py"
        sys.exit(-1)
    
    # Einlesen
    print "Dateiname: ", sys.argv[1]
    points = [map(float, x.split())+[1.0] for x in file(sys.argv[1]).readlines()]
    
    cameraVectors = createCamera()
    lookAtMatrix = createLookAtMatrix(cameraVectors)
    trafoMatrix = createTransformMatrix()
    
    # Bounding Box, verschieben zum Mittelpunkt, skalieren und anpassen an Aufloesung
    deltaValues = calcDeltas(createBoundingBox(points))
    movedPoints = moveBoundingBox(deltaValues, points)
    scaledPoints = scaleBoundingBox(movedPoints)
   
    transformedPoints = []
   
    for i in scaledPoints:
        # Homogene Komponente hinzufuegen
        i.append(1.0)
        transformedPoints.append(useTrafoMatrix(trafoMatrix, useLookAtMatrix(lookAtMatrix,i)))

    finalPoints = dividePerspective(transformedPoints)
    
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