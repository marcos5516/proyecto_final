import tkinter as tk
from tkinter import END, messagebox
import math

root = tk.Tk()
root.config(width=600, height=700, bg='#4d3c36')
root.title("Calculadora Científica")

# Variables para la base actual
base_actual = tk.StringVar(value="decimal")

# Función para cambiar la base
def cambiar_base(base):
    base_actual.set(base)
    limpiar()

# Entrada para mostrar y editar la expresión matemática
entrada = tk.Entry(root, width=16, font=('Arial', 24), borderwidth=2, relief="solid")
entrada.grid(row=0, column=1, columnspan=5, padx=10, pady=10)

# Botones para seleccionar la base numérica
tk.Button(root, text="Binario", width=7, command=lambda: cambiar_base("binario")).grid(row=0, column=0, padx=5, pady=5)
tk.Button(root, text="Octal", width=7, command=lambda: cambiar_base("octal")).grid(row=1, column=0, padx=5, pady=5)
tk.Button(root, text="Decimal", width=7, command=lambda: cambiar_base("decimal")).grid(row=2, column=0, padx=5, pady=5)
tk.Button(root, text="Hexadecimal", width=7, command=lambda: cambiar_base("hexadecimal")).grid(row=3, column=0, padx=5, pady=5)

# Entradas para mostrar resultados en otros sistemas numéricos
resultado_decimal = tk.Label(root, text='Decimal: ', font=('Arial', 18), bg='#4d3c36', fg='white')
resultado_decimal.grid(row=1, column=1, columnspan=5, padx=10, pady=5)

resultado_hexadecimal = tk.Label(root, text='Hexadecimal: ', font=('Arial', 18), bg='#4d3c36', fg='white')
resultado_hexadecimal.grid(row=2, column=1, columnspan=5, padx=10, pady=5)

resultado_octal = tk.Label(root, text='Octal: ', font=('Arial', 18), bg='#4d3c36', fg='white')
resultado_octal.grid(row=3, column=1, columnspan=5, padx=10, pady=5)

resultado_binario = tk.Label(root, text='Binario: ', font=('Arial', 18), bg='#4d3c36', fg='white')
resultado_binario.grid(row=4, column=1, columnspan=5, padx=10, pady=5)

# Función para agregar texto a la entrada
def agregar_a_entrada(valor):
    entrada.insert(END, valor)

# Función para convertir la expresión a decimal
def convertir_a_decimal(expresion, base):
    if base == "binario":
        return int(expresion, 2)
    elif base == "octal":
        return int(expresion, 8)
    elif base == "hexadecimal":
        return int(expresion, 16)
    return int(expresion)

# Función para evaluar la expresión
def evaluar():
    try:
        expresion = entrada.get()
        base = base_actual.get()

        # Reemplazar símbolos personalizados por operaciones válidas de Python
        expresion = expresion.replace('X', '*').replace('÷', '/').replace('^', '**')

        # Convertir números individuales en la expresión
        if base != "decimal":
            partes = []
            numero_actual = ""
            for char in expresion:
                if char.isdigit() or (base == "hexadecimal" and char.upper() in "ABCDEF"):
                    numero_actual += char
                else:
                    if numero_actual:
                        partes.append(str(convertir_a_decimal(numero_actual, base)))
                        numero_actual = ""
                    partes.append(char)
            if numero_actual:
                partes.append(str(convertir_a_decimal(numero_actual, base)))
            expresion_decimal = "".join(partes)
        else:
            expresion_decimal = expresion

        # Evaluar porcentaje
        if '%' in expresion_decimal:
            valor, porcentaje = expresion_decimal.split('%')
            valor = eval(valor)
            porcentaje = eval(porcentaje)
            resultado = valor * (porcentaje / 100)
        else:
            # Realizar la operación en decimal
            resultado = eval(expresion_decimal)

        # Mostrar resultados en diferentes bases
        resultado_decimal.config(text=f"Decimal: {resultado}")
        resultado_hexadecimal.config(text=f"Hexadecimal: {hex(int(resultado))[2:].upper()}")
        resultado_octal.config(text=f"Octal: {oct(int(resultado))[2:]}")
        resultado_binario.config(text=f"Binario: {bin(int(resultado))[2:]}")

        # Mostrar el resultado en la entrada según la base seleccionada
        if base == "binario":
            entrada.delete(0, END)
            entrada.insert(END, bin(int(resultado))[2:])
        elif base == "octal":
            entrada.delete(0, END)
            entrada.insert(END, oct(int(resultado))[2:])
        elif base == "hexadecimal":
            entrada.delete(0, END)
            entrada.insert(END, hex(int(resultado))[2:].upper())
        else:
            entrada.delete(0, END)
            entrada.insert(END, str(resultado))

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Funciones matemáticas adicionales
def raiz_cuadrada():
    try:
        expresion = entrada.get()
        resultado = eval(expresion) ** 0.5
        entrada.delete(0, END)
        entrada.insert(END, str(resultado))
    except:
        messagebox.showerror("Error", "Expresión no válida")

