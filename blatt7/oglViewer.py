'''
Created on May 23, 2013

Generative Computergrafik, Uebungsblatt 6, Aufgabe 4
Hochschule RheinMain, Medieninformatik

@author: soerenkroell
'''

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo

import sys, numpy, math

angle = 10
i = 0

WIDTH, HEIGHT = 500, 500

# color definitions
black = (0.0,0.0,0.0,0.0)
white = (1.0,1.0,1.0,1.0)
blue = (0.0,0.0,1.0,0.0)
green = (0.0,1.0,0.0,0.0)
yellow = (1.0,1.0,0.0,0.0)
red = (1.0,0.0,0.0,0.0)

colorList = [white, black, red, yellow, green, blue]
colorFlag = True


def initGL(width, height):
    '''
    OpenGL initialisieren
    '''
    #Set background color
    #blue
    glClearColor(colorList[2][0],colorList[2][1],colorList[2][2],colorList[2][3])
    #switch to projection matrix
    glMatrixMode(GL_PROJECTION)
    #set to 1
    glLoadIdentity()
    # Camera, multiply with new p-matrix
    glOrtho(-1.5, 1.5, -1.5, 1.5, -1.0, 1.0)
    #switch to modelview matrix
    glMatrixMode(GL_MODELVIEW)



def display():
    '''
    Objekte rendern
    '''
    global scale, center, points, vbo, colorList, colorFlag, i
    
    # Clear framebuffer
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Render Color
    
    if i < len(colorList):
        if colorFlag:
            #white
            glColor(colorList[i][0],colorList[i][1],colorList[i][2])
            i += 1
        else:
            #black
            glColor(colorList[i][0],colorList[i][1],colorList[i][2])
            i += 1
    else:
        i = 0
    
    # Reset modelview matrix
    glLoadIdentity()
    # Rotate
    glRotate(rotateX, 1, 0, 0)
    glRotate(rotateY, 0, 1, 0)
    glRotate(rotateZ, 0, 0, 1)
    # Scale
    glScale(scale, scale, scale)
    # move to center
    glTranslatef(-center[0], -center[1], -center[2])
    # load points
    vbo.bind()
    glVertexPointerf(vbo)
    glEnableClientState(GL_VERTEX_ARRAY)
    glDrawArrays(GL_POINTS, 0, len(points))
    vbo.unbind()
    glDisableClientState(GL_VERTEX_ARRAY)
    #swap buffer
    glutSwapBuffers()            


def keyPressed(key, x, y):
    '''
    Drehungen mittels Tasen x,X, y,Y und z,Z
    '''
    global rotateX, rotateY, rotateZ, colorList, colorFlag
    
    angle = 10

    if key == 'x': 
        rotateX = rotateX + angle
    if key == 'X':
        rotateX = rotateX - angle
    if key == 'y': 
        rotateY = rotateY + angle
    if key == 'Y':
        rotateY = rotateY - angle
    if key == 'z': 
        rotateZ = rotateZ + angle
    if key == 'Z':
        rotateZ = rotateZ - angle
        
    # Hintergrundfarbe aendern
    if key == 'b':
        glClearColor(black[0],black[1],black[2],black[3])

    if key == 'f':
        glutPostRedisplay()
        if colorFlag:
            colorFlag = False
        else:
            colorFlag = True

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


#### ROTIERUNG MIT MOUSE
def projectOnSphere(x,y,r):
    x,y = x - WIDTH / 2.0, HEIGHT/ 2.0 -y
    a = min(r*r, x**2 + y**2)
    z = math.sqrt(r*r - a)
    l = math.sqrt(x**2 + y**2 + z**2)
    return x/l, y/l, z/l

def mouse(button, state, x, y):
    """ handle mouse events """
    
    global startP, actOri, angle, doRotation, axis
    
    r = min(WIDTH, HEIGHT)/2.0
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            doRotation = True
            startP = projectOnSphere(x,y,r)
        if state == GLUT_UP:
            doRotation = False
            actOri = actOri * rotate(angle,axis)
            angle = 0

def mouseMotion(x,y):
    """ handle mouse motion """
    print "mouse motion at ", x, y

def rotate(angle,axis):
    pass

#### ENDE ROTIERUNG MIT MOUSE

def main():
    '''
    Fenster initialisieren, File einlesen, BoundingBox erstellen/zentrieren/skalieren
    '''
    global scale, center, points, vbo, rotateX, rotateY, rotateZ
    
    rotateX, rotateY, rotateZ = 0, 0, 0
    
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

    #check parameters
    if len(sys.argv) == 1:
        print "oglViewer.py"
        sys.exit(-1)
    
    # File einlesen
    print "Verwendetes File: ", sys.argv[1]
    points = [map(float, x.split())+[1.0] for x in file(sys.argv[1]).readlines()]
    
    # bounding box in Schwani Manier
    boundingBox = [map(min, zip(*points)), map(max, zip(*points))]
    
    # calc center of bounding box
    center = [(x[0]+x[1])/2.0 for x in zip(*boundingBox)]
    
    #calc scale factor
    scale = 2.0/max([(x[1]-x[0]) for x in zip(*boundingBox)])
    
    vbo = vbo.VBO(numpy.array(points, 'f'))
    
    # Init OpenGL context
    initGL(500,500)
    # Start GLUT mainloop
    glutMainLoop()
    
    
if __name__ == '__main__':
    main()