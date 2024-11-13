import tkinter as tk
from tkinter import messagebox
import math

# Clases para cada figura geométrica
class Triangulo:
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura
        self.area = 0

    def calcular(self):
        self.area = (self.base * self.altura) / 2

    def get_area(self):
        return self.area

class Cuadrado:
    def __init__(self, lado):
        self.lado = lado
        self.area = 0

    def calcular(self):
        self.area = self.lado ** 2

    def get_area(self):
        return self.area

class Rectangulo:
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura
        self.area = 0

    def calcular(self):
        self.area = self.base * self.altura

    def get_area(self):
        return self.area

class Poligono:
    def __init__(self, lado, num_lados):
        self.lado = lado
        self.num_lados = num_lados
        self.area = 0

    def calcular(self):
        if self.num_lados < 3:
            raise ValueError("El número de lados debe ser al menos 3.")
        # Calcular apotema
        apotema = self.lado / (2 * math.tan(math.pi / self.num_lados))
        # Calcular perímetro
        perimetro = self.lado * self.num_lados
        # Calcular área
        self.area = (perimetro * apotema) / 2

    def get_area(self):
        return self.area

# Interfaz Gráfica
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Áreas Figuras")
        self.geometry("400x500")

        self.formulario_actual = None

        # Crear botones para seleccionar la figura
        self.btTriangulo = tk.Button(self, text="Triángulo", command=self.mostrar_formulario_triangulo)
        self.btTriangulo.place(x=00, y=20)

        self.btCuadrado = tk.Button(self, text="Cuadrado", command=self.mostrar_formulario_cuadrado)
        self.btCuadrado.place(x=90, y=20)

        self.btRectangulo = tk.Button(self, text="Rectángulo", command=self.mostrar_formulario_rectangulo)
        self.btRectangulo.place(x=182, y=20)

        self.btPoligono = tk.Button(self, text="Polígono", command=self.mostrar_formulario_poligono)
        self.btPoligono.place(x=283, y=20)

        # Botón de cálculo
        self.btCalcular = tk.Button(self, text="Calcular Área", command=self.btCalcularClicked)
        self.btCalcular.place(x=10, y=450)

        # Componentes del formulario
        self.formularios = {
            'triangulo': self.crear_formulario('Base', 'Altura'),
            'cuadrado': self.crear_formulario('Lado Cuadrado'),
            'rectangulo': self.crear_formulario('Base Rectángulo', 'Altura Rectángulo'),
            'poligono': self.crear_formulario('Lado Polígono', 'Número de Lados')
        }

        self.ocultar_formularios()

    def crear_formulario(self, *labels):
        frame = tk.Frame(self)
        entries = {}
        for i, label in enumerate(labels):
            tk.Label(frame, text=label).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            entry = tk.Entry(frame)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[label] = entry
        return frame, entries

    def mostrar_formulario_triangulo(self):
        self.mostrar_formulario('triangulo')

    def mostrar_formulario_cuadrado(self):
        self.mostrar_formulario('cuadrado')

    def mostrar_formulario_rectangulo(self):
        self.mostrar_formulario('rectangulo')

    def mostrar_formulario_poligono(self):
        self.mostrar_formulario('poligono')

    def mostrar_formulario(self, figura):
        self.ocultar_formularios()
        formulario, _ = self.formularios[figura]
        formulario.place(x=10, y=60)
        self.formulario_actual = figura

    def ocultar_formularios(self):
        for formulario, _ in self.formularios.values():
            formulario.place_forget()

    def btCalcularClicked(self):
        try:
            if self.formulario_actual == 'triangulo':
                base = float(self.formularios['triangulo'][1]['Base'].get())
                altura = float(self.formularios['triangulo'][1]['Altura'].get())
                triangulo = Triangulo(base, altura)
                triangulo.calcular()
                messagebox.showinfo(title="Área Triángulo", message="Resultado: " + str(triangulo.get_area()))

            elif self.formulario_actual == 'cuadrado':
                lado = float(self.formularios['cuadrado'][1]['Lado Cuadrado'].get())
                cuadrado = Cuadrado(lado)
                cuadrado.calcular()
                messagebox.showinfo(title="Área Cuadrado", message="Resultado: " + str(cuadrado.get_area()))

            elif self.formulario_actual == 'rectangulo':
                base = float(self.formularios['rectangulo'][1]['Base Rectángulo'].get())
                altura = float(self.formularios['rectangulo'][1]['Altura Rectángulo'].get())
                rectangulo = Rectangulo(base, altura)
                rectangulo.calcular()
                messagebox.showinfo(title="Área Rectángulo", message="Resultado: " + str(rectangulo.get_area()))

            elif self.formulario_actual == 'poligono':
                lado = float(self.formularios['poligono'][1]['Lado Polígono'].get())
                num_lados = int(self.formularios['poligono'][1]['Número de Lados'].get())
                poligono = Poligono(lado, num_lados)
                poligono.calcular()
                messagebox.showinfo(title="Área Polígono", message="Resultado: " + str(poligono.get_area()))

            else:
                messagebox.showerror(title="Error", message="Por favor seleccione una figura.")

        except ValueError as e:
            messagebox.showerror(title="Error", message=f"Error en los datos ingresados: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