def factorial():
    expresion = entrada.get()
    if expresion.isdigit():  # Solo evaluar si la expresión es un número entero
        resultado = math.factorial(int(expresion))
        entrada.delete(0, END)
        entrada.insert(END, str(resultado))
    else:
        messagebox.showerror("Error", "Debe ingresar un número entero para el factorial")

def porcentaje():
    expresion = entrada.get()
    if '%' in expresion:
        valor, porcentaje = expresion.split('%')
        valor = eval(valor)
        porcentaje = eval(porcentaje)
        resultado = valor * (porcentaje / 100)
        entrada.delete(0, END)
        entrada.insert(END, str(resultado))
    else:
        messagebox.showerror("Error", "Formato de porcentaje no válido")

def absoluto():
    try:
        expresion = entrada.get()
        resultado = abs(eval(expresion))
        entrada.delete(0, END)
        entrada.insert(END, str(resultado))
    except:
        messagebox.showerror("Error", "Expresión no válida")

def seno():
    try:
        expresion = entrada.get()
        resultado = math.sin(math.radians(eval(expresion)))
        entrada.delete(0, END)
        entrada.insert(END, str(resultado))
    except:
        messagebox.showerror("Error", "Expresión no válida")

def coseno():
    try:
        expresion = entrada.get()
        resultado = math.cos(math.radians(eval(expresion)))
        entrada.delete(0, END)
        entrada.insert(END, str(resultado))
    except:
        messagebox.showerror("Error", "Expresión no válida")

# Funciones de manejo de la entrada
def limpiar():
    entrada.delete(0, END)

def borrar():
    entrada_texto = entrada.get()
    entrada.delete(0, END)
    entrada.insert(END, entrada_texto[:-1])

# Definir botones
botones = [
    ('√', 5, 1, raiz_cuadrada), ('^', 5, 2, lambda: agregar_a_entrada('^')), ('%', 5, 3, porcentaje),
    ('!', 5, 4, factorial), ('sin', 6, 1, seno), ('cos', 6, 2, coseno),
    ('A', 5, 0, lambda: agregar_a_entrada('A')), ('B', 6, 0, lambda: agregar_a_entrada('B')), 
    ('C', 7, 0, lambda: agregar_a_entrada('C')), ('D', 8, 0, lambda: agregar_a_entrada('D')),
    ('E', 9, 0, lambda: agregar_a_entrada('E')), ('F', 10, 0, lambda: agregar_a_entrada('F')),
    ('7', 7, 1, lambda: agregar_a_entrada('7')), ('8', 7, 2, lambda: agregar_a_entrada('8')), 
    ('9', 7, 3, lambda: agregar_a_entrada('9')), ('⌫', 6, 3, borrar), ('CE', 6, 4, limpiar),
    ('4', 8, 1, lambda: agregar_a_entrada('4')), ('5', 8, 2, lambda: agregar_a_entrada('5')), 
    ('6', 8, 3, lambda: agregar_a_entrada('6')), ('X', 8, 4, lambda: agregar_a_entrada('X')), 
    ('+', 10, 4, lambda: agregar_a_entrada('+')),
    ('1', 9, 1, lambda: agregar_a_entrada('1')), ('2', 9, 2, lambda: agregar_a_entrada('2')), 
    ('3', 9, 3, lambda: agregar_a_entrada('3')), ('÷', 7, 4, lambda: agregar_a_entrada('÷')), 
    ('-', 9, 4, lambda: agregar_a_entrada('-')),
    ('0', 10, 2, lambda: agregar_a_entrada('0')), ('.', 10, 1, lambda: agregar_a_entrada('.')), 
    ('=', 10, 3, evaluar)
]

# Añadir los botones a la interfaz
for (texto, fila, columna, *funcion) in botones:
    cmd = funcion[0] if funcion else lambda: None
    tk.Button(root, text=texto, height=2, width=5, command=cmd).grid(row=fila, column=columna, padx=5, pady=5)

root.mainloop()
