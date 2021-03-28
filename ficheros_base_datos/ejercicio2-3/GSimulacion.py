from particulaMasa import *
from random import random, seed
from math import sqrt
from matplotlib.figure import Figure
import time
from mpl_toolkits import mplot3d
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
from pymongo import MongoClient
import pymongo

pausa = 0.02

class GSimulacion(threading.Thread):
        
    def __init__(self, NumParticulas, tiempoTot, ventana):
        threading.Thread.__init__(self)
        self.ventana = ventana
        self.N = NumParticulas
        self.tiempoTot = tiempoTot
        self.particulas = []

        cliente = MongoClient()
        self.db=cliente.ParticulasDB

        for _ in range(0,self.N):
            self.particulas.append(ParticulaMasa())
            particula=self.db.Iniciales.find_one({"id":i},{"_id":0})


            pos=np.array(particula["pos"])
            vel=np.array(particula["vel"])
            acc=np.array(particula["acc"])
            masa=particula["masa"]
            
            self.particulas[i].set_valores(pos,vel,acc,masa)
        # self.initPos()  
        # self.initVel() 
        # self.initMasa()
        
        self.deltat = 0.1
        self.tiempo =0.0
        self.preparaGrafico()
        self.refrescaParticulas() 

    # def initPos(self):
    #     """
    #         Iniciliza las 3 primeras posiciones a valores fijos y el resto aleatorios
    #     """
        
    #     self.particulas[0].pos=np.array([0.,0.,0.])
    #     self.particulas[1].pos=np.array([1,1,0.])
    #     self.particulas[2].pos=np.array([1.2,0.25,0.])
    #     seed()
    #     for i in range(3,self.N):
    #         self.particulas[i].pos =np.array([random()*2-1,random()*2-1,random()*2-1])

    # def initVel(self):
    #     """
    #         Iniciliza las 3 primeras velocidades a valores fijos y el resto aleatorios
    #     """

    #     self.particulas[0].vel=np.array([0.,0.,0.])
    #     self.particulas[1].vel=np.array([0,0.5,0.])
    #     self.particulas[2].vel=np.array([0,0.5,0.])
    #     seed()
    #     for i in range(3,self.N):
    #         self.particulas[i].vel =np.array([0.,0.5,0.])

    # def initMasa(self):
    #     """
    #         Iniciliza la primera masa a 1.0e10 (grande) y el resto a 1.0e5 
    #     """
    #     self.particulas[0].masa = 1.0e10
    #     for i in range(1,self.N):
    #         self.particulas[i].masa = 1.0e5

    def preparaGrafico(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111,projection='3d')

        self.ax.set_xlim(-2.5,2.5)
        self.ax.set_ylim(-2.5,2.5)
        self.ax.set_zlim(-2.5,2.5)

        self.grafico = self.ax.scatter([],[],[],c='r',marker='o')
        self.graph = FigureCanvasTkAgg(self.fig, master=self.ventana)
        self.graph.get_tk_widget().grid(column=0, row=2) 



    def refrescaParticulas(self):
       
        self.grafico.remove() #Limpia el gráfico para mostrar las posiciones nuevas
        col=['g']   # La primera verde y el resto rojas
        for _ in range (1,self.N):
            col.append('r')
        x,y,z = self.vectoriza()    
        self.grafico = self.ax.scatter(x,y,z,c=col,marker='o')
        self.fig.canvas.draw()

    def printParticulas(self):
        for i in range(0,self.N):
            self.particulas[i].muestra()

    def cabecera(self):
        print ("Inicio de la simulación")

    def vectoriza(self):
        x=[]
        y=[]
        z=[]
        for i in range(0,self.N):
            x.append(self.particulas[i].pos[0])
            y.append(self.particulas[i].pos[1])
            z.append(self.particulas[i].pos[2])

        return x,y,z

    def pasoSimulacion(self):
         for k in range(self.N):
                self.particulas[k].muestra()
                self.db.Valores.insert_one({"id":k, "pos":self.particulas[k].pos.tolist(), "vel":self.particulas[k].vel.tolist(), "acc":self.particulas[k].acc.tolist(), "masa": self.particulas[k].masa, "tiempo":i})
            i+=self.deltaT          

    def start_(self):
        self.cabecera()
        
        while self.tiempo <= self.tiempoTot: 
            # print ("Timepo:", self.tiempo)
            self.printParticulas()
            self.pasoSimulacion()
            self.refrescaParticulas()
            self.tiempo += self.deltat
 
        print ("Fin particulas")

    def start_embedded(self):
        self.cabecera()
        self.ventana.after(int(self.deltat*1000),self.refresca)

    def refresca(self):        
        if self.tiempo <= self.tiempoTot:
            print('paso: '+str(self.tiempo)+' '+str(self.tiempoTot)) 
            self.ventana.after(int(self.deltat*1000),self.refresca)
            self.printParticulas()
            self.pasoSimulacion()
            self.refrescaParticulas()
            self.tiempo += self.deltat

    def run(self):
        self.cabecera()
        
        while self.tiempo <= self.tiempoTot: 
            self.printParticulas()
            self.pasoSimulacion()
            self.ventana.after_idle(self.refrescaParticulas)
            self.tiempo += self.deltat
 
        print ("Fin particulas")
