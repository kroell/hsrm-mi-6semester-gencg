'''
Created on May 23, 2013
Finished on May 30, 2013

Generative Computergrafik, Uebungsblatt 7, Aufgabe 1
Bewertete Abgabe
Hochschule RheinMain, Medieninformatik

Folgende Features sind enthalten:
- Aendern der Hintergrundfarbe mit 'b'
- Aendern der Vordergrundfabre mit 'f'
- Objekt rotieren mit linker Muastaste
- Objekt zoom mit rechter Maustaste

Zusatzfeature:
- obj einlesen und beleuchtet darstellen


@author: soerenkroell
'''

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo
from numpy import array

import numpy, math

my_vbo = None

doZoom = False
doRotation = False
doTranslation = False

actOri = 1
axis = [1,1,1]
angle = 10
newPosition = [0,0,0]

frontColorIndex,backColorIndex = 2,1
rotateX, rotateY, rotateZ = 0, 0, 0
WIDTH, HEIGHT = 500, 500

# color definitions
black = (0.0,0.0,0.0,0.0)
white = (1.0,1.0,1.0,1.0)
blue = (0.0,0.0,1.0,0.0)
green = (0.0,1.0,0.0,0.0)
yellow = (1.0,1.0,0.0,0.0)
red = (1.0,0.0,0.0,0.0)

colorList = [black, white, red, green, blue, yellow]

def initGL(width, height):
    '''
    OpenGL initialisieren
    '''
    #Set background color - black
    glClearColor(colorList[0][0],colorList[0][1],colorList[0][2],colorList[0][3])
    '''
    color
    '''
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    #glShadeModel(GL_FLAT)
    
    #switch to projection matrix
    glMatrixMode(GL_PROJECTION)
    #set to 1
    glLoadIdentity()
    # Camera, multiply with new p-matrix
    gluOrtho2D(-1.5, 1.5, -1.5, 1.5)
    #switch to modelview matrix
    glMatrixMode(GL_MODELVIEW)


def projectOnSphere(x,y,r):
    '''
    '''
    x,y = x - WIDTH / 2.0, HEIGHT/ 2.0 -y
    a = min(r*r, x**2 + y**2)
    z = math.sqrt(r*r - a)
    l = math.sqrt(x**2 + y**2 + z**2)
    return x/l, y/l, z/l


def mouse(button, state, x, y):
    '''
    handle mouse events
    '''
    global startP, actOri, angle, doRotation, axis, doZoom, doRotation, doTranslation
    r = min(WIDTH, HEIGHT) / 2.0
    # rotate object
    if button == GLUT_MIDDLE_BUTTON:
        if state == GLUT_DOWN:
            doRotation = True
            startP = projectOnSphere(x,y,r)
        if state == GLUT_UP:
            doRotation = False
            actOri = actOri * rotate(angle,axis)
            angle = 0
            
    # translate object
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            doTranslation = True
        if state == GLUT_UP:
            doTranslation = False
        
    # zoom object
    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            doZoom = True
        if state == GLUT_UP:
            doZoom = False

def mouseMotion(x,y):
    ''' 
    handle mouse motion
    '''
    global angle, axis, scaleFactor, doZoom, doRotation, doTranslation, center, newPosition
    
    # Roation durchfuehren bei Mausbewegung
    if doRotation:
        r = min(WIDTH, HEIGHT) / 2.0
        moveP = projectOnSphere(x, y, r)
        #math domain error
        angle = math.acos(numpy.dot(startP,moveP))
        axis = numpy.cross(startP, moveP)
        glutPostRedisplay()
    
    # Zoom durchfuehren bei Mausbewegung  
    if doZoom:
        r = min(WIDTH, HEIGHT) / 2.0
        moveP = projectOnSphere(x, y, r)
        x,y,z = [i for i in moveP]
        zoomFactor = y/100
        if zoomFactor >= 0.0001 and zoomFactor <= 0.01:
            scaleFactor= zoomFactor
            glutPostRedisplay()
    
    # Verschiebung durchfuehren bei Mausbewegung
    if doTranslation:
        r = min(WIDTH, HEIGHT) / 2.0
        moveP = projectOnSphere(x, y, r)
        x,y,z = [i for i in moveP]
        newPosition = [x,y,z]
        glutPostRedisplay()
    
        
def rotate(angle,axis):
    '''
    rotate object
    '''
    c, mc = math.cos(angle), 1-math.cos(angle)
    s = math.sin(angle)
    l = math.sqrt(numpy.dot(numpy.array(axis), numpy.array(axis)))
    if l != 0:
        x,y,z = numpy.array(axis)/l
        r = numpy.matrix([
                         [x*x*mc+c, x*y*mc-z*s, x*z*mc+y*s, 0],
                         [x*y*mc+z*s, y*y*mc+c, y*z*mc-x*s, 0],
                         [x*z*mc-y*s, y*z*mc+x*s, z*z*mc+c, 0],
                         [0,0,0,1]
                         ])
    return r.transpose()
        

