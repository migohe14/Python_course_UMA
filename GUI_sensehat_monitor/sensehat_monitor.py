import threading
import tkinter as tk
import pathlib
import csv

import tkinter

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

from tkinter import ttk, messagebox
from sense_emu import SenseHat
from time import sleep
from datetime import datetime
from os import sep
from copy import deepcopy
from random import choice

from plot_settings import Plot_settings
    
    

class Monitor():

    def __init__(self, window):
        self.dimensions = '800x600'
        self.style_button = {
            'comenzar': {
                'bg': '#00b200',
                'fg': 'black',
                'relief': 'flat',
                'text': 'Comenzar',
            },
            'parar': {
                'bg': '#e50000',
                'fg': 'black',
                'relief': 'flat',
                'text': 'Parar',
            } 
        }
        self.medida_selected = tk.IntVar(value=1)
        self.add_in_list = tk.IntVar(value=0)
        self.period_default = 1000
        self.counter = 1
        self.data_store = []
        self.abortar = True
        self.temp = 0.0
        self.pres = 0.0
        self.humd = 0.0
        self.x = []
        self.y = []

        self.window = window
        self.emulator = sense

        self.data_config_plot = Plot_settings()
        
        self.sizer()
        self.title_window()
        self.main_menu()
        self.tabs()

        self.bucle()
        
    
    def bucle(self):
        self.window.after(self.period_default, self.process_queue)

    def process_queue(self):
        if not self.abortar:
            modo_listar = self.add_in_list.get()
            self.get_values_from_emu()
            if modo_listar == 1:
                sensor = self.medida_selected.get()
                self.register_in_tree(sensor)
            elif modo_listar == 0:
                self.register_in_entry()
  
        self.window.after(self.period_default, self.process_queue)

    def sizer(self):
        self.window.geometry(self.dimensions)

    def title_window(self):
        self.window.title('Práctica GUI SenseHat')
    
    def main_menu(self):
        opciones_list = tk.Menu()
        opciones_list.add_command(label='Propiedades', command=self.options)

        root_menu = tk.Menu()
        root_menu.add_cascade(label='Opciones', menu=opciones_list)
        self.window.config(menu=root_menu)

    def options(self):
        self.win_option = tk.Toplevel()
        self.win_option.title('Editor de opciones')
        self.win_option.geometry('300x150')

        tk.Label(self.win_option, text='Período: ').grid(row=0, column=0, padx=25, pady=20)
        periodo = tk.Entry(self.win_option)
        periodo.grid(row=0, column=1)

        tk.Button(self.win_option, text='Guardar', command=lambda: self.config_periodo(periodo.get())).grid(row=1, column=0, padx=20, sticky=tk.W)
    
    def config_periodo(self, value):
        operation_valid = False
        try:
            num = int(value)
            operation_valid = True
            self.marcador['text'] = str(value)
            self.period_default = num
                
        except ValueError as e:
            messagebox.showerror(title='Error datos introducidos', message='Debe introducir un valor numérico - digitos(0-9)')
            print(e)
        
        if operation_valid:
            self.win_option.destroy()

    def tabs(self):
        notebook = ttk.Notebook(self.window)
        sheet1 = ttk.Frame(notebook)
        sheet2 = ttk.Frame(notebook)
        notebook.add(sheet1, text='Monitorizacion')
        notebook.add(sheet2, text='Gráfica')
        self.containter_widgets_monitorizacion(sheet1)
        self.container_widgets_grafica(sheet2)
        notebook.pack(fill='both', expand='yes')

    def containter_widgets_monitorizacion(self, win_reference):
        self.frame_control(win_reference)
        self.frame_medidas(win_reference)
        self.frame_historico(win_reference)

    def container_widgets_grafica(self, win_reference):
        
        self.sensor_selected = str(self.medida_selected.get())
        self.config = self.data_config_plot.tags_canvas()

        valor_sensor = self.measure()
        
        self.x.append(self.current_time())
        self.y.append(valor_sensor[self.sensor_selected])

        fig = Figure(facecolor=Plot_settings.FACECOLOR)

        axs = fig.add_subplot(Plot_settings.SUBPLOT)    
        axs.grid(True)
        self.ax = axs

        self.lines = axs.plot([], [], **self.data_config_plot.get_style_sensor(self.sensor_selected))[0]

        axs.set_title(self.config[self.sensor_selected][Plot_settings.TITLE])
        axs.set_xlabel(Plot_settings.LABEL_X)
        axs.set_ylabel(self.config[self.sensor_selected][Plot_settings.LABEL])

        self.canvas = FigureCanvasTkAgg(fig, master=win_reference)
        self.canvas.get_tk_widget().place(**self.data_config_plot.dimensions_canvas())
        self.canvas.draw()

        toolbar = NavigationToolbar2Tk(self.canvas, win_reference)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        self.window.after(self.period_default, self.show_values)
        
    def measure(self):
        return {
            "1": self.temp,
            "2": self.pres,
            "3": self.humd
        }

    def show_values(self):
        sensor = str(self.medida_selected.get())
        
        self.lines = self.ax.plot(self.x, self.y, **self.data_config_plot.get_style_sensor(sensor))[0]
        
        valor_sensor = self.measure()

        self.ax.set_title(self.config[sensor][Plot_settings.TITLE])
        self.ax.set_ylabel(self.config[sensor][Plot_settings.LABEL])
 
        self.ax.set_xlim(left=self.current_time()-5, right=self.current_time())
        self.ax.set_ylim(top=valor_sensor[sensor]+1, bottom=valor_sensor[sensor]-1)

        for label in self.ax.xaxis.get_ticklabels():
            label.set_rotation(Plot_settings.ROTATION_X)
        
        self.check_size_list()
        
        self.lines.set_xdata(self.x)
        self.lines.set_ydata(self.y)

        self.canvas.draw()
        
        self.window.after(self.period_default, self.show_values)

    def check_size_list(self):
        self.x = self.define_total_items_list(self.x, Plot_settings.TIME)
        self.y = self.define_total_items_list(self.y, Plot_settings.SENSOR)

    def define_total_items_list(self, my_list, tipo):
        sensor = str(self.medida_selected.get())
        valor_sensor = self.measure()

        if len(my_list) < 10:
            if tipo == Plot_settings.TIME:
                my_list.append(self.current_time())
            else:
                my_list.append(valor_sensor[sensor])
        else:
            del my_list[0]
            if tipo == Plot_settings.TIME:
                my_list.append(self.current_time())
            else:
                my_list.append(valor_sensor[sensor])

        return my_list

    def current_time(self):
        now = datetime.now()
        time_string = now.strftime("%M%S")
        return int(time_string)

    def frame_control(self, window):
        frame = tk.LabelFrame(window, text='Control')
        frame.grid(row=0, column=1, columnspan=6, padx=140, pady=20)

        self.action_app = tk.Button(frame, **self.style_button['comenzar'], command=self.action_button)
        self.action_app.grid(row=1, columnspan=6)
    
        tk.Label(frame, text='Período: ').grid(row=2, column=0)
        self.marcador = tk.Label(frame, text='1000')
        self.marcador.grid(row=2, column=1)

    def action_button(self):
        state_button = self.state_button()
        self.abortar = False if state_button == 'Comenzar' else True

        if state_button == 'Comenzar':
            self.action_app.config(self.style_button['parar'])
        elif state_button == 'Parar':
            self.action_app.config(self.style_button['comenzar'])

    def state_button(self):
        return self.action_app.config('text')[-1]

    def get_values_from_emu(self):
        self.temp = self.emulator.temperature
        self.pres = self.emulator.pressure
        self.humd = self.emulator.humidity

    def register_in_tree(self, option):
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        register = {
            'id': self.counter,
            'datetime': date_time,
        }

        if option == 1:
            register['tipo'] = 'Temperatura'
            register['valor'] = self.temp
            self.tree.insert('', 'end', text=self.counter, values=(self.temp, date_time, 'Temperatura'))
        elif option == 2:
            register['tipo'] = 'Presión'
            register['valor'] = self.pres
            self.tree.insert('', 'end', text=self.counter, values=(self.pres, date_time, 'Presión'))
        elif option == 3:
            register['tipo'] = 'Humedad'
            register['valor'] = self.humd
            self.tree.insert('', 'end', text=self.counter, values=(self.humd, date_time, 'Humedad'))
        
        self.data_store.append(register)
        self.counter +=1

    def register_in_entry(self):
        option = self.medida_selected.get()
        self.medida.delete(0,tk.END)

        if option == 1:
            self.medida.insert(0, self.temp)
        elif option == 2:
            self.medida.insert(0, self.pres)
        elif option == 3:
            self.medida.insert(0, self.humd)

    def frame_medidas(self, window):
        frame = tk.LabelFrame(window, text='Medidas')
        frame.grid(row=1, column=0, columnspan=9, pady=10)

        self.medida = tk.Entry(frame, justify=tk.CENTER)
        self.medida.grid(row=2, column=0, columnspan=4)
        temp = tk.Radiobutton(frame, text='Temperartura', variable=self.medida_selected, value=1)
        temp.grid(row=3, column=0)
        pres = tk.Radiobutton(frame, text='Presión', variable=self.medida_selected, value=2)
        pres.grid(row=3, column=1)
        humd = tk.Radiobutton(frame, text='Humedad', variable=self.medida_selected, value=3)
        humd.grid(row=3, column=2)

    def frame_historico(self, win_reference):
        frame = tk.LabelFrame(win_reference, text='Historico')
        frame.grid(row=4, column=0, columnspan=8, pady=10)

        self.tree = ttk.Treeview(frame, height=13, columns=4)
        self.tree.grid(row=4, column=0, columnspan=3)
        self.tree["columns"] = ('Valor', 'DateTime', 'Tipo')
        self.tree.heading('#0', text='#Num', anchor=tk.CENTER)
        self.tree.heading('Valor', text='Valor', anchor=tk.CENTER)
        self.tree.heading('DateTime', text='Fecha/Hora', anchor=tk.CENTER)
        self.tree.heading('Tipo', text='Tipo', anchor=tk.CENTER)

        self.action_limpiar = tk.Button(frame, text='Limpiar', command=self.reset_table)
        self.action_limpiar.grid(row=5, column=0, sticky=tk.W + tk.E)
        self.action_media = tk.Button(frame, text='Calcular Media', command=self.show_average)
        self.action_media.grid(row=5, column=1, sticky=tk.W + tk.E)
        self.action_exportar = tk.Button(frame, text='Exportar', command=self.export_list)
        self.action_exportar.grid(row=5, column=2, sticky=tk.W + tk.E)

        action_list = tk.Checkbutton(frame, text='Añadir a lista', variable=self.add_in_list)
        action_list.grid(row=6, column=0, columnspan=4)

    def reset_table(self):
        records = self.tree.get_children()

        for element in records:
            self.tree.delete(element)

        self.counter = 1
        self.data_store = []

    def show_average(self):
        copied_data = self.clone_data()
        if len(copied_data) == 0:
            msg = 'No hay datos para calcular la MEDIA. Por favor haga check en <Añadir a lista> y pulse el botón COMENZAR'
            messagebox.showinfo(message=msg, title="Datos no encontrados")
        else:
            totalTemp = 0
            contadorTemp = 0
            totalHumd = 0
            contadorHumd = 0
            totalPres = 0
            contadorPres = 0
            for data in copied_data:
                if data['tipo'] == 'Temperatura':
                    totalTemp += data['valor']
                    contadorTemp += 1
                if data['tipo'] == 'Presión':
                    totalPres += data['valor']
                    contadorPres += 1
                if data['tipo'] == 'Humedad':
                    totalHumd += data['valor']
                    contadorHumd += 1

            mediaTemp = totalTemp / contadorTemp if contadorTemp else 0.0
            mediaPres = totalPres / contadorPres if contadorPres else 0.0
            mediaHumd = totalHumd / contadorHumd if contadorHumd else 0.0

            msg = 'La media de los sensores son:  TEMP: {}                 PRES: {}       HUMD: {}'.format(mediaTemp, mediaPres, mediaHumd)
            messagebox.showinfo(message=msg, title='Media Sensores')
            
    def clone_data(self):
        return deepcopy(self.data_store)

    def export_list(self):
        current_path = str(pathlib.Path().absolute()) + sep
        now = datetime.now()
        name_file_csv = now.strftime("%Y%m%d_%H%M%S")
        extension = '.csv'
        file_path = current_path + 'monitoring_' + name_file_csv + extension

        copy_store = deepcopy(self.data_store)
        if len(copy_store) == 0:
            msg = 'No hay datos para listar. Por favor activar registro de datos en lista. Haga check en <Añadir a lista> y pulse el botón COMENZAR'
            messagebox.showinfo(message=msg, title="Datos no encontrados")
        else:
            msg = '¿Desea generar un fichero en formato CSV?'
            selecciona = messagebox.askokcancel(message=msg, title="Crear fichero CSV")
            if selecciona:
                with open(file_path, 'w', newline='') as fh:
                    fieldnames = ['id', 'valor', 'datetime', 'tipo']
                    thewritter = csv.DictWriter(fh, fieldnames=fieldnames)
                    thewritter.writeheader()
                    for dato in copy_store:
                        thewritter.writerow(dato)
        




if __name__ == '__main__':
    window = tk.Tk()
    sense = SenseHat()
    application = Monitor(window)
    window.mainloop()