'''
Created on May 23, 2013

@author: soerenkroell
'''

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import sys, math

animate = False
angle = 0

def initGL(width, height):
    #Set background color
    glClearColor(0.0,0.0,1.0,0.0)
    #Enable clearing of the depth buffer
    glEnable(GL_DEPTH_TEST)
    #Set perspektive Transform
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Camera
    gluPerspective(45., float(width)/height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def display():
    # Clear framebuffer and depth buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Reset modelview matrix
    glLoadIdentity()
    
    #### Anzeige von 2 rotierenden kannen
    
    # Save Matrix
    glPushMatrix()
    # Move
    glTranslate(0.0,0.7,-4.0)
    # Rotate around y-axis
    glRotate(angle, 0.0, 1.0, 0.0)
    # Set glutWireTeapot
    glutWireTeapot(.5)
    # prevent stack overflow or underflow
    glPopMatrix()
    #Move
    glTranslate(0.0,-0.7,-4.0)
    # Rotate around y-Axis
    glRotate(-angle, 1.0,0.0,0.0)
    # Set glutWireTeapot
    glutWireTeapot(.5)
    # Swap buffers
    glutSwapBuffers()
    
    ###
    
    #Move down the z-axis
    glTranslate(0.0,0.0,-4.0)
    #Set glutWireTeapot
    glutWireTeapot(1.0)
    # Swap double buffer buffers
    glutSwapBuffers()

def keyPressed(key, x, y):
    global animate
    if key == 'a':
        animate = True
    glutPostRedisplay()

def animation():
    global angle
    if animate:
        angle = (angle+1)%360
        glutPostRedisplay()

def resizeViewport(width, height):
    if height == 0:
        height = 1
    
    # Reset current viewport
    glViewport(0,0,width,height)
    #Reset perspective transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0,float(width)/ height, 0.1,100.0)
    # Activate model view matrix
    glMatrixMode(GL_MODELVIEW)
    # Swap double buffer buffers
    glutSwapBuffers()
     

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize (500,500)
    glutCreateWindow("Beispiel GLUT Primitive")
    # Register display callback function
    glutDisplayFunc(display)
    # Register reshape callback function
    glutReshapeFunc(resizeViewport)
    # Register keyboad callback function
    glutKeyboardFunc(keyPressed)
    # Register Idle Callback
    glutIdleFunc(animation)
    # Init OpenGL context
    initGL(500,500)
    # Start GLUT mainloop
    glutMainLoop()
    
if __name__ == '__main__':
    main()