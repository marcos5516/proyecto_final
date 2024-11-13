import tkinter as tk
from tkinter import END, messagebox
import math

root = tk.Tk()
root.config(width=300, height=400, bg='#4d3c36')
root.title("Calculadora Científica")

# Entrada para mostrar y editar la expresión matemática
entrada = tk.Entry(root, width=16, font=('Arial', 24), borderwidth=2, relief="solid")
entrada.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

# Función para agregar texto a la entrada
def agregar_a_entrada(valor):
    entrada.insert(END, valor)

# Función para evaluar la expresión
def evaluar():
    try:
        expresion = entrada.get()
        # Reemplazar símbolos personalizados por operaciones válidas de Python
        expresion = expresion.replace('X', '*').replace('÷', '/').replace('^', '**')
        resultado = eval(expresion)
        entrada.delete(0, END)
        entrada.insert(END, str(resultado))
    except:
        messagebox.showerror("Error", "Expresión no válida")

# Función para calcular la raíz cuadrada
def raiz_cuadrada():
    try:
        expresion = entrada.get()
        resultado = eval(expresion) ** 0.5
        entrada.delete(0, END)
        entrada.insert(END, str(resultado))
    except:
        messagebox.showerror("Error", "Expresión no válida")

# Función para calcular el factorial
def factorial():
    try:
        expresion = entrada.get()
        resultado = math.factorial(int(eval(expresion)))
        entrada.delete(0, END)
        entrada.insert(END, str(resultado))
    except:
        messagebox.showerror("Error", "Expresión no válida")

# Función para calcular porcentajes
def porcentaje():
    try:
        expresion = entrada.get()
        resultado = eval(expresion) / 100
        entrada.delete(0, END)
        entrada.insert(END, str(resultado))
    except:
        messagebox.showerror("Error", "Expresión no válida")

# Función para calcular valores absolutos
def absoluto():
    try:
        expresion = entrada.get()
        resultado = abs(eval(expresion))
        entrada.delete(0, END)
        entrada.insert(END, str(resultado))
    except:
        messagebox.showerror("Error", "Expresión no válida")

# Función para limpiar la entrada
def limpiar():
    entrada.delete(0, END)

# Función para borrar el último carácter de la entrada
def borrar():
    entrada_texto = entrada.get()
    entrada.delete(0, END)
    entrada.insert(END, entrada_texto[:-1])

# Definir botones
botones = [
    ('√', 1, 0, raiz_cuadrada), ('^', 1, 1, lambda: agregar_a_entrada('^')), ('%', 1, 2, porcentaje), 
    ('|x|', 1, 3, absoluto), ('!', 1, 4, factorial),
    ('7', 2, 0, lambda: agregar_a_entrada('7')), ('8', 2, 1, lambda: agregar_a_entrada('8')), 
    ('9', 2, 2, lambda: agregar_a_entrada('9')), ('⌫', 2, 3, borrar), ('C', 2, 4, limpiar),
    ('4', 3, 0, lambda: agregar_a_entrada('4')), ('5', 3, 1, lambda: agregar_a_entrada('5')), 
    ('6', 3, 2, lambda: agregar_a_entrada('6')), ('X', 3, 3, lambda: agregar_a_entrada('X')), 
    ('+', 3, 4, lambda: agregar_a_entrada('+')),
    ('1', 4, 0, lambda: agregar_a_entrada('1')), ('2', 4, 1, lambda: agregar_a_entrada('2')), 
    ('3', 4, 2, lambda: agregar_a_entrada('3')), ('÷', 4, 3, lambda: agregar_a_entrada('÷')), 
    ('-', 4, 4, lambda: agregar_a_entrada('-')),
    ('0', 5, 0, lambda: agregar_a_entrada('0')), ('.', 5, 1, lambda: agregar_a_entrada('.')), 
    ('(', 5, 2, lambda: agregar_a_entrada('(')), (')', 5, 3, lambda: agregar_a_entrada(')')), 
    ('=', 5, 4, evaluar)
]

# Añadir los botones a la interfaz
for (texto, fila, columna, *funcion) in botones:
    cmd = funcion[0] if funcion else lambda: None
    tk.Button(root, text=texto, height=2, width=5, command=cmd).grid(row=fila, column=columna, padx=5, pady=5)

root.mainloop()
