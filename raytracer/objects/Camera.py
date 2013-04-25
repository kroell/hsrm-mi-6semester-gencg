'''
Created on 25.04.2013

Generative Computergrafik, Uebungsblatt 2, Aufgabe 1
RAYTRACER
Hochschule RheinMain, Medieninformatik

@author: Soeren Kroell
'''

from raytracer.objects import *
from raytracer.PIL import Image

import math 


class Camera(object):
    '''
    Kamera zum Darstellen einer Szene
    '''
    
    __f = Vector([0,0,0])
    __s = Vector([0,0,0])
    __u = Vector([0,0,0])
    __pixelWidth = 0
    __pixelHeight = 0
    
    def __init__(self, up, c, e, fow, aspectRatio, backgroundColor, image, objectlist, light, wRes, hRes):
        '''
        @param up: Vektor nach oben
        @param c: 
        @param e: Position der Kamera
        @param fow: Oeffnungswinkel der Kamera
        @param aspect ratio: Seitenverhaeltnis
        @param backgroundColor: Hintergrundfarbe
        @param image: Image Objekt
        @param objectlist: Liste mit allen Objekten, die von der Kamera angezeigt werden sollen
        @param light: Lichtquelle
        @param wRes: Breite der Aufloesung
        @param hRes: Hoehe der Aufloesung
        @param c_a: Umgebungslichtfarbe
        '''
        self.__up = up
        self.__c = c 
        self.__e = e
        self.__fow = fow
        self.__aspectRatio = aspectRatio
        self.__backgroundColor = backgroundColor
        self.__image = image
        self.__objectlist = objectlist
        self.__light = light
        self.__wRes = wRes
        self.__hRes = hRes
        self.__c_a = Color([0.6,0.6,0.6])
        self.__c_in = self.__light.getColor()
        
        # Kamera initialiseren
        self.initialCamera()
        # Szene rendern
        self.renderScene()
        
    def initialCamera(self):
        '''
        Kamera initialisieren
        '''
        #Extrinsische Kamera erstellen
        self.__f = (self.__c - self.__e) / Vector.norm(self.__c - self.__e)
        self.__s = (self.__f.cross(self.__up)) / Vector.norm(self.__f.cross(self.__up))
        self.__u = (self.__s.cross(self.__f)).scale(-1)
        
        #Intrinsische Kamera erstellen
        alpha = self.__fow / 2.0
        self.__height = 2 * math.tan(alpha)
        self.__width = self.__aspectRatio * self.__height
        self.__pixelWidth = self.__width / (self.__wRes - 1)
        self.__pixelHeight = self.__height / (self.__hRes - 1)
        
        print "Kamera initialisiert!"
        print repr(self)
        
    def calcRay(self,x,y):
        '''
        Gibt einen Strahl, der durch die mitgegebenen Pixel (x,y) geht, zurueck
        '''
        xcomp = self.__s.scale(x * self.__pixelWidth - self.__width / 2)
        ycomp = self.__u.scale(y * self.__pixelHeight - self.__height / 2)
        return Ray(self.__e, self.__f + xcomp + ycomp)
    
    def calcShadow(self, lightRay, object, objectlist):
        '''
        Berechnung der Schatten mit Abhaengigkeit des aktuellen Objekts
        @param lightRay: Strahl vom Objekt-Schnittpunkt in Richtung Lichtquelle
        @param object: Aktuelles Objekt
        @param objectlist: Liste aller Objekte in der Szene
        '''
        for single_object in objectlist:
            hit = single_object.intersectionParameter(lightRay)
            # Schatten Sphere
            if hit > -0.0001 and isinstance(object,Sphere) and object == single_object:
                return True
            # Schatten Plane
            elif hit > 0.0001:
                return True
        # Kein Schatten 
        return False
    
    def calcLightRay(self, origin):
        '''
        Gibt einen Strahl vom Objekt-Schnittpunkt zur Lichtquelle zurueck
        @param origin: Objekt-Schnittpunkt
        '''
        return Ray(origin, self.__light.getPosition() - origin)
    
    def renderScene(self):    
        '''
        Eigentliche Berechnung der Szene. 
        '''
        # fuer jedes x/y der gegebenen Aufloesung
        for x in range(self.__wRes):
            for y in range(self.__hRes):
                ray = self.calcRay(x,y)
                maxdist = float('inf')
                color = self.__backgroundColor
                # Fuer jedes Objekt einzeln pruefen
                for single_object in self.__objectlist:
                    hitdist = single_object.intersectionParameter(ray)
                    if hitdist > 0 and hitdist < maxdist:
                        # BaseColor
                        baseColor = single_object.material.baseColor
                        # Schattierung berechnen
                        point = ray.origin + ray.direction.scale(hitdist)
                        normal = single_object.normalAt(point)  
                        origin = ray.pointAtParameter(hitdist)
                        lightray = self.calcLightRay(origin)
                        
                        if not self.calcShadow(lightray, single_object, self.__objectlist):
                            '''
                            Unschattierter Bereich -> ambient + diffus + spektular Anteil
                            '''
                            color = single_object.material.calcColor(baseColor, self.__c_a, self.__c_in, lightray.direction, normal, ray.direction).colorToRGBTuple()
                        else:
                            '''
                            Schattierter Bereich -> nur ambienter Anteil
                            '''
                            color = single_object.material.calcAmbient(baseColor, self.__c_a).colorToRGBTuple()
 
                        maxdist = hitdist
                # X/Y- und Farbwerte in Bild speichern
                self.__image.putpixel((x,y), color)
    
    def getImage(self):
        '''
        Gibt das erzeugte Image-Objekt zurueck
        '''
        return self.__image
    
    def __repr__(self):
        return 'f:%s, s:%s, u:%s, field of view:%s, aspect ratio:%s' % (repr(self.__f), repr(self.__s), repr(self.__u), repr(self.__fow), repr(self.__aspectRatio))
        