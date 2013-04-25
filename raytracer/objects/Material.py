'''
Created on 25.04.2013

Generative Computergrafik, Uebungsblatt 2, Aufgabe 1
RAYTRACER
Hochschule RheinMain, Medieninformatik

@author: Soeren Kroell
'''

from Color import *

class Material(object):
    '''
    Materialklasse fuer Objekte mit Berechnungen nach Phong-Beleuchtungsmodell
    '''
    GRAY = Color([0.5,0.5,0.5])
    WHITE = Color([1,1,1])
    BLACK = Color([0,0,0])
    AMBIENT = Color([0.3, 0.3, 0.3])
    
    def __init__(self, baseColor, ambientCoefficient=0.8, diffusCoefficient=0.8, specularCoefficient=0.2, glossiness=0.1):
        self.baseColor = baseColor
        self.glossiness = glossiness
        self.ambientCoefficient = ambientCoefficient 
        self.diffusCoefficient = diffusCoefficient
        self.specularCoefficient = specularCoefficient
        self.n = 3
    
    def calcAmbient(self, colorAmbient, c_a):
        '''
        Berechnung ambienter Anteil nach Phong
        @param colorAmbient: Farbe des Objekts
        @param c_a: Umgebungslichtfarbe
        '''
        k_a = colorAmbient * self.ambientCoefficient
        return Color(c_a.vectorMul(k_a))
    
    def calcDiffus(self, colorDiffus, c_in, lightray, normal):
        '''
        Berechnung diffuser Anteil nach Phong
        @param colorDiffus: Farbe des Objekts
        @param c_in: Farbe der Lichtquelle
        @param ligthray: Strahlrichtung zur Lichtquelle
        @param normal: Normalen Vektor des Objekts
        '''
        k_d = colorDiffus * self.diffusCoefficient
        skalar = lightray.dot(normal)
        if skalar >= 0:
            return Color(c_in.vectorMul(k_d) * skalar)
        else:
            return 0
    
    def calcLr(self, lightray, normal):
        '''
        Berechnung LR und Rueckgabe eines Vektors
        @param ligthray: Strahlrichtung zur Lichtquelle
        @param normal: Normalen Vektor des Objekts
        '''
        return (lightray - 2 * (lightray.dot(normal) * normal)) * (-1)
    
    def calcSpecular(self, colorSpecular, c_in, direction, lightray, normal):
        '''
        Berechnung des spekularen Anteils nach Phong
        @param colorSpecular: Farbe des Objekts
        @param c_in: Farbe der Lichtquelle
        @param direction: Richtung des Strahls von der Kamera aus
        @param ligthray: Strahlrichtung zur Lichtquelle
        @param normal: Normalen Vektor des Objekts
        '''
        k_s = colorSpecular * self.specularCoefficient
        lr = self.calcLr(lightray, normal) 
        skalar = lr.dot(direction * (-1))
        if skalar >= 0:
            return c_in.vectorMul(k_s) * lr.dot(direction * (-1)) ** self.n
        else:
            return 0
    
    def calcReflect(self, direction, normal):
        return Color(direction - (2 * direction.cross(normal)).vectorMul(normal))
    
    def calcColor(self, colorObject, c_a, c_in, lightray, normal, direction):
        '''
        Berechnung der Farbe -> ambient + diffus + specular
        @param colorObject: Farbe des Objekts
        @param c_a: Umgebungslicht
        @param c_in: Farbe der Lichtquelle
        @param ligthray: Strahlrichtung zur Lichtquelle
        @param normal: Normalen Vektor des Objekts
        @param direction: Richtung des Strahls von der Kamera aus
        '''
        ambient = self.calcAmbient(colorObject, c_a)
        diffus = self.calcDiffus(colorObject, c_in, lightray, normal)
        spec = self.calcSpecular(colorObject, c_in, direction, lightray, normal)

        if diffus == 0 and spec != 0:
            return Color(ambient + spec)
        
        if spec == 0 and diffus !=0:
            return Color(ambient + diffus)
        
        if spec != 0 and diffus != 0:
            return Color(ambient + diffus + spec)       
        