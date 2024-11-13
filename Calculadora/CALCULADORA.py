import tkinter as tk
from tkinter import END, messagebox, ttk

root = tk.Tk()
root.config(width=300, height=400)
root.title("Calculadora")

# Entrada para mostrar y editar la expresión matemática
entrada = tk.Entry(root, width=16, font=('Arial', 24), borderwidth=2, relief="solid")
entrada.grid(row=0, column=0, columnspan=4)

def agregar_a_entrada(valor):
    entrada.insert(END, valor)

def evaluar():
    try:
        expresion = entrada.get()
        expresion = expresion.replace('x', '*').replace('÷', '/')
        resultado = eval(expresion)
        entrada.delete(0, END)
        entrada.insert(END, str(resultado))
    except:
        messagebox.showerror("Error", "Expresión no válida")

def limpiar():
    entrada.delete(0, END)

# Botones numéricos
numeros = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
    ('0', 4, 1)
]

for (texto, fila, columna) in numeros:
    tk.Button(root, text=texto, command=lambda t=texto: agregar_a_entrada(t), height=2, width=5).grid(row=fila, column=columna)

# Botones de operaciones
operaciones = [
    ('+', 1, 3), ('-', 2, 3),
    ('x', 3, 3), ('÷', 4, 3)
]

for (texto, fila, columna) in operaciones:
    tk.Button(root, text=texto, command=lambda t=texto: agregar_a_entrada(t), height=2, width=5).grid(row=fila, column=columna)

# Botones de funciones adicionales
tk.Button(root, text='C', command=limpiar, height=2, width=5).grid(row=4, column=0)
tk.Button(root, text='=', command=evaluar, height=2, width=5).grid(row=4, column=2)

root.mainloop()
