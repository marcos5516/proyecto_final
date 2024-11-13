import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# Crear la ventana principal de la aplicación
root = tk.Tk()
root.title("Sistema de Reservaciones de Hotel")
root.geometry("700x250")

# Inicializar listas globales para simular una base de datos simple
clientes = []
habitaciones = [{'id': i, 'numero': i, 'estado': 'Libre'} for i in range(1, 11)]  # 10 habitaciones
reservaciones = []
reservas = []

# Definir el archivo donde se almacenarán los datos
DATA_FILE = "datos_hotel.json"

# ================= Funciones para cargar y guardar datos =================
def cargar_datos():
    global clientes, habitaciones, reservaciones, reservas  # Asegúrate de incluir las reservas aquí
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            clientes = data.get('clientes', [])
            habitaciones = data.get('habitaciones', [{'id': i, 'numero': i, 'estado': 'Libre'} for i in range(1, 11)])  # 10 habitaciones por defecto
            reservaciones = data.get('reservaciones', [])
            reservas = data.get('reservas', [])  # Cargamos las reservas aquí

            # Actualizar el estado de las habitaciones según las reservaciones cargadas
            for reserva in reservas:
                habitacion_id = reserva.get('habitacion')
                for habitacion in habitaciones:
                    if habitacion['id'] == int(habitacion_id):
                        habitacion['estado'] = 'Reservada'
    else:
        # Crear habitaciones por defecto si no existe el archivo
        habitaciones = [{'id': i, 'numero': i, 'estado': 'Libre'} for i in range(1, 11)]  # 10 habitaciones
        reservas = []  # Iniciamos reservas vacías si no existe el archivo



def guardar_datos():
    data = {
        'clientes': clientes,
        'habitaciones': habitaciones,
        'reservaciones': reservaciones,  # Reservaciones es el nombre que usas para las reservas en el JSON
        'reservas': reservas  # Aquí estamos asegurándonos de guardar también las reservas
    }
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)
    print("Datos guardados correctamente.")
    
# Llamar a la función de carga al iniciar la aplicación
cargar_datos()

# Crear el notebook para las pestañas
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Variables para el estado de los botones
modo_editar = False
cliente_seleccionado = None
reserva_seleccionada = None

# ================= Funciones para Clientes =================
def nuevo_cliente():
    limpiar_campos_cliente()
    deshabilitar_botones_edicion()

def salvar_cliente():
    global modo_editar, cliente_seleccionado
    
    nombre = entrada_nombre.get()
    direccion = entrada_direccion.get()
    email = entrada_email.get()
    telefono = entrada_telefono.get()

    if nombre and direccion and email and telefono:
        if modo_editar and cliente_seleccionado:
            # Actualizar cliente
            cliente_seleccionado['nombre'] = nombre
            cliente_seleccionado['direccion'] = direccion
            cliente_seleccionado['email'] = email
            cliente_seleccionado['telefono'] = telefono
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
        else:
            # Crear nuevo cliente
            id_cliente = len(clientes) + 1
            cliente = {'id': id_cliente, 'nombre': nombre, 'direccion': direccion, 'email': email, 'telefono': telefono}
            clientes.append(cliente)
            messagebox.showinfo("Éxito", f"Cliente registrado correctamente con ID: {id_cliente}")
        
        limpiar_campos_cliente()
        habilitar_botones_edicion()
        guardar_datos()
    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios")

def cancelar_accion():
    limpiar_campos_cliente()
    habilitar_botones_edicion()

def editar_cliente():
    global modo_editar, cliente_seleccionado
    
    cliente_id = entrada_id_buscar_cliente.get()
    cliente = next((c for c in clientes if str(c['id']) == cliente_id), None)
    if cliente:
        modo_editar = True
        cliente_seleccionado = cliente
        entrada_id.config(state='normal')
        entrada_id.delete(0, tk.END)
        entrada_id.insert(0, cliente['id'])
        entrada_id.config(state='readonly')
        
        entrada_nombre.delete(0, tk.END)
        entrada_nombre.insert(0, cliente['nombre'])

        entrada_direccion.delete(0, tk.END)
        entrada_direccion.insert(0, cliente['direccion'])

        entrada_email.delete(0, tk.END)
        entrada_email.insert(0, cliente['email'])

        entrada_telefono.delete(0, tk.END)
        entrada_telefono.insert(0, cliente['telefono'])

        deshabilitar_botones_edicion()
    else:
        messagebox.showerror("Error", "Cliente no encontrado")
        
