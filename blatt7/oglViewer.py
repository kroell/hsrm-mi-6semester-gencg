'''
Created on May 23, 2013
Finished on May 30, 2013

Generative Computergrafik, Uebungsblatt 7, Aufgabe 1
Bewertete Abgabe
Hochschule RheinMain, Medieninformatik

Start des Programms mit:
- python object.obj [wire|solid]

Standardwerte:
- Objektdarstellung als wire 
- Intrinsische Kamera auf orthographische Projektion

Folgende Features sind enthalten:
- Aendern der Hintergrundfarbe mit 'b'
- Aendern der Vordergrundfabre mit 'f'
- Objekt rotieren mit linker Muastaste
- Objekt zoom mit mittlerer Maustaste
- Objekt verschieben mit rechter Maustaste
- Umstellen der intrinsischen Kamera auf orthographische Projektion mit 'o'
- Umstellen der intrinsischen Kamera auf perspektivische Projektion mit 'p'

Zusatzfeature:
- Objekt solid und beleuchtet darstellen, dazu wie folgt starten
  python object.obj solid
  
  Die Objektfarbe kann dann jedoch nicht mehr geandert werden!


@author: Soeren Kroell
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
solidMode = False
wireMode = True
orthoMode = True
perspectiveMode = False

actOri = 1
axis = [1,1,1]
angle = 10
newPosition = [0,0,0]

zPosCamera =0.0

frontColorIndex,backColorIndex = 2,1
rotateX, rotateY, rotateZ = 0, 0, 0
WIDTH, HEIGHT = 500, 500

aspect = WIDTH/HEIGHT
fov = 60
near = 0.1
far = 30.0

rotateX, rotateY, rotateZ = 0, 0, 0

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
    OpenGL initialize
    '''
    global solidMode
    
    #Set background color - black
    glClearColor(colorList[0][0],colorList[0][1],colorList[0][2],colorList[0][3])
    
    if solidMode:
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)

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
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            doRotation = True
            startP = projectOnSphere(x,y,r)
        if state == GLUT_UP:
            doRotation = False
            actOri = actOri * rotate(angle,axis)
            angle = 0
            
    # translate object
    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            doTranslation = True
        if state == GLUT_UP:
            doTranslation = False
        
    # zoom object
    if button == GLUT_MIDDLE_BUTTON:
        if state == GLUT_DOWN:
            doZoom = True
        if state == GLUT_UP:
            doZoom = False

def mouseMotion(x,y):
    ''' 
    handle mouse motion
    '''
    global angle, axis, scaleFactor, doZoom, doRotation, doTranslation, center, newPosition
    
    # rotate by mouse
    if doRotation:
        r = min(WIDTH, HEIGHT) / 2.0
        moveP = projectOnSphere(x, y, r)
        #math domain error
        angle = math.acos(numpy.dot(startP,moveP))
        axis = numpy.cross(startP, moveP)
        glutPostRedisplay()
    
    # zoom  
    if doZoom:
        r = min(WIDTH, HEIGHT) / 2.0
        moveP = projectOnSphere(x, y, r)
        x,y,z = [i for i in moveP]
        # differenz anfangspunkt zu endpunkt
        zoomFactor = y/100
        print "zoomFactor: ", zoomFactor
        if zoomFactor >= 0.0001 and zoomFactor <= 0.01:
            scaleFactor= zoomFactor
            glutPostRedisplay()
    
    # translatation
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
        
    print "Used File: ", sys.argv[1]
    objFile = sys.argv[1]
    
    objectVertices = [] 
    objectNormals = []
    objectFaces =[] 
    data = []
    objectFaces2 = []
    
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
                if not objectNormals:
                    objectFaces2.append(map(float,first))
                for face in first:
                    objectFaces.append(map(float,face.split('//')))
    
    print "objFaces: ",objectFaces[:10]
    print "objFaces2: ",objectFaces2[:10]
    
    for face in objectFaces:
        if len(face) == 2:
            face.insert(1, 0.0)

    # Create BoundingBox
    boundingBox = [map(min, zip(*objectVertices)), map(max, zip(*objectVertices))]
    # Calc center of bounding box
    center = [(x[0]+x[1])/2.0 for x in zip(*boundingBox)]
    # Calc scale factor
    scaleFactor = 2.0/max([(x[1]-x[0]) for x in zip(*boundingBox)])
    
    if objectNormals:
        for vertex in objectFaces:
            vn = int(vertex[0])-1
            nn = int(vertex[2])-1
            data.append(objectVertices[vn] + objectNormals[nn])
    else:
        for vertex in objectFaces2:
            point = []
            for x in vertex:
                vn = int(x)-1
                point.append(objectVertices[vn])
            data.append(point)
            
    print "verticies: ", objectVertices[:10]
    print "data: ",data[:10]
    
    my_vbo = vbo.VBO(array(data,'f'))
        

