'''
Created on 16.04.2013

@author: soerenkroell
'''

import math,os,sys
from Camera import *
from Tkinter import *
from Canvas import *
from raytracer.objects import *
from raytracer.PIL import Image


# Konstanten definieren
BLACK = (0,0,0)
BLACK2 = (20,20,20)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GREY = (125,125,125)

IMG_WIDTH  = 320.0 # Breite
IMG_HEIGHT = 240.0 # Hoehe
FOW = 45 # Field of View
ASPECT_RATIO = IMG_WIDTH/ IMG_HEIGHT #Seitenverhaeltniss
SPHERE_RADIUS = 2 # Radius der Kugeln


if __name__ == "__main__":
    
    # Image mit Masse 320x240 und schwarzem Hintergrund erstellen
    image = Image.new('RGB', (int(IMG_WIDTH), int(IMG_HEIGHT)), BLACK) 
    
    # Farbverktoren erstellen
    black = Color([0,0,0])
    grey = Color([0.5,0.5,0.5])
    white = Color([1,1,1])
    red = Color([0.8, 0, 0])
    green = Color([0, 0.8, 0])
    blue = Color([0, 0, 0.8])
    
    #Kugeln erstellen
    redSphere = Sphere(Point([2.5, 3, -10]), SPHERE_RADIUS, RED, Material(red))
    greenSphere = Sphere (Point([-2.5, 3, -10]), SPHERE_RADIUS, GREEN, Material(green))
    blueSphere = Sphere(Point([0, 7, -10]), SPHERE_RADIUS, BLUE, Material(blue))
    
    #Ebene erstellen
    greyPlane = Plane(Point([0,0,0]), Vector([0,1,0]), GREY, Material(grey))
               
    # Kamerapositionen erstellen
    up = Vector ([0,1,0])
    e = Point ([0,2,10])
    c = Point ([0,3,0])
    
    # Lichtpunkt
    light = Light(Point([30, 30, 10]), BLACK)
    
    # Ojektliste zur Darstellung in Szene
    #objectlist = [redSphere, blueSphere, greenSphere, greyPlane]
    objectlist = [redSphere, blueSphere, greenSphere,greyPlane]
    
    # Kamera erstellen
    camera = Camera(up, c, e, FOW, ASPECT_RATIO, BLACK, image, objectlist, light)
    
    #finalImage = camera.getImage()
    #finalImage.show()
    #finalImage.save("bild","PNG")