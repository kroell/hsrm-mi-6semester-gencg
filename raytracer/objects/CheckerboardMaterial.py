'''
Created on 16.04.2013

@author: soerenkroell
'''

from raytracer.objects import Vector
from raytracer.objects import Color



class CheckerboardMaterial(object):
    
    def __init__(self, objectColor):
        self.baseColor = Color([1,1,1])
        self.otherColor = Color([0,0,0])
        self.ambientCoefficient = 1.0 
        self.diffuseCoefficient =  0.6
        self.specularCoefficient = 0.2
        self.checkSize = 1
        self.actColor = objectColor

    def baseColorAt(self, p):
        v = Vector(p)
        v.scale(1.0 / self.checkSize)
        
        if (int(abs(v.x) + 0.5) + int(abs(v.y) + 0.5) + int(abs(v.z) + 0.5)) % 2:
            return self.otherColor
        
        return self.baseColor
    