def buscar_cliente():
    global cliente_seleccionado
    
    cliente_id = entrada_id_buscar_cliente.get()
    cliente = next((r for r in clientes if str(r['id']) == cliente_id), None)
    if cliente:
        cliente_seleccionado = cliente
        entrada_id.config(state='normal')
        entrada_id.delete(0, tk.END)
        entrada_id.insert(0, cliente['id'])
        entrada_id.config(state='readonly')
        
        entrada_nombre.delete(0, tk.END)
        entrada_nombre.insert(0, cliente['nombre'])

        entrada_direccion.delete(0, tk.END)
        entrada_direccion.insert(0, cliente['direccion'])

        entrada_email.delete(0, tk.END)
        entrada_email.insert(0, cliente['email'])

        entrada_telefono.delete(0, tk.END)
        entrada_telefono.insert(0, cliente['telefono'])

        deshabilitar_botones_buscar()
        
    else:
        messagebox.showerror("Error", "No se encontró el clientes")

def eliminar_cliente():
    cliente_id = entrada_id_buscar_cliente.get()
    cliente = next((c for c in clientes if str(c['id']) == cliente_id), None)
    
    if cliente:
        clientes.remove(cliente)
        messagebox.showinfo("Éxito", f"Cliente ID {cliente_id} eliminado correctamente")
        limpiar_campos_cliente()
        habilitar_botones_edicion()
    else:
        messagebox.showerror("Error", "Cliente no encontrado")

def limpiar_campos_cliente():
    entrada_id.config(state='normal')
    entrada_id.delete(0, tk.END)
    entrada_id.config(state='readonly')
    entrada_nombre.delete(0, tk.END)
    entrada_direccion.delete(0, tk.END)
    entrada_email.delete(0, tk.END)
    entrada_telefono.delete(0, tk.END)
    entrada_id_buscar_cliente.delete(0, tk.END)

def deshabilitar_botones_edicion():
    boton_nuevo.config(state='disabled')
    boton_editar.config(state='disabled')
    boton_eliminar.config(state='disabled')
    boton_salvar.config(state='normal')
    boton_cancelar.config(state='normal')
    
def deshabilitar_botones_buscar():
    boton_nuevo.config(state='disabled')
    boton_editar.config(state='normal')
    boton_eliminar.config(state='normal')
    boton_salvar.config(state='disabled')
    boton_cancelar.config(state='normal')
    

def habilitar_botones_edicion():
    boton_nuevo.config(state='normal')
    boton_editar.config(state='normal')
    boton_eliminar.config(state='normal')
    boton_salvar.config(state='disabled')
    boton_cancelar.config(state='disabled')
    
    
# ================= Funciones para Reservaciones =================
def limpiar_campos_reserva():
    entrada_id_reserva.delete(0, tk.END)
    combo_cliente_id.set('')
    combo_habitacion_id.set('')
    entrada_costo.delete(0, tk.END)
    entrada_fecha_reserva.delete(0, tk.END)
    entrada_hora_reserva.delete(0, tk.END)
    entrada_fecha_salida.delete(0, tk.END)

# def reservar_habitacion(cliente_id, habitacion_id, costo, fecha_reserva, hora_reserva, fecha_salida):
#     if cliente_id and habitacion_id and costo and fecha_reserva and hora_reserva and fecha_salida:
#         habitacion = next((h for h in habitaciones if h['id'] == int(habitacion_id)), None)
#         if habitacion and habitacion['estado'] == 'Libre':
#             habitacion['estado'] = 'Reservada'
#             reservacion = {
#                 'id': len(reservaciones) + 1, 'cliente_id': int(cliente_id), 'habitacion_id': int(habitacion_id),
#                 'costo': costo, 'fecha_reserva': fecha_reserva, 'hora_reserva': hora_reserva, 'fecha_salida': fecha_salida
#             }
#             reservaciones.append(reservacion)
#             messagebox.showinfo("Éxito", f"Habitación {habitacion_id} reservada correctamente")
#             limpiar_campos_reserva()
#         else:
#             messagebox.showerror("Error", "La habitación no está disponible")
#     else:
#         messagebox.showerror("Error", "Todos los campos son obligatorios")
        
