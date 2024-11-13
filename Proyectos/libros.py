import tkinter as tk
from tkinter import END, messagebox, ttk

libros = []
libro_id = 1  # Inicializamos el ID en 1
is_editing = False  # Bandera para saber si estamos editando

def deshabilitar_componentes():
    txTitulo.config(state="disabled")
    txAutor.config(state="disabled")
    txEditorial.config(state="disabled")
    cbClasificacion.config(state="disabled")

def habilitar_componentes():
    txTitulo.config(state="normal")
    txAutor.config(state="normal")
    txEditorial.config(state="normal")
    cbClasificacion.config(state="normal")

def limpiar_campos():
    txId.config(state="normal")
    txId.delete(0, END)
    txTitulo.delete(0, END)
    txAutor.delete(0, END)
    txEditorial.delete(0, END)
    cbClasificacion.set('')
    txId.config(state="disabled")

def nuevo_libro():
    global libro_id, is_editing
    is_editing = False  # No estamos editando
    txId.config(state="normal")
    txId.delete(0, END)
    txId.insert(0, str(libro_id))
    txId.config(state="disabled")
    habilitar_componentes()

    btnNuevo.config(state="disabled")
    btnGuardar.config(state="normal")
    btnCancelar.config(state="normal")
    btnEditar.config(state="disabled")
    btnEliminar.config(state="disabled")

def guardar_libro():
    global libro_id, is_editing
    if is_editing:
        # Si estamos editando, actualizar el libro existente
        editar_id = int(txId.get())
        for libro in libros:
            if libro['Id'] == editar_id:
                libro['Titulo'] = txTitulo.get()
                libro['Autor'] = txAutor.get()
                libro['Editorial'] = txEditorial.get()
                libro['Clasificacion'] = cbClasificacion.get()
                break
        is_editing = False
    else:
        # Si no estamos editando, crear un nuevo libro
        libro = {
            "Id": libro_id,
            "Titulo": txTitulo.get(),
            "Autor": txAutor.get(),
            "Editorial": txEditorial.get(),
            "Clasificacion": cbClasificacion.get()
        }
        libros.append(libro)
        libro_id += 1

    limpiar_campos()
    deshabilitar_componentes()

    btnGuardar.config(state="disabled")
    btnCancelar.config(state="disabled")
    btnNuevo.config(state="normal")

def cancelar_accion():
    global is_editing
    limpiar_campos()
    deshabilitar_componentes()

    btnGuardar.config(state="disabled")
    btnCancelar.config(state="disabled")
    btnNuevo.config(state="normal")
    btnEditar.config(state="disabled")
    btnEliminar.config(state="disabled")
    is_editing = False  # Restablecemos la bandera de edición

def buscar_libro():
    titulo_buscar = txBuscar.get().strip()
    if titulo_buscar:
        for libro in libros:
            if libro['Titulo'].lower() == titulo_buscar.lower():
                txId.config(state="normal")
                txId.delete(0, END)
                txId.insert(0, libro['Id'])
                txId.config(state="disabled")
                
                txTitulo.config(state="normal")
                txAutor.config(state="normal")
                txEditorial.config(state="normal")
                cbClasificacion.config(state="normal")

                txTitulo.delete(0, END)
                txAutor.delete(0, END)
                txEditorial.delete(0, END)

                txTitulo.insert(0, libro['Titulo'])
                txAutor.insert(0, libro['Autor'])
                txEditorial.insert(0, libro['Editorial'])
                cbClasificacion.set(libro['Clasificacion'])

                txTitulo.config(state="disabled")
                txAutor.config(state="disabled")
                txEditorial.config(state="disabled")
                cbClasificacion.config(state="disabled")

                btnEditar.config(state="normal")
                btnEliminar.config(state="normal")
                return
        messagebox.showinfo("Información", "Libro no encontrado")
    else:
        messagebox.showerror("Error", "Por favor ingrese un título para buscar")

def editar_libro():
    global is_editing
    habilitar_componentes()
    is_editing = True  # Estamos en modo de edición

    btnGuardar.config(state="normal")
    btnCancelar.config(state="normal")
    btnEditar.config(state="disabled")
    btnEliminar.config(state="disabled")

def eliminar_libro():
    global libros
    eliminar_id = int(txId.get())
    libros = [libro for libro in libros if libro['Id'] != eliminar_id]

    limpiar_campos()
    deshabilitar_componentes()

    btnNuevo.config(state="normal")
    btnGuardar.config(state="disabled")
    btnCancelar.config(state="disabled")
    btnEditar.config(state="disabled")
    btnEliminar.config(state="disabled")

root = tk.Tk()
root.config(width=500, height=400)
root.title("Biblioteca")

tk.Label(root, text="Ingrese título a buscar:").place(x=10, y=10)
txBuscar = tk.Entry(root)
txBuscar.place(x=160, y=10, width=200)

btnBuscar = tk.Button(root, text="Buscar", command=buscar_libro)
btnBuscar.place(x=370, y=10)

tk.Label(root, text="ID:").place(x=10, y=50)
txId = tk.Entry(root)
txId.place(x=100, y=50, width=200)
txId.config(state="disabled")

tk.Label(root, text="Título:").place(x=10, y=90)
txTitulo = tk.Entry(root, width=30)
txTitulo.place(x=100, y=90, width=200)

tk.Label(root, text="Autor:").place(x=10, y=130)
txAutor = tk.Entry(root, width=30)
txAutor.place(x=100, y=130, width=200)

tk.Label(root, text="Editorial:").place(x=10, y=170)
txEditorial = tk.Entry(root, width=30)
txEditorial.place(x=100, y=170, width=200)

tk.Label(root, text="Clasificación:").place(x=10, y=210)
cbClasificacion = ttk.Combobox(root, state="normal",
                               values=["Novela", "Cuento", "Finanzas", "Economía"])
cbClasificacion.place(x=100, y=210, width=200)

# Botones
btnNuevo = tk.Button(root, text="Nuevo", command=nuevo_libro)
btnNuevo.place(x=10, y=280)

btnGuardar = tk.Button(root, text="Guardar", state="disabled", command=guardar_libro)
btnGuardar.place(x=90, y=280)

btnCancelar = tk.Button(root, text="Cancelar", state="disabled", command=cancelar_accion)
btnCancelar.place(x=170, y=280)

btnEditar = tk.Button(root, text="Editar", state="disabled", command=editar_libro)
btnEditar.place(x=250, y=280)

btnEliminar = tk.Button(root, text="Eliminar", state="disabled", command=eliminar_libro)
btnEliminar.place(x=330, y=280)

root.mainloop()