def initGeometryFromObjFile():
    '''
    load obj File, init Bounding Box, init Faces
    '''
    global my_vbo, scaleFactor, center, data
    
    #check parameters
    if len(sys.argv) == 1:
        print "python oglViewer.py object.obj"
        sys.exit(-1)
        
    print "Verwendetes File: ", sys.argv[1]
    objFile = sys.argv[1]
    
    objectVertices = [] 
    objectNormals = []
    objectFaces =[] 
    data = []
    
    for lines in file(objFile):
        # wenn nicht leer
        if lines.split():
            check = lines.split()[0]
            if check == 'v':
                objectVertices.append(map(float,lines.split()[1:]))
            if check == 'vn':
                objectNormals.append(map(float,lines.split()[1:]))
            if check == 'f':
                first = lines.split()[1:]
                for face in first:
                    objectFaces.append(map(float,face.split('//')))
    
    for face in objectFaces:
        # wenn vt fehlt um 0 erweitern
        if len(face) == 2:
            face.insert(1, 0.0)
        # wenn vt und vn fehlt um 0 erweitern
        if len(face) == 1:
            face.insert(1, 0.0)
            face.insert(2, 0.0)

    # Create BoundingBox
    boundingBox = [map(min, zip(*objectVertices)), map(max, zip(*objectVertices))]
    # Calc center of bounding box
    center = [(x[0]+x[1])/2.0 for x in zip(*boundingBox)]
    # Calc scale factor
    scaleFactor = 2.0/max([(x[1]-x[0]) for x in zip(*boundingBox)])
        
    for vertex in objectFaces:
        vn = int(vertex[0])-1
        nn = int(vertex[2])-1

        if objectNormals:
            data.append(objectVertices[vn] + objectNormals[nn])
        else:
            data.append(objectVertices[vn])

    my_vbo = vbo.VBO(array(data,'f'))
        

def display():
    '''
    Render objects
    '''
    global scaleFactor, center, my_vbo, actOri, angle, axis, data, newPosition
    
    # Clear framebuffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # render vertox buffer object
    my_vbo.bind()
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    
    glVertexPointer(3, GL_FLOAT, 24 , my_vbo)
    glNormalPointer(GL_FLOAT, 24 , my_vbo + 12)

    # Reset modelview matrix
    glLoadIdentity()

    # Translate
    glTranslate(newPosition[0],newPosition[1],0)
    
    # Rotate
    glMultMatrixf(actOri*rotate(angle,axis))
    
    # Scale
    glScale(scaleFactor, scaleFactor, scaleFactor)
    # move to center
    glTranslate(-center[0], -center[1], -center[2])
    
    # Draw VBO as Triangles
    glDrawArrays(GL_TRIANGLES, 0, len(data))

    my_vbo.unbind()
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)
    
    #swap buffer
    glutSwapBuffers()            


def keyPressed(key, x, y):
    '''
    Hintergrundfarbe mit b und Objektfarbe mit f wechseln
    '''
    global colorList, frontColorIndex, backColorIndex, angle

    # Change background color
    if key == 'b':
        if backColorIndex < len(colorList):
            glClearColor(colorList[backColorIndex][0],colorList[backColorIndex][1],colorList[backColorIndex][2],colorList[backColorIndex][3])
            backColorIndex += 1      
        else:
            backColorIndex = 1
            glClearColor(colorList[0][0],colorList[0][1],colorList[0][2],colorList[0][3])
        
    # Change foreground color / object color
    if key == 'f':
        if frontColorIndex < len(colorList):
            glColor(colorList[frontColorIndex][0],colorList[frontColorIndex][1],colorList[frontColorIndex][2])
            frontColorIndex += 1
        else:
            frontColorIndex = 1
            glColor(colorList[0][0],colorList[0][1],colorList[0][2])

    glutPostRedisplay()


def resizeViewport(width, height):
    '''
    Anpassen des Viewports an Fenster
    '''
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if width <= height:
        glOrtho(-1.5, 1.5,-1.5*height/width, 1.5*height/width,-1.0, 1.0)
    else:
        glOrtho(-1.5*width/height, 1.5*width/height,-1.5, 1.5,-1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)


def main():
    '''
    Fenster initialisieren, File einlesen, BoundingBox erstellen/zentrieren/skalieren
    '''
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize (500,500)
    glutCreateWindow("OpenGL obj Viewer")
    # Register display callback function
    glutDisplayFunc(display)
    # Register reshape callback function
    glutReshapeFunc(resizeViewport)
    # Register keyboad callback function
    glutKeyboardFunc(keyPressed)
    #register mouse function
    glutMouseFunc(mouse)         
    #register motion function
    glutMotionFunc(mouseMotion)  
    
    initGeometryFromObjFile()
    
    # Init OpenGL context
    initGL(500,500)
    
    # Start even processing
    glutMainLoop()
    
    
if __name__ == '__main__':
    main()