def salvar_reserva():
    global modo_editar, reserva_seleccionada
    
    id_reserva = entrada_id_reserva.get().strip()
    cliente = combo_cliente_id.get().strip()
    habitacion = combo_habitacion_id.get().strip()
    costo = entrada_costo.get().strip()
    fecha_reserva = entrada_fecha_reserva.get().strip()
    fecha_salida = entrada_fecha_salida.get().strip()
    hora_reserva = entrada_hora_reserva.get().strip()
    
    # Revisar si algún campo está vacío, tanto los combobox como las entradas
    if not cliente:
        messagebox.showerror("Error", "Debe seleccionar un cliente.")
        return
    if not habitacion:
        messagebox.showerror("Error", "Debe seleccionar una habitación.")
        return
    if not costo or not fecha_reserva or not fecha_salida or not hora_reserva:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    # Si estamos en modo de edición, actualizar la reserva seleccionada
    if modo_editar and reserva_seleccionada:
        reserva_seleccionada['cliente'] = cliente
        reserva_seleccionada['costo'] = costo
        reserva_seleccionada['fecha_reserva'] = fecha_reserva
        reserva_seleccionada['id'] = id_reserva
        reserva_seleccionada['habitacion'] = habitacion
        reserva_seleccionada['fecha_salida'] = fecha_salida
        reserva_seleccionada['hora_reserva'] = hora_reserva

        messagebox.showinfo("Éxito", "Reserva actualizada correctamente")
    else:
        # Crear una nueva reserva
        id_reserva_nueva = len(reservas) + 1
        reserva = {
            'id': id_reserva_nueva, 
            'cliente': cliente, 
            'costo': costo, 
            'fecha': fecha_reserva, 
            'habitacion': habitacion, 
            'salida': fecha_salida, 
            'hora': hora_reserva
        }
        reservas.append(reserva)
        messagebox.showinfo("Éxito", f"Reserva registrada correctamente con ID: {id_reserva_nueva}")
    
    limpiar_campos_reserva()
    habilitar_botones_edicion()
    guardar_datos()

    
def buscar_reserva():
    global reserva_seleccionada
    
    reserva_id = entrada_buscar_reserva.get()
    reserva = next((r for r in reservas if str(r['id']) == reserva_id), None)
    if reserva:
        reserva_seleccionada = reserva
        entrada_id_reserva.config(state='normal')
        entrada_id_reserva.delete(0, tk.END)
        entrada_id_reserva.insert(0, reserva['id'])
        entrada_id_reserva.config(state='readonly')
        
        combo_cliente_id.delete(0, tk.END)
        combo_cliente_id.insert(0, reserva['cliente'])
        
        combo_habitacion_id.delete(0, tk.END)
        combo_habitacion_id.insert(0, reserva['habitacion'])
        
        entrada_costo.delete(0, tk.END)
        entrada_costo.insert(0, reserva['costo'])

        entrada_fecha_reserva.delete(0, tk.END)
        entrada_fecha_reserva.insert(0, reserva['fecha'])

        entrada_fecha_salida.delete(0, tk.END)
        entrada_fecha_salida.insert(0, reserva['salida'])

        entrada_hora_reserva.delete(0, tk.END)
        entrada_hora_reserva.insert(0, reserva['hora'])

        deshabilitar_botones_buscar()
        
    else:
        messagebox.showerror("Error", "No se encontró la reserva")
    
    

def buscar_reservacion(id_reserva):
    reservacion = next((r for r in reservaciones if str(r['id']) == id_reserva), None)
    if reservacion:
        messagebox.showinfo("Reservación encontrada", 
                            f"ID: {reservacion['id']}\nCliente ID: {reservacion['cliente_id']}\nHabitacion ID: {reservacion['habitacion_id']}\n"
                            f"Fecha Reserva: {reservacion['fecha_reserva']}\nHora Reserva: {reservacion['hora_reserva']}\nFecha Salida: {reservacion['fecha_salida']}\nCosto: {reservacion['costo']}")
    else:
        messagebox.showerror("Error", "No se encontró la reservación")

