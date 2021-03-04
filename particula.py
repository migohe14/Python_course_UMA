from random import random, seed
from math import sqrt
import numpy as np

Masa = 20
G = 6.67259e-11

class Particula:
    __cuantas = 0
    def __init__(self):
        self.pos= np.array([0.0,0.0,0.0])
        self.vel= np.array([0.0,0.0,0.0])
        self.acc= np.array([0.0,0.0,0.0])
        self.id = Particula.__cuantas
        Particula.__cuantas += 1
 
    def setValores(self, pPos, pVel,pAcc):
        self.pos= pPos   
        self.vel= pVel
        self.acc= pAcc
    
    def initRandom(self):
        self.setValores(np.array([random(), random(), random() ]), np.array([random(), random(), random()]),
          np.array( [random(), random(), random()])),    

    def muestra(self):
        print("Partícula ", self.id)
        print("   La posición es: ", self.pos)
        print("   La velocidad es: ", self.vel)
        print("   La acc es: ", self.acc)
        pass

    def distancia(self, otra): 
        delta=self.pos - otra.pos
        res = sqrt (delta[0] ** 2 + delta[1] ** 2 + delta[2] **2)
        return res
    
    def actualizaVelocidadYPosicion (self, tstep):
        self.vel += self.acc * float(tstep)
        self.pos += self.vel * float(tstep)