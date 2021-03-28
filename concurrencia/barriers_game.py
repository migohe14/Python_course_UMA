import threading
from random import randint
import numpy as np
import time

class Player(threading.Thread):
    def __init__(self,player, name):
        threading.Thread.__init__(self)
        self.jugador=player 
        self.nombre=name 
        self.numero=0 

    def run(self):
        while(1):
            self.numero=randint(0,100) 
            barrier_director.wait() 
            barrier_players.wait() 
            if(director.num_ganador==self.numero): 
                print("Soy "+self.nombre+" y he ganado con el número: " + str(self.numero))
            else: 
                print("Soy "+self.nombre+" y he perdido con el "+str(self.numero)+", el ganador ha sido el número: "+str(director.num_ganador))
            time.sleep(7) 
            print(" ")

class Director(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.nombre=name 
        self.numeros=list(range(3)) 
        self.num_ganador=-1 
    def run(self):
        while(1):
            barrier_director.wait() 
            self.consigo_los_numeros() 
            self.num_ganador=self.numero_victorioso() # winner
            barrier_players.wait() 
        
    def consigo_los_numeros(self):
        self.numeros[0]=player1.numero
        self.numeros[1]=player2.numero
        self.numeros[2]=player3.numero

    def numero_victorioso(self): 
        if((self.numeros[0]>self.numeros[1])and(self.numeros[0]>self.numeros[2])):
            return self.numeros[0]
        elif((self.numeros[1]>self.numeros[0])and(self.numeros[1]>self.numeros[2])):
            return self.numeros[1]
        else:
            return self.numeros[2]

director=Director("Director")

player1=Player(1,"Bob")
player2=Player(2,"Alice")
player3=Player(3,"John")

barrier_players=threading.Barrier(4) 
barrier_director=threading.Barrier(4)  

player1.start()
player2.start()
player3.start()

director.start()