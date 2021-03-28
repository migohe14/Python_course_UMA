import tkinter as tk
from tkinter import ttk
from GSimulacion import *

class Aplicacion:

    def __init__(self):
        self.ventana1=tk.Tk()
        self.ventana1.title("Simulación Particulas")

        self.gui_datos()
        self.ventana1.mainloop()


    def gui_datos(self):
        self.labelframe1=ttk.LabelFrame(self.ventana1, text="Datos Simulación:")        
        self.labelframe1.grid(column=0, row=0)        

        self.label1=ttk.Label(self.labelframe1, text="Número partículas:")
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        
        self.datoTemp=tk.StringVar(value='3')
        self.entryTemp=ttk.Entry(self.labelframe1,textvariable=self.datoTemp)
        self.entryTemp.grid(column=1, row=0, padx=4, pady=4)
        
        self.label2=ttk.Label(self.labelframe1, text="Tiempo total:")        
        self.label2.grid(column=0, row=1, padx=4, pady=4)

        self.datoTiempoTotal=tk.StringVar(value='20')
        self.entry2=ttk.Entry(self.labelframe1,textvariable=self.datoTiempoTotal)
        self.entry2.grid(column=1, row=1, padx=4, pady=4)

        self.labelframe2=ttk.Frame(self.ventana1)        
        self.labelframe2.grid(column=0, row=1)        
        self.boton=tk.Button(self.labelframe2,text="Comenzar",command=self.comenzar_simulacion)
        self.boton.grid(column=0,row=0)



    def comenzar_simulacion(self):
        NumeroParticulas=3
        TiempoTotal=20
        gsim = GSimulacion(NumeroParticulas,TiempoTotal,self.ventana1).start()


aplicacion1=Aplicacion()

