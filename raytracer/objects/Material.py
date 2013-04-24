'''
Created on 20.04.2013

@author: soerenkroell
'''

from Color import *
import math

class Material(object):
    GRAY = Color([0.5,0.5,0.5])
    WHITE = Color([1,1,1])
    BLACK = Color([0,0,0])
    AMBIENT = Color([0.3, 0.3, 0.3])
    
    def __init__(self, baseColor, ambientCoefficient=0.45, glossiness=0.1):
        self.baseColor = baseColor
        self.glossiness = glossiness
        self.ambientCoefficient = ambientCoefficient 
    
    def calcAmbient(self, colorAmbient):
        '''
        Ambienter Anteil berechnen
        '''
        #print colorAmbient
        return Color(colorAmbient * self.ambientCoefficient)
        
        
        '''
        self.ambientColor = ambientColor if ambientColor else self.AMBIENT
        self.diffuseColor = diffuseColor if diffuseColor else self.ambientColor
        self.specularColor = specularColor if specularColor else Color([glossiness, glossiness, glossiness])
        
        self.glossiness = glossiness
        self.n = 64 * glossiness + 1 
        self.specConst = (self.n + 2) / (math.pi * 2)
        
        self.specularBase = self.specularColor * self.specConst
    
    def baseColorAt(self, point):
        return self.ambientColor * self.AMBIENT
    
    def renderColor(self, lightRay, normal, rayDirection):
        lightColor = Color([1,1,1])
        color = self.BLACK
        
        diffuseFactor = lightRay.direction.dot(normal)
    
        if diffuseFactor > 0:
            print self.diffuseColor
            print lightColor
            color += self.diffuseColor * lightColor * diffuseFactor
            reflectedLight = (lightRay.direction).reflect(normal)
            specularFactor = reflectedLight.dot(-rayDirection)
            
            if specularFactor > 0:
                color += self.specularBase * lightColor * (specularFactor**self.n)
                
        return color
    '''
    