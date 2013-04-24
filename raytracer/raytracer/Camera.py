'''
Created on 16.04.2013

@author: soerenkroell
'''

from raytracer.objects import *
from raytracer.PIL import Image

import sys

class Camera(object):
    '''
    Kamera zum Darstellen einer Szene
    '''
    
    __f = Vector([0,0,0])
    __s = Vector([0,0,0])
    __u = Vector([0,0,0])
    __wRes = 320
    __hRes = 240
    __pixelWidth = 0
    __pixelHeight = 0
    
    def __init__(self, up, c, e, fow, aspectRatio, backgroundColor, image, objectlist, light):
        '''
        @param up: wo ist oben
        @param c: 
        @param e: Position der Kamera
        @param fow: Oeffnungswinkel der Kamera
        @param aspect ratio: Seitenverhaeltnis
        @param backgroundColor: Hintergrundfarbe
        @param image: Image Objekt
        @param objectlist: Liste mit allen Objekten, die von der Kamera angezeigt werden sollen
        @param light: Lichtquelle
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
        Wird ein Strahl von einem Objekt geschnitten wird true zurueck gegeben, ansonsten false.
        @param lightRay: Strahl vom Objekt-Schnittpunkt in Richtung Lichtquelle
        '''
        for single_object in objectlist:
            hit = single_object.intersectionParameter(lightRay)
            # Schatten Sphere
            if hit > -0.0001 and isinstance(object,Sphere) and object == single_object:
                return True
            # Schatten Plane
            elif hit > 0.0001:
                return True
                
        return False
    
    def calcLightRay(self, origin):
        '''
        gibt einen Strahl vom Objekt-Schnittpunkt zur Lichtquelle zurueck
        @param origin: Objekt-Schnittpunkt
        '''
        return Ray(origin, self.__light.getPosition() - origin)
    
    def calcColor(self,rayDirection, single_object, point, normal, lightray):
        color = single_object.material.baseColorAt(point)
        
        if not self.calcShadow(lightray):
            color += single_object.material.renderColor(lightray, normal, self.__light.color, rayDirection)
        
        return color

    def renderColor(self):
        pass
        
    def renderScene(self):    
        '''
        Ray Casting Algorithmus
        '''
        # fuer jedes x/y
        for x in range(self.__wRes):
            for y in range(self.__hRes):
                ray = self.calcRay(x,y)
                maxdist = float('inf')
                color = self.__backgroundColor
                for single_object in self.__objectlist:
                    hitdist = single_object.intersectionParameter(ray)
                    if hitdist > 0 and hitdist < maxdist:
                        point = ray.origin + ray.direction.scale(hitdist)
                        normal = single_object.normalAt(point)  
                        # Schattierung berechnen
                        origin = ray.pointAtParameter(hitdist)
                        lightray = self.calcLightRay(origin)
                        #color = single_object.material.baseColorAt(point)
                        if not self.calcShadow(lightray, single_object, self.__objectlist):
                            #color += single_object.material.renderColor(lightray, normal, ray.direction)
                            #color = single_object.color()
                            #print single_object.material.baseColor
                            color = single_object.material.baseColor.colorToRGBTuple()    
                                               
                        else:
                            print "bla"
                            '''try:
                                colornew = single_object.material.calcAmbient(single_object.material.baseColor)
                                color = colornew.colorToRGBTuple()
                            except Exception, err:
                                sys.stderr.write('ERROR: %s\n' % str(err))'''
                                    
                            color = self.__light.getColor()
                        maxdist = hitdist
                self.__image.putpixel((x,y), color)
        self.__image.show()
        self.__image.save("raytracer","PNG")
    
        
    def getF(self):
        return self.__f
    
    def getS(self):
        return self.__s
    
    def getU(self):
        return self.__u
    
    def getRay(self):
        return self.__ray
    
    def getImage(self):
        return Image(self.__image)
    
    def __repr__(self):
        return 'f:%s, s:%s, u:%s, field of view:%s, aspect ratio:%s' % (repr(self.__f), repr(self.__s), repr(self.__u), repr(self.__fow), repr(self.__aspectRatio))
        