import oglFixme
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys, math, os, numpy, math

EXIT = -1
FIRST = 0
WIDTH = 500
HEIGHT = 500

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
    "LookAtMatrix mittels KameraVektoren erstellen und zurueckgeben"
    s,e,u,f = cameraVectors
    a = -dot(s,e)
    b = -dot(u,e)
    c = dot(f,e)
    return numpy.matrix([ [s[0],s[1],s[2],a] , [u[0],u[1],u[2],b] , [-f[0],-f[1],-f[2],c] , [0,0,0,1] ])

def useLookAtMatrix(lookAtMatrix, p):
    "LookAtMatrix auf mitgegebenem Punkt anwenden"
    pointAsMatrix = numpy.matrix([[p[0]],[p[1]],[p[2]],[p[3]]])
    return lookAtMatrix * pointAsMatrix

def createTransformMatrix():
    "Tansformationsmatrix erstllen und zurueckgeben"
    global WIDTH
    global HEIGHT
    
    f = 6
    n = 2
    
    aspect = WIDTH / HEIGHT
    alpha = math.pi * 30 / 180

    cot = ((math.cos(alpha))/(math.sin(alpha)))/aspect
    
    temp3 = f+n
    temp5 = f*n
    temp1 = (-temp3) / (f-n)
    temp2 = (-2*(f*n)) / (f-n)
    
    return numpy.matrix( [ 
                          [ cot,0,0,0 ] , 
                          [ 0,cot,0,0 ] , 
                          [ 0,0,temp1,temp2 ] , 
                          [ 0,0,-1,0 ] 
                          ] )

def useTrafoMatrix(trafoMatrix, p):
    pointAsMatrix = numpy.matrix(p)
    
    ret = (trafoMatrix * pointAsMatrix).tolist()
    return [ret[0][0], ret[1][0], ret[2][0], ret[3][0]]


def dividePerspective(transformedPoints):
    return [ [x[0]/x[3], x[1]/x[3] , x[2]/x[3] , x[3]/x[3]] for x in transformedPoints ]

# ------------- END ----------

# ------------- BEGIN VECTOR FUNCTIONS ----------
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

# ------------- END ----------

# ------------- BEGIN BOUNDING BOX ----------

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

# ------------- END ----------

# ------------- BEGIN OPEN GL ----------
def init(width, height):
    """ Initialize an OpenGL window """
    glClearColor(0.0, 0.0, 0.0, 0.0)         #background color
    glMatrixMode(GL_PROJECTION)              #switch to projection matrix
    glLoadIdentity()                         #set to 1
    glOrtho(-1.5, 1.5, -1.5, 1.5, -1.0, 1.0) #multiply with new p-matrix
    glMatrixMode(GL_MODELVIEW)               #switch to modelview matrix


def display():
    """ Render all objects"""
    glClear(GL_COLOR_BUFFER_BIT) #clear screen
    glColor(0.0, 0.0, 1.0)       #render stuff
    glRectf(-1.0 ,-1.0 ,1.0, 1.0)
    glutSwapBuffers()            #swap buffer


def reshape(width, height):
    """ adjust projection matrix to window size"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if width <= height:
        glOrtho(-1.5, 1.5, -1.5*height/width, 1.5*height/width,-1.0, 1.0)
    else:
        glOrtho(-1.5*width/height, 1.5*width/height,-1.5, 1.5,-1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)


def keyPressed(key, x, y):
    """ handle keypress events """
    if key == chr(27): # chr(27) = ESCAPE
        sys.exit()


def mouse(button, state, x, y):
    """ handle mouse events """
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        print "left mouse button pressed at ", x, y


def mouseMotion(x,y):
    """ handle mouse motion """
    print "mouse motion at ", x, y


def menu_func(value):
    """ handle menue selection """
    print "menue entry ", value, "choosen..."
    if value == EXIT:
        sys.exit()
    glutPostRedisplay()

def createMenu():
    menu = glutCreateMenu(processMenuEvents)
    glutAddMenuEntry("One", 1)
    glutAddMenuEntry("Two", 2)
    glutAttachMenu(GLUT_RIGHT_BUTTON)

def processMenuEvents(option):
    logging.debug("Menu pressed")


def main():
    # Hack for Mac OS X
    cwd = os.getcwd()
    glutInit(sys.argv)
    os.chdir(cwd)
    
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutCreateWindow("simple openGL/GLUT template")

    glutDisplayFunc(display)     #register display function
    glutReshapeFunc(reshape)     #register reshape function
    glutKeyboardFunc(keyPressed) #register keyboard function 
    glutMouseFunc(mouse)         #register mouse function
    glutMotionFunc(mouseMotion)  #register motion function
    #glutCreateMenu(menu_func)    #register menue function

    glutAddMenuEntry("First Entry",FIRST) #Add a menu entry
    glutAddMenuEntry("EXIT",EXIT)         #Add another menu entry
    glutAttachMenu(GLUT_RIGHT_BUTTON)     #Attach mouse button to menue

    init(500,500) #initialize OpenGL state

    glutMainLoop() #start even processing

# ------------- END ----------



if __name__ == "__main__":
    
    # File einlesen
    print "Dateiname: ", sys.argv[1]
    points = [map(float, x.split())+[1.0] for x in file(sys.argv[1]).readlines()]
    
    # Kameravektoren, LookAtMatrix und Transformationsmatrix erstellen
    cameraVectors = createCamera()
    lookAtMatrix = createLookAtMatrix(cameraVectors)
    trafoMatrix = createTransformMatrix()
    
    # Bounding Box, verschieben zum Mittelpunkt, skalieren und anpassen an Aufloesung
    deltaValues = calcDeltas(createBoundingBox(points))
    movedPoints = moveBoundingBox(deltaValues, points)
    scaledPoints = scaleBoundingBox(movedPoints)
    
    # Homogene Komponente zu skalierten Punkten hinzufuegen
    pointList = [p+[1.0] for p in scaledPoints ]
    
    main()