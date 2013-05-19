'''
Created on 17.05.2013

@author: soerenkroell
'''


import OpenGL
OpenGL.ERROR_CHECKING = False
from OpenGL.GL import *
from OpenGL.GLU import *

import sys,math

def initGL(width, height):
    glClearColor(0.0,0.0,1.0,0.0)
    glMatrixMode(GL_PROJECTION)