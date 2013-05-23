'''
Created on May 23, 2013

Generative Computergrafik, Uebungsblatt 6, Aufgabe 4
Hochschule RheinMain, Medieninformatik

@author: soerenkroell
'''

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo

import sys, numpy


def initGL(width, height):
    '''
    OpenGL initialisieren
    '''
    #Set background color
    glClearColor(0.0,0.0,1.0,0.0)
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
    global scale, center, points, vbo
    # Clear framebuffer
    glClear(GL_COLOR_BUFFER_BIT)
    # Render Color
    glColor(1.0, 1.0, 1.0)
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
    global rotateX, rotateY, rotateZ
    
    angle = 20

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
    global scale, center, points, vbo, rotateX, rotateY, rotateZ
    
    rotateX, rotateY, rotateZ = 0, 0, 0
    
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize (500,500)
    glutCreateWindow("OpenGL Viewer")
    # Register display callback function
    glutDisplayFunc(display)
    # Register reshape callback function
    glutReshapeFunc(resizeViewport)
    # Register keyboad callback function
    glutKeyboardFunc(keyPressed)

    #check parameters
    if len(sys.argv) == 1:
        print "oglViewer.py"
        sys.exit(-1)
    
    # File einlesen
    print "Dateiname: ", sys.argv[1]
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