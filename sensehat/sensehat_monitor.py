import tkinter as tk
from tkinter import ttk
from tabs.Data_table import *
from tabs.Chart import *

class Application(ttk.Frame):
    
    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("Práctica GUI Sensehat")
        main_window.geometry("900x600")
        
        self.notebook = ttk.Notebook(self)
        
        self.greeting_frame = Data_table(self.notebook)
        self.notebook.add(
            self.greeting_frame, text="Monitorización", padding=10)
        
        self.about_frame = Chart(self.notebook)
        self.notebook.add(
            self.about_frame, text="Gráfica", padding=10)
        
        self.notebook.pack(padx=10, pady=10)
        self.pack()

main_window = tk.Tk()
app = Application(main_window)
app.mainloop()