def cancelar_reservacion(habitacion_id):
    habitacion = next((h for h in habitaciones if h['id'] == int(habitacion_id)), None)
    if habitacion and habitacion['estado'] == 'Reservada':
        habitacion['estado'] = 'Libre'
        reservacion = next((r for r in reservaciones if r['habitacion_id'] == int(habitacion_id)), None)
        if reservacion:
            reservaciones.remove(reservacion)
            messagebox.showinfo("Éxito", f"Reservación de la habitación {habitacion_id} cancelada correctamente")
        else:
            messagebox.showerror("Error", "No se encontró la reservación")
    else:
        messagebox.showerror("Error", "La habitación no está reservada")

def editar_reservacion():
    # Aquí puedes agregar la lógica para editar una reservación
    messagebox.showinfo("Editar", "Funcionalidad de editar reservación en desarrollo")
    
#----------------------
def nueva_reservacion():
    limpiar_campos_reserva()
    deshabilitar_botones_edicion_reserva()
    
def deshabilitar_botones_edicion_reserva():
    boton_nueva_reserva.config(state='disabled')
    boton_editar_reserva.config(state='disabled')
    boton_cancelar_reserva.config(state='normal')
    boton_reservar.config(state='normal')

    
# ================= Funciones para habbitra =================
def buscar_habitacion():
    numero_buscar = numero_habitacion_entry.get()
    
    # Convertir el número a entero para la comparación
    try:
        numero_buscar = int(numero_buscar)
    except ValueError:
        messagebox.showerror("Error", "El número de habitación debe ser un valor numérico")
        return

    habitacion = next((h for h in habitaciones if h['numero'] == numero_buscar), None)
    if habitacion:
        habitacion_id_entry.delete(0, tk.END)
        habitacion_id_entry.insert(0, habitacion['id'])
        numero_entry.delete(0, tk.END)
        numero_entry.insert(0, habitacion['numero'])
        estado_combobox.set(habitacion['estado'])
    else:
        messagebox.showwarning("Buscar Habitación", "Habitación no encontrada")


def nueva_habitacion():
    numero = numero_entry.get()
    estado = estado_combobox.get()

    # Verificar si el número de habitación ya existe
    if numero:
        try:
            numero = int(numero)  # Convertir a entero
        except ValueError:
            messagebox.showerror("Error", "El número de habitación debe ser un valor numérico")
            return

        if any(h['numero'] == numero for h in habitaciones):
            messagebox.showerror("Error", "La habitación ya existe")
            return

        # Crear nueva habitación
        nueva_habitacion = {'id': len(habitaciones) + 1, 'numero': numero, 'estado': estado}
        habitaciones.append(nueva_habitacion)
        guardar_datos()  # Guardar en el archivo JSON
        messagebox.showinfo("Nueva Habitación", "Habitación agregada con éxito")
        limpiar_campos_habitacion()
    else:
        messagebox.showwarning("Nueva Habitación", "El número de habitación es obligatorio")


def editar_habitacion():
    habitacion_id_editar = habitacion_id_entry.get()

    # Verificar si la habitación existe
    habitacion = next((h for h in habitaciones if str(h['id']) == habitacion_id_editar), None)
    
    if habitacion:
        try:
            nuevo_numero = int(numero_entry.get())  # Asegurar que el número de habitación es un entero
        except ValueError:
            messagebox.showerror("Error", "El número de habitación debe ser un valor numérico")
            return

        # Actualizar los detalles de la habitación
        habitacion['numero'] = nuevo_numero
        habitacion['estado'] = estado_combobox.get()
        guardar_datos()  # Guardar los cambios en el archivo JSON
        messagebox.showinfo("Editar Habitación", "Habitación editada con éxito")
        limpiar_campos_habitacion()
    else:
        messagebox.showwarning("Editar Habitación", "Habitación no encontrada para editar")


def limpiar_campos_habitacion():
    habitacion_id_entry.delete(0, tk.END)
    numero_entry.delete(0, tk.END)
    estado_combobox.set('Libre')


