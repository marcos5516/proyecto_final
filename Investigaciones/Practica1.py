import tkinter as tk
from tkinter import END, messagebox, ttk

root = tk.Tk()
root.config(width=300,height=400)
root.title("Practica 1")
ttk.Label(root,text="Ingrese nombre").place(x=10,y=20)
txNombre=tk.Entry(root, width=15)
txNombre.place(x=10, y=50)

def mostrarNombre():
    nombre=txNombre.get()
    messagebox.showinfo(message="Hola "+nombre, title="Resultado")
    
btMostrar=tk.Button(root,text="Mostrar", command=mostrarNombre)
btMostrar.place(x=10,y=80)
root.mainloop()
    
