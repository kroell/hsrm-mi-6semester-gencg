'''
Created on 20.04.2013

@author: soerenkroell
'''

from raytracer.objects import Point

class Light(object):
    '''Lichtklasse'''
    
    def __init__(self, position, color, ):
        self.__position = position #Point
        self.color = color
    
    def getPosition(self):
        return Point(self.__position)
    
    def getColor(self):
        return self.color
    