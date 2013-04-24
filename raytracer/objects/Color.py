'''
Created on 20.04.2013

@author: soerenkroell
'''

from raytracer.objects import *


class Color(Vector):
    '''
    Vektor welcher die Farbbereiche repraensentiert. 
    Anstelle von 0 - 255 gehen die Werte von 0 bis 1. 
    0 = Schwarz und 1 = Weiss
    '''
    
    __colorVector = [0,0,0]
    
    def __init__(self, colorVector):
        self.__colorVector = Vector.__init__(self, colorVector)
        #for i in range(len(colorVector)):
         #   if colorVector[i] >= 0 and colorVector[i] <= 1:
          #      self.__colorVector = colorVector
           # else:
            #    print "Werte duerfen nur zwischen 0 und 1 liegen" 
            
    def colorToRGBTuple(self):
        '''
        wandelt den Color-Vector in ein Tupel mit RGB Werten um und gibt dieses Tupel zurueck
        '''
        return tuple([255 if x > 255 else int(255 * x) for x in self])
    
    def __repr__(self):
        return "Color-Vector: [{0}, {1}, {2}]".format(*self.__colorVector)