def display():
    '''
    Render objects
    '''
    global scaleFactor, center, my_vbo, actOri, angle, axis, data, newPosition, wireMode, orthoMode, perspectiveMode

    # Clear framebuffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # view as ortho Projection
    if orthoMode:
        #switch to projection matrix
        glMatrixMode(GL_PROJECTION)
        #set to 1
        glLoadIdentity()
        # Camera, multiply with new p-matrix
        gluOrtho2D(-1.5, 1.5, -1.5, 1.5)
        #switch to modelview matrix
        glMatrixMode(GL_MODELVIEW)
    
    # view as perspective Projection
    if perspectiveMode:
        #switch to projection matrix
        glMatrixMode(GL_PROJECTION)
        #set to 1
        glLoadIdentity()
        #change perspective mode
        gluPerspective(fov, aspect, near, far)
        #set Camera
        gluLookAt (0,0,2,0,0,0,0,1,0)
        #switch to modelview matrix
        glMatrixMode(GL_MODELVIEW)
    
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
    
    # Rotate by key
    glRotate(rotateX, 1, 0, 0)
    glRotate(rotateY, 0, 1, 0)
    glRotate(rotateZ, 0, 0, 1)
    
    # Rotate by mouse
    glMultMatrixf(actOri*rotate(angle,axis))
    
    # Scale
    glScale(scaleFactor, scaleFactor, scaleFactor)
    
    # move to center
    glTranslate(-center[0], -center[1], -center[2])
    
    # show object as wires
    if wireMode:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    
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
    global colorList, frontColorIndex, backColorIndex, angle, rotateX, rotateY, rotateZ, perspectiveMode, orthoMode

    # If escape is pressed, kill everything.
    if key == '\x1b':
        sys.exit()

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

    # Rotate with keys x,X,y,Y,z,Z
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
    
    # Activate Orthogonal-Projection
    if key == 'o':
        if perspectiveMode:
            orthoMode = True
            perspectiveMode =False
            
    # Activate Perspective-Projection
    if key == 'p':
        if orthoMode:
            orthoMode = False
            perspectiveMode =True

    glutPostRedisplay()


def resizeViewport(width, height):
    '''
    Adjust projection matrix to window size
    '''
    if height == 0:
        height = 1
        
    glViewport(0, 0, width, height)
    #change to projection matrix
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    if width <= height:
        glOrtho(-1.5, 1.5, -1.5*height/width, 1.5*height/width, -1.0, 1.0)
    else:
        glOrtho(-1.5*width/height, 1.5*width/height,-1.5, 1.5,-1.0, 1.0)
        
    #change to modelview matrix
    glMatrixMode(GL_MODELVIEW)
    
    #swap buffer
    glutSwapBuffers()   


def reshape(width, height):
    """ adjust projection matrix to window size"""
    #global windowWidth, windowHeight
    
    if height == 0:
        height = 1
        
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    if orthoMode:
        
        if width <= height:
            glOrtho(-1.5, 1.5, -1.5*height/width, 1.5*height/width, -1.0, 1.0)
        else:
            glOrtho(-1.5*width/height, 1.5*width/height,-1.5, 1.5,-1.0, 1.0)
        
    else:
        if width <= height:
            glViewport(0, (height - width) / 2, width, width)
            gluPerspective(60.0, 1, 0.1, 100.0)
        else:
            glViewport((width - height) / 2, 0, height, height)
            gluPerspective(60.0, 1.0, 0.1, 100.0)
            
    glMatrixMode(GL_MODELVIEW)


def main():
    '''
    Fenster initialisieren, File einlesen, BoundingBox erstellen/zentrieren/skalieren
    '''
    
    global solidMode, wireMode
    
    # Wenn solid oder wire beim Start mitgegeben wurde, den entsprechenden Modus aktivieren
    if len(sys.argv) == 3:
        if sys.argv[2] == "solid":
            solidMode = True
            wireMode = False
        if sys.argv[2] == "wire":
            wireMode = True
            solidMode = False
    
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize (500,500)
    glutCreateWindow("OpenGL obj Viewer")
    # Register display callback function
    glutDisplayFunc(display)
    # Register reshape callback function
    glutReshapeFunc(reshape)
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