# ================= Pestaña Clientes =================
tab_clientes = ttk.Frame(notebook)
notebook.add(tab_clientes, text="Clientes")

# Campos y etiquetas de cliente
tk.Label(tab_clientes, text="Ingrese Id del Cliente:").grid(row=0, column=0, padx=10, pady=5)
entrada_id_buscar_cliente = tk.Entry(tab_clientes)
entrada_id_buscar_cliente.grid(row=0, column=1, padx=10, pady=5)
boton_buscar_cliente = tk.Button(tab_clientes, text="Buscar", command=buscar_cliente)
boton_buscar_cliente.grid(row=0, column=2, padx=10, pady=5)

tk.Label(tab_clientes, text="ID:").grid(row=1, column=0, padx=10, pady=5)
entrada_id = tk.Entry(tab_clientes, state='readonly')
entrada_id.grid(row=1, column=1, padx=10, pady=5)

tk.Label(tab_clientes, text="Nombre:").grid(row=2, column=0, padx=10, pady=5)
entrada_nombre = tk.Entry(tab_clientes)
entrada_nombre.grid(row=2, column=1, padx=10, pady=5)

tk.Label(tab_clientes, text="Email:").grid(row=2, column=2, padx=10, pady=5)
entrada_email = tk.Entry(tab_clientes)
entrada_email.grid(row=2, column=3, padx=10, pady=5)

tk.Label(tab_clientes, text="Dirección:").grid(row=3, column=0, padx=10, pady=5)
entrada_direccion = tk.Entry(tab_clientes)
entrada_direccion.grid(row=3, column=1, padx=10, pady=5)

tk.Label(tab_clientes, text="Teléfono:").grid(row=4, column=0, padx=10, pady=5)
entrada_telefono = tk.Entry(tab_clientes)
entrada_telefono.grid(row=4, column=1, padx=10, pady=5)

# Botones de cliente
boton_nuevo = tk.Button(tab_clientes, text="Nuevo", command=nuevo_cliente)
boton_nuevo.grid(row=5, column=0, padx=10, pady=5)

boton_salvar = tk.Button(tab_clientes, text="Salvar", command=salvar_cliente, state='disabled')
boton_salvar.grid(row=5, column=1, padx=10, pady=5)

boton_cancelar = tk.Button(tab_clientes, text="Cancelar", command=cancelar_accion, state='disabled')
boton_cancelar.grid(row=5, column=2, padx=10, pady=5)

boton_editar = tk.Button(tab_clientes, text="Editar", command=editar_cliente)
boton_editar.grid(row=5, column=3, padx=10, pady=5)

boton_eliminar = tk.Button(tab_clientes, text="Eliminar", command=eliminar_cliente)
boton_eliminar.grid(row=5, column=4, padx=10, pady=5)

# ================= Pestaña Reservaciones =================
tab_reservaciones = ttk.Frame(notebook)
notebook.add(tab_reservaciones, text="Reservaciones")

tk.Label(tab_reservaciones, text="Ingrese ID Reservacion:").grid(row=0, column=0, padx=10, pady=5)
entrada_buscar_reserva = tk.Entry(tab_reservaciones)
entrada_buscar_reserva.grid(row=0, column=1, padx=10, pady=5)
boton_buscar_reserva = tk.Button(tab_reservaciones, text="Buscar", command= buscar_reserva)
boton_buscar_reserva.grid(row=0, column=2, padx=10, pady=5)

tk.Label(tab_reservaciones, text="Reservacion ID:").grid(row=1, column=0, padx=10, pady=5)
entrada_id_reserva = tk.Entry(tab_reservaciones, state='readonly')
entrada_id_reserva.grid(row=1, column=1, padx=10, pady=5)

tk.Label(tab_reservaciones, text="Cliente ID:").grid(row=2, column=0, padx=10, pady=5)
combo_cliente_id = ttk.Combobox(tab_reservaciones, values=[cliente['id'] for cliente in clientes])
combo_cliente_id.grid(row=2, column=1, padx=10, pady=5)

