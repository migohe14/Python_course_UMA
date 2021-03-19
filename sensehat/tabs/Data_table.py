import tkinter as tk
from tkinter import ttk

class Data_table(ttk.Frame):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.label = ttk.Label(self)
        self.label["text"] = ("Control")
        self.label.pack()
        
        self.web_button = ttk.Button(self, text="Comenzar")
        self.web_button.pack(pady=10)

        self.tree = ttk.Treeview(self)
        self.tree.pack()

        # https://tkdocs.com/tutorial/tree.html
        self.tree['columns'] = ('valor', 'fecha', 'tipo')

        # self.tree.column('size', width=100, anchor='center')
        self.tree.heading('#1', text='#Num')
        self.tree.heading('valor', text='Valor')
        self.tree.heading('fecha', text='Fecha/Hora')
        self.tree.heading('tipo', text='Tipo')

        # Treeview chooses the id:
        for x in range(1,20):
            self.tree.insert('', 'end', text=''+str(x), values=('primer valor','segundo valor','tercer valor'))