tk.Label(tab_reservaciones, text="Habitacion ID:").grid(row=3, column=0, padx=10, pady=5)
combo_habitacion_id = ttk.Combobox(tab_reservaciones, values=[h['id'] for h in habitaciones])
combo_habitacion_id.grid(row=3, column=1, padx=10, pady=5)

tk.Label(tab_reservaciones, text="Costo:").grid(row=4, column=0, padx=10, pady=5)
entrada_costo = tk.Entry(tab_reservaciones)
entrada_costo.grid(row=4, column=1, padx=10, pady=5)

tk.Label(tab_reservaciones, text="Fecha Reservacion:").grid(row=1, column=2, padx=10, pady=5)
entrada_fecha_reserva = tk.Entry(tab_reservaciones)
entrada_fecha_reserva.grid(row=1, column=3, padx=10, pady=5)

tk.Label(tab_reservaciones, text="Fecha Salida:").grid(row=2, column=2, padx=10, pady=5)
entrada_fecha_salida = tk.Entry(tab_reservaciones)
entrada_fecha_salida.grid(row=2, column=3, padx=10, pady=5)

tk.Label(tab_reservaciones, text="Hora Reservacion:").grid(row=3, column=2, padx=10, pady=5)
entrada_hora_reserva = tk.Entry(tab_reservaciones)
entrada_hora_reserva.grid(row=3, column=3, padx=10, pady=5)

# Botones para gestionar las reservaciones
boton_nueva_reserva = tk.Button(tab_reservaciones, text="Nueva Reservacion", command=nueva_reservacion)
boton_nueva_reserva.grid(row=5, column=0, padx=10, pady=5)

boton_reservar = tk.Button(tab_reservaciones, text="Reservar", command= salvar_reserva, state='disabled')
boton_reservar.grid(row=5, column=1, padx=10, pady=5)

boton_cancelar_reserva = tk.Button(tab_reservaciones, text="Cancelar Reservacion", command=lambda: cancelar_reservacion(combo_habitacion_id.get()), state='disabled')
boton_cancelar_reserva.grid(row=5, column=2, padx=10, pady=5)

boton_editar_reserva = tk.Button(tab_reservaciones, text="Editar", command=lambda: editar_reservacion(), state='disabled')
boton_editar_reserva.grid(row=5, column=3, padx=10, pady=5)

# ================= Pestaña Habitaciones =================
tab_habitaciones = ttk.Frame(notebook)
notebook.add(tab_habitaciones, text="Habitaciones")

numero_habitacion_label = ttk.Label(tab_habitaciones, text="Ingrese Número de Habitación:")
numero_habitacion_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
numero_habitacion_entry = ttk.Entry(tab_habitaciones)
numero_habitacion_entry.grid(row=0, column=1, padx=10, pady=5)
buscar_button = ttk.Button(tab_habitaciones, text="Buscar", command=buscar_habitacion)
buscar_button.grid(row=0, column=2, padx=10, pady=5)

habitacion_id_label = ttk.Label(tab_habitaciones, text="Habitación ID:")
habitacion_id_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
habitacion_id_entry = ttk.Entry(tab_habitaciones)
habitacion_id_entry.grid(row=1, column=1, padx=10, pady=5)

numero_label = ttk.Label(tab_habitaciones, text="Número:")
numero_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')
numero_entry = ttk.Entry(tab_habitaciones)
numero_entry.grid(row=2, column=1, padx=10, pady=5)

estado_label = ttk.Label(tab_habitaciones, text="Seleccione Estado Habitación:")
estado_label.grid(row=1, column=2, padx=10, pady=5, sticky='w')
estado_combobox = ttk.Combobox(tab_habitaciones, values=["Libre", "Reservada"])
estado_combobox.grid(row=1, column=3, padx=10, pady=5)
estado_combobox.set('Libre')

nueva_habitacion_button = ttk.Button(tab_habitaciones, text="Nueva Habitación", command=nueva_habitacion)
nueva_habitacion_button.grid(row=3, column=0, padx=10, pady=10)
editar_habitacion_button = ttk.Button(tab_habitaciones, text="Editar", command=editar_habitacion)
editar_habitacion_button.grid(row=3, column=1, padx=10, pady=10)

# Iniciar la aplicación
root.mainloop()