import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry  
from tkinter import ttk
import mysql.connector
from datetime import datetime


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        
        # Conexión a la base de datos
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dbtaller_mecanico"
        )
        self.cursor = self.conn.cursor()
        
        # Elementos de la interfaz de inicio de sesión
        self.create_login_widgets()
    
    def create_login_widgets(self):
        # Usuario
        self.label_user = tk.Label(self.root, text="User:")
        self.label_user.grid(row=0, column=0, padx=10, pady=10)
        self.entry_user = tk.Entry(self.root)
        self.entry_user.grid(row=0, column=1, padx=10, pady=10)
        
        # Contraseña
        self.label_pass = tk.Label(self.root, text="Password:")
        self.label_pass.grid(row=1, column=0, padx=10, pady=10)
        self.entry_pass = tk.Entry(self.root, show="*")
        self.entry_pass.grid(row=1, column=1, padx=10, pady=10)
        
        # Botón de inicio de sesión
        self.button_login = tk.Button(self.root, text="Login", command=self.login)
        self.button_login.grid(row=2, columnspan=2, padx=10, pady=10)
    
    def login(self):
        user = self.entry_user.get()
        password = self.entry_pass.get()
        
        # Validación de credenciales en la base de datos
        self.cursor.execute("SELECT * FROM usuarios WHERE username = %s AND password = %s", (user, password))
        result = self.cursor.fetchone()
        
        if result:
            messagebox.showinfo("Login", "Inicio de sesión exitoso")
            self.root.destroy()
            # Pasar el nombre de usuario y el perfil al menú principal
            self.open_menu(result[1], result[4])  # Aquí result[1] es el nombre del usuario y result[4] es el perfil
        else:
            messagebox.showerror("Login", "Usuario o contraseña incorrectos")
    
    def open_menu(self, username, perfil):
        menu_root = tk.Tk()
        MenuApp(menu_root, username, perfil)
        menu_root.mainloop()


class MenuApp:
    def __init__(self, root, username, perfil):
        self.root = root
        self.root.title("Menú Principal")
        self.root.geometry("300x400")

        # Guardar el nombre de usuario y perfil
        self.username = username
        self.perfil = perfil

        # Hacer que las columnas se expandan uniformemente
        self.root.columnconfigure(0, weight=1)

        # Crear la interfaz del menú
        self.create_menu_widgets()

    def create_menu_widgets(self):
        # Opciones del menú
        self.button_users = tk.Button(self.root, text="Usuarios", command=self.open_users)
        self.button_users.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.button_customer = tk.Button(self.root, text="Clientes", command=self.open_customer)
        self.button_customer.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.button_vehicle = tk.Button(self.root, text="Vehículo", command=self.open_vehicle)
        self.button_vehicle.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.button_part = tk.Button(self.root, text="Pieza", command=self.open_piezas)
        self.button_part.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.button_repair = tk.Button(self.root, text="Reparar", command=self.open_repair)
        self.button_repair.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.button_exit = tk.Button(self.root, text="Salir", command=self.root.quit)
        self.button_exit.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

    def open_users(self):
        self.root.destroy()
        users_root = tk.Tk()
        UsuarioApp(users_root, self.username, self.perfil)  # Pasar el usuario y perfil
        users_root.mainloop()

    def open_customer(self):
        self.root.destroy()
        customer_root = tk.Tk()
        ClienteApp(customer_root, self.username, self.perfil)  # Pasar el usuario y perfil
        customer_root.mainloop()

    def open_vehicle(self):
        self.root.destroy()
        vehicle_root = tk.Tk()
        VehiculoApp(vehicle_root, self.username, self.perfil)  # Pasar el usuario y perfil
        vehicle_root.mainloop()

    def open_piezas(self):
        self.root.destroy()
        piezas_root = tk.Tk()
        PiezasApp(piezas_root, self.username, self.perfil)  # Pasar el usuario y perfil
        piezas_root.mainloop()

    def open_repair(self):
        self.root.destroy()
        repair_root = tk.Tk()
        RepairApp(repair_root, self.username, self.perfil)  # Pasar el usuario y perfil
        repair_root.mainloop()


class UsuarioApp:
    def __init__(self, root, username, perfil):
        self.root = root
        self.root.title("Usuarios")
        self.username = username
        self.perfil = perfil
        
        # Conexión con la base de datos
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dbtaller_mecanico"
        )
        self.cursor = self.conn.cursor()
        
        # Elementos de la interfaz
        self.create_widgets()
        
    def create_widgets(self):
        # Etiquetas y entradas de texto
        self.label_buscar = tk.Label(self.root, text="Ingrese ID a buscar:")
        self.label_buscar.grid(row=0, column=0, padx=10, pady=10)
        self.entry_buscar = tk.Entry(self.root)
        self.entry_buscar.grid(row=0, column=1, padx=10, pady=10)
        self.button_buscar = tk.Button(self.root, text="Buscar", command=self.buscar_usuario)
        self.button_buscar.grid(row=0, column=2, padx=10, pady=10)

        self.label_id = tk.Label(self.root, text="Usuario ID:")
        self.label_id.grid(row=1, column=0, padx=10, pady=10)
        self.entry_id = tk.Entry(self.root)
        self.entry_id.grid(row=1, column=1, padx=10, pady=10)

        self.label_nombre = tk.Label(self.root, text="Nombre:")
        self.label_nombre.grid(row=2, column=0, padx=10, pady=10)
        self.entry_nombre = tk.Entry(self.root)
        self.entry_nombre.grid(row=2, column=1, padx=10, pady=10)

        self.label_username = tk.Label(self.root, text="User Name:")
        self.label_username.grid(row=3, column=0, padx=10, pady=10)
        self.entry_username = tk.Entry(self.root)
        self.entry_username.grid(row=3, column=1, padx=10, pady=10)

        self.label_password = tk.Label(self.root, text="Password:")
        self.label_password.grid(row=4, column=0, padx=10, pady=10)
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.grid(row=4, column=1, padx=10, pady=10)

        self.label_perfil = tk.Label(self.root, text="Perfil:")
        self.label_perfil.grid(row=5, column=0, padx=10, pady=10)
        self.entry_perfil = tk.Entry(self.root)
        self.entry_perfil.grid(row=5, column=1, padx=10, pady=10)

        # Botones
        self.button_nuevo = tk.Button(self.root, text="Nuevo", command=self.nuevo_usuario)
        self.button_nuevo.grid(row=6, column=0, padx=10, pady=10)

        self.button_guardar = tk.Button(self.root, text="Guardar", command=self.guardar_usuario)
        self.button_guardar.grid(row=6, column=1, padx=10, pady=10)

        self.button_editar = tk.Button(self.root, text="Editar", command=self.editar_usuario)
        self.button_editar.grid(row=7, column=0, padx=10, pady=10)

        self.button_eliminar = tk.Button(self.root, text="Eliminar", command=self.eliminar_usuario)
        self.button_eliminar.grid(row=7, column=1, padx=10, pady=10)

        self.button_cancelar = tk.Button(self.root, text="Cancelar", command=self.cancelar_usuario)
        self.button_cancelar.grid(row=8, column=0, padx=10, pady=10)

        self.button_volver = tk.Button(self.root, text="Volver al Menú", command=self.volver_menu)
        self.button_volver.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

    def nuevo_usuario(self):
        self.entry_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_perfil.delete(0, tk.END)

    def guardar_usuario(self):
        usuario_id = self.entry_id.get()
        nombre = self.entry_nombre.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        perfil = self.entry_perfil.get()

        try:
            self.cursor.execute(
                "INSERT INTO usuarios (usuario_id, nombre, username, password, perfil) VALUES (%s, %s, %s, %s, %s)",
                (usuario_id, nombre, username, password, perfil)
            )
            self.conn.commit()
            messagebox.showinfo("Éxito", "Usuario guardado exitosamente.")
            self.nuevo_usuario()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el usuario: {e}")

    def buscar_usuario(self):
        usuario_id = self.entry_buscar.get()
        try:
            self.cursor.execute("SELECT * FROM usuarios WHERE usuario_id = %s", (usuario_id,))
            usuario = self.cursor.fetchone()
            if usuario:
                self.entry_id.delete(0, tk.END)
                self.entry_nombre.delete(0, tk.END)
                self.entry_username.delete(0, tk.END)
                self.entry_password.delete(0, tk.END)
                self.entry_perfil.delete(0, tk.END)

                self.entry_id.insert(0, usuario[0])
                self.entry_nombre.insert(0, usuario[1])
                self.entry_username.insert(0, usuario[2])
                self.entry_password.insert(0, usuario[3])
                self.entry_perfil.insert(0, usuario[4])
            else:
                messagebox.showwarning("No encontrado", "Usuario no encontrado.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar el usuario: {e}")

    def editar_usuario(self):
        usuario_id = self.entry_id.get()
        nombre = self.entry_nombre.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        perfil = self.entry_perfil.get()
        try:
            self.cursor.execute(
                "UPDATE usuarios SET nombre=%s, username=%s, password=%s, perfil=%s WHERE usuario_id=%s",
                (nombre, username, password, perfil, usuario_id)
            )
            self.conn.commit()
            messagebox.showinfo("Éxito", "Usuario actualizado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar el usuario: {e}")

    def eliminar_usuario(self):
        usuario_id = self.entry_id.get()
        if not usuario_id:
            messagebox.showerror("Error", "Debe ingresar un ID para eliminar.")
            return
        try:
            self.cursor.execute("DELETE FROM usuarios WHERE usuario_id = %s", (usuario_id,))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Usuario eliminado exitosamente.")
            self.nuevo_usuario()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el usuario: {e}")

    def cancelar_usuario(self):
        self.nuevo_usuario()

    def volver_menu(self):
        self.root.destroy()
        menu_root = tk.Tk()
        MenuApp(menu_root, self.username, self.perfil)  # Volver al menú principal con el usuario y perfil
        menu_root.mainloop()


class ClienteApp:
    def __init__(self, root, username, perfil):
        self.root = root
        self.root.title("Clientes")
        
        # Conexión con la base de datos
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dbtaller_mecanico"
        )
        self.cursor = self.conn.cursor()
        
        # Guardar el usuario y perfil
        self.username = username
        self.perfil = perfil
        
        # Crear la interfaz de clientes
        self.create_widgets()
        
    def create_widgets(self):
        # Mostrar el nombre de usuario y perfil en la ventana de Clientes 

        self.label_usuario = tk.Label(self.root, text="Usuario:")
        self.label_usuario.grid(row=0, column=0, padx=10, pady=10)

        # Usamos Label en vez de Entry para mostrar el nombre de usuario sin permitir edición
        self.label_usuario_valor = tk.Label(self.root, text=self.username)
        self.label_usuario_valor.grid(row=0, column=1, padx=10, pady=10)

        self.label_perfil = tk.Label(self.root, text="Perfil:")
        self.label_perfil.grid(row=1, column=0, padx=10, pady=10)

        # Usamos Label para mostrar el perfil sin permitir edición
        self.label_perfil_valor = tk.Label(self.root, text=self.perfil)
        self.label_perfil_valor.grid(row=1, column=1, padx=10, pady=10)


        self.label_id = tk.Label(self.root, text="ID:")
        self.label_id.grid(row=2, column=0, padx=10, pady=10)
        self.entry_id = tk.Entry(self.root)
        self.entry_id.grid(row=2, column=1, padx=10, pady=10)

        self.label_nombre = tk.Label(self.root, text="Nombre:")
        self.label_nombre.grid(row=3, column=0, padx=10, pady=10)
        self.entry_nombre = tk.Entry(self.root)
        self.entry_nombre.grid(row=3, column=1, padx=10, pady=10)
        
        self.label_telefono = tk.Label(self.root, text="Teléfono:")
        self.label_telefono.grid(row=4, column=0, padx=10, pady=10)
        self.entry_telefono = tk.Entry(self.root)
        self.entry_telefono.grid(row=4, column=1, padx=10, pady=10)

        # Botones
        self.button_nuevo = tk.Button(self.root, text="Nuevo", command=self.nuevo)
        self.button_nuevo.grid(row=5, column=0, padx=10, pady=10)
        
        self.button_guardar = tk.Button(self.root, text="Guardar", state="disabled", command=self.guardar)
        self.button_guardar.grid(row=5, column=1, padx=10, pady=10)
        
        self.button_editar = tk.Button(self.root, text="Editar", state="disabled", command=self.editar)
        self.button_editar.grid(row=6, column=0, padx=10, pady=10)
        
        self.button_cancelar = tk.Button(self.root, text="Cancelar", state="disabled", command=self.cancelar)
        self.button_cancelar.grid(row=6, column=1, padx=10, pady=10)
        
        self.button_buscar = tk.Button(self.root, text="Buscar", command=self.buscar)
        self.button_buscar.grid(row=2, column=2, padx=10, pady=10)

        self.button_volver = tk.Button(self.root, text="Volver al Menú", command=self.volver_menu)
        self.button_volver.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
    
    def nuevo(self):
        # Habilitar campos y botones
        self.entry_nombre.config(state="normal")
        self.entry_telefono.config(state="normal")
        self.button_guardar.config(state="normal")
        self.button_cancelar.config(state="normal")
        self.entry_id.delete(0, tk.END)  # Limpiar ID
        self.entry_nombre.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)

    def guardar(self):
        nombre = self.entry_nombre.get()
        telefono = self.entry_telefono.get()
        
        # Encontrar el ID más bajo disponible
        try:
            self.cursor.execute("SELECT cliente_id FROM clientes ORDER BY cliente_id ASC")
            ids = self.cursor.fetchall()
            next_id = 1  # Inicializamos el próximo ID en 1
            for current_id in ids:
                if current_id[0] == next_id:
                    next_id += 1
                else:
                    break

            # Insertar el nuevo cliente con el ID más bajo disponible
            self.cursor.execute(
                "INSERT INTO clientes (cliente_id, nombre, telefono) VALUES (%s, %s, %s)",
                (next_id, nombre, telefono)
            )
            self.conn.commit()
            messagebox.showinfo("Éxito", "Cliente guardado exitosamente.")
            self.cancelar()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")

    def buscar(self):
        cliente_id = self.entry_id.get()
        if cliente_id:
            try:
                self.cursor.execute("SELECT nombre, telefono FROM clientes WHERE cliente_id = %s", (cliente_id,))
                cliente = self.cursor.fetchone()
                if cliente:
                    self.entry_nombre.config(state="normal")
                    self.entry_telefono.config(state="normal")
                    self.entry_nombre.delete(0, tk.END)
                    self.entry_telefono.delete(0, tk.END)
                    self.entry_nombre.insert(0, cliente[0])
                    self.entry_telefono.insert(0, cliente[1])
                    self.button_editar.config(state="normal")
                    self.button_cancelar.config(state="normal")
                else:
                    messagebox.showwarning("No encontrado", "Cliente no encontrado.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al buscar: {e}")

    def editar(self):
        cliente_id = self.entry_id.get()
        nombre = self.entry_nombre.get()
        telefono = self.entry_telefono.get()
        try:
            self.cursor.execute(
                "UPDATE clientes SET nombre=%s, telefono=%s WHERE cliente_id=%s",
                (nombre, telefono, cliente_id)
            )
            self.conn.commit()
            messagebox.showinfo("Éxito", "Cliente actualizado exitosamente.")
            self.cancelar()
        except Exception as e:
            messagebox.showerror("Error", f"Error al editar: {e}")
    
    def cancelar(self):
        # Limpiar campos y deshabilitar botones
        self.entry_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.config(state="disabled")
        self.entry_telefono.delete(0, tk.END)
        self.entry_telefono.config(state="disabled")
        self.button_guardar.config(state="disabled")
        self.button_editar.config(state="disabled")
        self.button_cancelar.config(state="disabled")

    def volver_menu(self):
        # Cerrar la ventana actual y abrir el menú principal
        self.root.destroy()
        menu_root = tk.Tk()
        MenuApp(menu_root, self.username, self.perfil)  # Volver al menú principal
        menu_root.mainloop()


class VehiculoApp:
    def __init__(self, root, username, perfil):
        self.root = root
        self.root.title("Vehículos")
        self.username = username
        self.perfil = perfil
        self.editando = False

        # Conexión con la base de datos (ajusta según tu configuración)
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dbtaller_mecanico"
        )
        self.cursor = self.conn.cursor()

        # Crear la interfaz
        self.create_widgets()

    def create_widgets(self):
        # Campo para buscar matrícula
        self.label_buscar_matricula = tk.Label(self.root, text="Ingrese matrícula a buscar:")
        self.label_buscar_matricula.grid(row=0, column=0, padx=10, pady=10)
        self.entry_buscar_matricula = tk.Entry(self.root)
        self.entry_buscar_matricula.grid(row=0, column=1, padx=10, pady=10)
        self.button_buscar = tk.Button(self.root, text="Buscar", command=self.buscar_vehiculo)
        self.button_buscar.grid(row=0, column=2, padx=10, pady=10)

        # Campo para buscar por cliente
        self.label_buscar_cliente = tk.Label(self.root, text="Nombre del Cliente:")
        self.label_buscar_cliente.grid(row=1, column=0, padx=10, pady=10)
        self.combobox_cliente = ttk.Combobox(self.root, state="readonly")
        self.combobox_cliente['values'] = self.obtener_nombres_clientes()
        self.combobox_cliente.grid(row=1, column=1, padx=10, pady=10)

        self.button_buscar_cliente = tk.Button(self.root, text="Buscar", command=self.buscar_vehiculos_por_cliente)
        self.button_buscar_cliente.grid(row=1, column=2, padx=10, pady=10)

        # Selector de vehículos para clientes con más de un vehículo
        self.label_select_vehiculo = tk.Label(self.root, text="Seleccione vehículo:")
        self.label_select_vehiculo.grid(row=2, column=0, padx=10, pady=10)
        self.combobox_vehiculo = ttk.Combobox(self.root, state="readonly")
        self.combobox_vehiculo.grid(row=2, column=1, padx=10, pady=10)
        self.combobox_vehiculo.bind("<<ComboboxSelected>>", self.mostrar_detalles_vehiculo)

        # Detalles del vehículo
        self.label_marca = tk.Label(self.root, text="Marca:")
        self.label_marca.grid(row=3, column=0, padx=10, pady=10)
        self.entry_marca = tk.Entry(self.root, state="readonly")
        self.entry_marca.grid(row=3, column=1, padx=10, pady=10)

        self.label_modelo = tk.Label(self.root, text="Modelo:")
        self.label_modelo.grid(row=4, column=0, padx=10, pady=10)
        self.entry_modelo = tk.Entry(self.root, state="readonly")
        self.entry_modelo.grid(row=4, column=1, padx=10, pady=10)

        self.label_ano = tk.Label(self.root, text="Año:")
        self.label_ano.grid(row=5, column=0, padx=10, pady=10)
        self.entry_ano = tk.Entry(self.root, state="readonly")
        self.entry_ano.grid(row=5, column=1, padx=10, pady=10)

        self.label_matricula = tk.Label(self.root, text="Matrícula:")
        self.label_matricula.grid(row=6, column=0, padx=10, pady=10)
        self.entry_matricula = tk.Entry(self.root, state="readonly")
        self.entry_matricula.grid(row=6, column=1, padx=10, pady=10)

        # Botones
        self.button_nuevo = tk.Button(self.root, text="Nuevo", command=self.nuevo_vehiculo)
        self.button_nuevo.grid(row=7, column=0, padx=10, pady=10)

        self.button_guardar = tk.Button(self.root, text="Guardar", command=self.guardar_vehiculo)
        self.button_guardar.grid(row=7, column=1, padx=10, pady=10)

        self.button_editar = tk.Button(self.root, text="Editar", command=self.editar_vehiculo)
        self.button_editar.grid(row=7, column=2, padx=10, pady=10)

        self.button_cancelar = tk.Button(self.root, text="Cancelar", command=self.cancelar_vehiculo)
        self.button_cancelar.grid(row=7, column=3, padx=10, pady=10)

        # Lista de reparaciones
        self.label_reparaciones = tk.Label(self.root, text="Reparaciones:")
        self.label_reparaciones.grid(row=8, column=0, padx=10, pady=10)

        self.lista_reparaciones = tk.Listbox(self.root, height=6, width=50)
        self.lista_reparaciones.grid(row=8, column=1, columnspan=2, padx=10, pady=10)

        self.button_volver = tk.Button(self.root, text="Volver al Menú", command=self.volver_menu)
        self.button_volver.grid(row=9, column=1, columnspan=2, padx=10, pady=10)

    def obtener_nombres_clientes(self):
        try:
            self.cursor.execute("SELECT nombre FROM clientes")
            clientes = [cliente[0] for cliente in self.cursor.fetchall()]
            return clientes
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los nombres de clientes: {e}")
            return []

    def buscar_vehiculo(self):
        matricula = self.entry_buscar_matricula.get()
        if not matricula:
            messagebox.showerror("Error", "Por favor, ingrese una matrícula para buscar.")
            return
        self.mostrar_detalles_vehiculo(matricula=matricula)

    def buscar_vehiculos_por_cliente(self):
        nombre_cliente = self.combobox_cliente.get()
        if not nombre_cliente:
            messagebox.showerror("Error", "Por favor, seleccione un cliente.")
            return

        try:
            # Buscar vehículos del cliente seleccionado
            self.cursor.execute("SELECT matricula, marca, modelo, ano FROM vehiculos JOIN clientes ON vehiculos.cliente_id = clientes.cliente_id WHERE clientes.nombre = %s", (nombre_cliente,))
            vehiculos = self.cursor.fetchall()

            if not vehiculos:
                messagebox.showinfo("Información", "Este cliente no tiene vehículos registrados.")
                return

            # Mostrar los vehículos en la combobox
            self.combobox_vehiculo['values'] = [f"{v[0]} - {v[1]} {v[2]} ({v[3]})" for v in vehiculos]
            self.vehiculos_cliente = {v[0]: v for v in vehiculos}  # Guardar info para referencia

            if len(vehiculos) == 1:
                # Si el cliente solo tiene un vehículo, mostrarlo de inmediato
                self.mostrar_detalles_vehiculo(matricula=vehiculos[0][0])
            else:
                # Permitir seleccionar un vehículo de la lista
                self.combobox_vehiculo.set('Seleccione un vehículo')
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar vehículos del cliente: {e}")

    def mostrar_detalles_vehiculo(self, event=None, matricula=None):
        if matricula is None:
            matricula = self.combobox_vehiculo.get().split(' ')[0]

        try:
            # Buscar detalles del vehículo
            self.cursor.execute("SELECT marca, modelo, ano, matricula, cliente_id FROM vehiculos WHERE matricula = %s", (matricula,))
            vehiculo = self.cursor.fetchone()

            if vehiculo:
                self.entry_marca.config(state="normal")
                self.entry_modelo.config(state="normal")
                self.entry_ano.config(state="normal")
                self.entry_matricula.config(state="normal")

                self.entry_marca.delete(0, tk.END)
                self.entry_marca.insert(0, vehiculo[0])

                self.entry_modelo.delete(0, tk.END)
                self.entry_modelo.insert(0, vehiculo[1])

                self.entry_ano.delete(0, tk.END)
                self.entry_ano.insert(0, vehiculo[2])

                self.entry_matricula.delete(0, tk.END)
                self.entry_matricula.insert(0, vehiculo[3])

                # Volver a deshabilitar los campos
                self.entry_marca.config(state="readonly")
                self.entry_modelo.config(state="readonly")
                self.entry_ano.config(state="readonly")
                self.entry_matricula.config(state="readonly")

                # Buscar el nombre del cliente asociado al vehículo
                cliente_id = vehiculo[4]
                self.cursor.execute("SELECT nombre FROM clientes WHERE cliente_id = %s", (cliente_id,))
                cliente = self.cursor.fetchone()

                if cliente:
                    self.combobox_cliente.set(cliente[0])  # Establecer el nombre del cliente en la combobox

                # Actualizar la combobox de vehículos para el cliente
                self.cursor.execute("SELECT matricula, marca, modelo, ano FROM vehiculos WHERE cliente_id = %s", (cliente_id,))
                vehiculos_cliente = self.cursor.fetchall()

                if vehiculos_cliente:
                    self.combobox_vehiculo['values'] = [f"{v[0]} - {v[1]} {v[2]} ({v[3]})" for v in vehiculos_cliente]

                # Mostrar las reparaciones asociadas al vehículo
                self.mostrar_reparaciones(matricula)

            else:
                messagebox.showinfo("Información", "Vehículo no encontrado.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar detalles del vehículo: {e}")

    def mostrar_reparaciones(self, matricula):
        try:
            # Limpiar lista de reparaciones
            self.lista_reparaciones.delete(0, tk.END)

            # Buscar reparaciones asociadas al vehículo
            self.cursor.execute("SELECT folio, fecha_entrada, fecha_salida, falla FROM reparaciones WHERE serial = %s", (matricula,))
            reparaciones = self.cursor.fetchall()

            if not reparaciones:
                self.lista_reparaciones.insert(tk.END, "No hay reparaciones registradas para este vehículo.")
            else:
                for rep in reparaciones:
                    self.lista_reparaciones.insert(tk.END, f"Folio: {rep[0]} | Entrada: {rep[1]} | Salida: {rep[2]} | Falla: {rep[3]}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar reparaciones: {e}")

    def nuevo_vehiculo(self):
        self.entry_marca.config(state="normal")
        self.entry_modelo.config(state="normal")
        self.entry_ano.config(state="normal")
        self.entry_matricula.config(state="normal")

        self.entry_marca.delete(0, tk.END)
        self.entry_modelo.delete(0, tk.END)
        self.entry_ano.delete(0, tk.END)
        self.entry_matricula.delete(0, tk.END)

    def guardar_vehiculo(self):
        marca = self.entry_marca.get()
        modelo = self.entry_modelo.get()
        ano = self.entry_ano.get()
        matricula = self.entry_matricula.get()
        cliente_nombre = self.combobox_cliente.get()

        if not (marca, modelo, ano, matricula, cliente_nombre):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            # Obtener el cliente_id
            self.cursor.execute("SELECT cliente_id FROM clientes WHERE nombre = %s", (cliente_nombre,))
            cliente = self.cursor.fetchone()

            if not cliente:
                messagebox.showerror("Error", "Cliente no encontrado.")
                return

            cliente_id = cliente[0]

            if self.editando:  # Si estamos editando un vehículo existente
                # Realizar un UPDATE en lugar de un INSERT
                self.cursor.execute(
                    "UPDATE vehiculos SET cliente_id = %s, marca = %s, modelo = %s, ano = %s, matricula = %s WHERE matricula = %s",
                    (cliente_id, marca, modelo, ano, matricula, self.matricula_original)
                )
                self.conn.commit()
                messagebox.showinfo("Éxito", "Vehículo actualizado exitosamente.")
                self.editando = False  # Salimos del modo edición
            else:
                # Insertar un nuevo vehículo
                self.cursor.execute(
                    "INSERT INTO vehiculos (cliente_id, marca, modelo, ano, matricula) VALUES (%s, %s, %s, %s, %s)",
                    (cliente_id, marca, modelo, ano, matricula)
                )
                self.conn.commit()
                messagebox.showinfo("Éxito", "Vehículo guardado exitosamente.")

            # Limpiar los campos
            self.cancelar_vehiculo()

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar vehículo: {e}")

    def editar_vehiculo(self):
        # Habilitar los campos para que puedan ser editados
        self.entry_marca.config(state="normal")
        self.entry_modelo.config(state="normal")
        self.entry_ano.config(state="normal")
        self.entry_matricula.config(state="normal")

        # Guardar la matrícula original antes de la edición
        self.matricula_original = self.entry_matricula.get()

        # Activar el modo edición
        self.editando = True

        # Habilitar el botón "Guardar"
        self.button_guardar.config(state="normal")

    def cancelar_vehiculo(self):
        self.entry_marca.config(state="readonly")
        self.entry_modelo.config(state="readonly")
        self.entry_ano.config(state="readonly")
        self.entry_matricula.config(state="readonly")

        self.entry_marca.delete(0, tk.END)
        self.entry_modelo.delete(0, tk.END)
        self.entry_ano.delete(0, tk.END)
        self.entry_matricula.delete(0, tk.END)

    def volver_menu(self):
        self.root.destroy()
        menu_root = tk.Tk()
        MenuApp(menu_root, self.username, self.perfil)  # Volver al menú principal
        menu_root.mainloop()

class PiezasApp:
    def __init__(self, root, username, perfil):
        self.root = root
        self.root.title("Gestión de Piezas")

        # Guardar el nombre de usuario y perfil
        self.username = username
        self.perfil = perfil

        # Conexión con la base de datos
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dbtaller_mecanico"
        )
        self.cursor = self.conn.cursor()

        # Crear la interfaz
        self.create_widgets()

    def create_widgets(self):
        # Mostrar el nombre de usuario y perfil en la interfaz
        # self.label_usuario = tk.Label(self.root, text=f"Usuario: {self.username}")
        # self.label_usuario.grid(row=0, column=0, padx=10, pady=10)

        # self.label_perfil = tk.Label(self.root, text=f"Perfil: {self.perfil}")
        # self.label_perfil.grid(row=1, column=0, padx=10, pady=10)

        # Combobox para buscar piezas por descripción
        self.label_buscar = tk.Label(self.root, text="Seleccione pieza a buscar:")
        self.label_buscar.grid(row=2, column=0, padx=10, pady=10)

        # Obtener descripciones de todas las piezas para el Combobox
        self.cursor.execute("SELECT descripcion FROM piezas")
        piezas = [pieza[0] for pieza in self.cursor.fetchall()]
        
        self.combobox_piezas = ttk.Combobox(self.root, values=piezas)
        self.combobox_piezas.grid(row=2, column=1, padx=10, pady=10)
        
        self.button_buscar = tk.Button(self.root, text="Buscar", command=self.buscar_pieza_por_descripcion)
        self.button_buscar.grid(row=2, column=2, padx=10, pady=10)

        # Campos para mostrar los detalles de la pieza seleccionada
        self.label_id = tk.Label(self.root, text="ID:")
        self.label_id.grid(row=3, column=0, padx=10, pady=10)
        self.entry_id = tk.Entry(self.root)
        self.entry_id.grid(row=3, column=1, padx=10, pady=10)

        self.label_descripcion = tk.Label(self.root, text="Descripción:")
        self.label_descripcion.grid(row=4, column=0, padx=10, pady=10)
        self.entry_descripcion = tk.Entry(self.root)
        self.entry_descripcion.grid(row=4, column=1, padx=10, pady=10)

        self.label_stock = tk.Label(self.root, text="Stock:")
        self.label_stock.grid(row=5, column=0, padx=10, pady=10)
        self.entry_stock = tk.Entry(self.root)
        self.entry_stock.grid(row=5, column=1, padx=10, pady=10)

        # Botones de acciones
        self.button_nuevo = tk.Button(self.root, text="Nuevo", command=self.nueva_pieza)
        self.button_nuevo.grid(row=6, column=0, padx=10, pady=10)

        self.button_guardar = tk.Button(self.root, text="Guardar", command=self.guardar_pieza)
        self.button_guardar.grid(row=6, column=1, padx=10, pady=10)

        self.button_editar = tk.Button(self.root, text="Editar", command=self.editar_pieza)
        self.button_editar.grid(row=7, column=0, padx=10, pady=10)

        self.button_cancelar = tk.Button(self.root, text="Cancelar", command=self.cancelar_pieza)
        self.button_cancelar.grid(row=7, column=1, padx=10, pady=10)

    def nueva_pieza(self):
        self.entry_id.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)

    def guardar_pieza(self):
        descripcion = self.entry_descripcion.get()
        stock = self.entry_stock.get()

        # Validar que el stock no sea negativo
        if int(stock) < 0:
            messagebox.showerror("Error", "No se puede registrar una pieza con stock negativo.")
            return

        try:
            # Verificar si la descripción ya existe (no permitir duplicados)
            self.cursor.execute("SELECT * FROM piezas WHERE descripcion = %s", (descripcion,))
            pieza_existente = self.cursor.fetchone()
            if pieza_existente:
                messagebox.showerror("Error", "Ya existe una pieza con esta descripción.")
                return
            
            # Guardar la nueva pieza
            self.cursor.execute("INSERT INTO piezas (descripcion, stock) VALUES (%s, %s)", (descripcion, stock))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Pieza guardada exitosamente.")
            self.nueva_pieza()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar la pieza: {e}")

    def buscar_pieza_por_descripcion(self):
        descripcion = self.combobox_piezas.get()
        try:
            # Buscar pieza por descripción
            self.cursor.execute("SELECT pieza_id, descripcion, stock FROM piezas WHERE descripcion = %s", (descripcion,))
            pieza = self.cursor.fetchone()
            if pieza:
                self.entry_id.delete(0, tk.END)
                self.entry_descripcion.delete(0, tk.END)
                self.entry_stock.delete(0, tk.END)
                
                self.entry_id.insert(0, pieza[0])
                self.entry_descripcion.insert(0, pieza[1])
                self.entry_stock.insert(0, pieza[2])
            else:
                messagebox.showwarning("No encontrado", "Pieza no encontrada.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar la pieza: {e}")

    def editar_pieza(self):
        pieza_id = self.entry_id.get()
        descripcion = self.entry_descripcion.get()
        stock = self.entry_stock.get()

        if int(stock) < 0:
            messagebox.showerror("Error", "El stock no puede ser negativo.")
            return

        try:
            self.cursor.execute(
                "UPDATE piezas SET descripcion=%s, stock=%s WHERE pieza_id=%s",
                (descripcion, stock, pieza_id)
            )
            self.conn.commit()
            messagebox.showinfo("Éxito", "Pieza actualizada exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar la pieza: {e}")

    def cancelar_pieza(self):
        self.nueva_pieza()

    def volver_menu(self):
        self.root.destroy()
        menu_root = tk.Tk()
        MenuApp(menu_root, self.username, self.perfil)  # Volver al menú principal con usuario y perfil
        menu_root.mainloop()

class RepairApp:
    def __init__(self, root, username, perfil):
        self.root = root
        self.root.title("Reparación")
        self.username = username
        self.perfil = perfil
        
        # Conexión con la base de datos
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dbtaller_mecanico"
        )
        self.cursor = self.conn.cursor()
        
        # Crear la interfaz de reparación
        self.create_widgets()

    def create_widgets(self):
        # Folio de búsqueda
        self.label_folio = tk.Label(self.root, text="Ingrese folio a buscar:")
        self.label_folio.grid(row=0, column=0, padx=10, pady=10)
        self.entry_folio = tk.Entry(self.root)
        self.entry_folio.grid(row=0, column=1, padx=10, pady=10)
        self.button_search = tk.Button(self.root, text="Search", command=self.buscar_folio)
        self.button_search.grid(row=0, column=2, padx=10, pady=10)

        # Campos de reparación (Key, Serial, Select piece, Date In, Date Out, Quantity, Falla)
        
        # Key Field
        self.label_key = tk.Label(self.root, text="Key:")
        self.label_key.grid(row=1, column=0, padx=10, pady=10)
        self.entry_key = tk.Entry(self.root)
        self.entry_key.grid(row=1, column=1, padx=10, pady=10)
        
        # Serial Dropdown
        self.label_serial = tk.Label(self.root, text="Matricula del auto a reparar:")
        self.label_serial.grid(row=2, column=0, padx=10, pady=10)
        self.combobox_serial = ttk.Combobox(self.root)
        self.combobox_serial['values'] = self.obtener_seriales()
        self.combobox_serial.grid(row=2, column=1, padx=10, pady=10)

        # Select Piece Dropdown
        self.label_pieza = tk.Label(self.root, text="Pieza:")
        self.label_pieza.grid(row=3, column=0, padx=10, pady=10)
        self.combobox_pieza = ttk.Combobox(self.root)
        self.combobox_pieza['values'] = self.obtener_piezas()
        self.combobox_pieza.grid(row=3, column=1, padx=10, pady=10)

        # Date In Field (con selector de fecha)
        self.label_date_in = tk.Label(self.root, text="Fecha de entrada:")
        self.label_date_in.grid(row=4, column=0, padx=10, pady=10)
        self.entry_date_in = DateEntry(self.root, date_pattern='yyyy-mm-dd')  # Usa DateEntry para seleccionar la fecha
        self.entry_date_in.grid(row=4, column=1, padx=10, pady=10)

        # Date Out Field (con selector de fecha)
        self.label_date_out = tk.Label(self.root, text="Fecha de salida:")
        self.label_date_out.grid(row=5, column=0, padx=10, pady=10)
        self.entry_date_out = DateEntry(self.root, date_pattern='yyyy-mm-dd')  # Usa DateEntry para seleccionar la fecha
        self.entry_date_out.grid(row=5, column=1, padx=10, pady=10)

        # Quantity Field
        self.label_quantity = tk.Label(self.root, text="Cantidad:")
        self.label_quantity.grid(row=6, column=0, padx=10, pady=10)
        self.entry_quantity = tk.Entry(self.root)
        self.entry_quantity.grid(row=6, column=1, padx=10, pady=10)

        # Falla Field
        self.label_falla = tk.Label(self.root, text="Falla:")
        self.label_falla.grid(row=7, column=0, padx=10, pady=10)
        self.entry_falla = tk.Entry(self.root)
        self.entry_falla.grid(row=7, column=1, padx=10, pady=10)

        # Botones de acción
        self.button_nuevo = tk.Button(self.root, text="Nuevo", command=self.nueva_reparacion)
        self.button_nuevo.grid(row=8, column=0, padx=10, pady=10)
        
        self.button_guardar = tk.Button(self.root, text="Guardar", command=self.guardar_reparacion)
        self.button_guardar.grid(row=8, column=1, padx=10, pady=10)
        
        self.button_cancelar = tk.Button(self.root, text="Cancelar", command=self.cancelar_reparacion)
        self.button_cancelar.grid(row=8, column=2, padx=10, pady=10)
        
        self.button_editar = tk.Button(self.root, text="Editar", command=self.editar_reparacion)
        self.button_editar.grid(row=9, column=0, padx=10, pady=10)
        
        self.button_editar = tk.Button(self.root, text="Volver al menu", command=self.volver_menu)
        self.button_editar.grid(row=9, column=2, padx=10, pady=10)

    def obtener_seriales(self):
        # Método para obtener los seriales desde la base de datos
        self.cursor.execute("SELECT matricula FROM vehiculos")
        seriales = [row[0] for row in self.cursor.fetchall()]
        return seriales

    def obtener_piezas(self):
        # Método para obtener las piezas desde la base de datos
        self.cursor.execute("SELECT descripcion FROM piezas")
        piezas = [row[0] for row in self.cursor.fetchall()]
        return piezas

    def nueva_reparacion(self):
        # Limpiar todos los campos para comenzar una nueva reparación
        self.entry_folio.delete(0, tk.END)
        self.entry_key.delete(0, tk.END)
        self.combobox_serial.set('')
        self.combobox_pieza.set('')
        self.entry_date_in.set_date(datetime.today())  # Establecer fecha actual
        self.entry_date_out.set_date(datetime.today())  # Establecer fecha actual
        self.entry_quantity.delete(0, tk.END)
        self.entry_falla.delete(0, tk.END)

    def buscar_folio(self):
        folio = self.entry_folio.get()
        if not folio:
            messagebox.showerror("Error", "Debe ingresar un folio.")
            return
        
        # Buscar el folio en la base de datos
        self.cursor.execute("SELECT * FROM reparaciones WHERE folio = %s", (folio,))
        reparacion = self.cursor.fetchone()
        if reparacion:
            self.entry_key.insert(0, reparacion[1])
            self.combobox_serial.set(reparacion[2])
            self.combobox_pieza.set(reparacion[3])
            self.entry_date_in.set_date(reparacion[4])  # Establecer la fecha seleccionada
            self.entry_date_out.set_date(reparacion[5])  # Establecer la fecha seleccionada
            self.entry_quantity.insert(0, reparacion[6])
            self.entry_falla.insert(0, reparacion[7])
        else:
            messagebox.showerror("Error", "Reparación no encontrada.")

    def obtener_folio_mas_bajo_disponible(self):
        # Consulta para obtener todos los folios en uso, ordenados de forma ascendente
        self.cursor.execute("SELECT folio FROM reparaciones ORDER BY folio ASC")
        folios_existentes = self.cursor.fetchall()

        # Si no hay folios en la base de datos, devolver 1 como el folio más bajo disponible
        if not folios_existentes:
            return 1

        # Convertir la lista de folios en uso a un set para facilitar la búsqueda de huecos
        folios_existentes = {folio[0] for folio in folios_existentes}

        # Buscar el folio más bajo disponible
        folio_mas_bajo = 1
        while folio_mas_bajo in folios_existentes:
            folio_mas_bajo += 1

        return folio_mas_bajo


    def guardar_reparacion(self):
        key = self.entry_key.get()
        serial = self.combobox_serial.get()
        pieza = self.combobox_pieza.get()
        date_in = self.entry_date_in.get_date()  # Obtén la fecha seleccionada
        date_out = self.entry_date_out.get_date()  # Obtén la fecha seleccionada
        quantity = self.entry_quantity.get()
        falla = self.entry_falla.get()

        if not (key and serial and pieza and date_in and date_out and quantity and falla):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if date_in > date_out:
            messagebox.showerror("Error", "La fecha de entrada no puede ser mayor que la fecha de salida.")
            return

        # Convertir la cantidad a entero
        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número.")
            return

        # Verificar si la pieza tiene suficiente stock antes de proceder con la reparación
        self.cursor.execute("SELECT stock FROM piezas WHERE descripcion = %s", (pieza,))
        pieza_data = self.cursor.fetchone()
        
        if pieza_data is None:
            messagebox.showerror("Error", "La pieza seleccionada no existe.")
            return

        stock_actual = pieza_data[0]  # Stock actual de la pieza

        if stock_actual < quantity:
            messagebox.showerror("Error", "Stock insuficiente para la pieza seleccionada.")
            return

        # Obtener el folio más bajo disponible antes de insertar la reparación
        folio_mas_bajo_disponible = self.obtener_folio_mas_bajo_disponible()

        # Insertar la reparación con el folio más bajo disponible
        try:
            self.cursor.execute(
                "INSERT INTO reparaciones (folio, key_field, serial, pieza, fecha_entrada, fecha_salida, cantidad, falla) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (folio_mas_bajo_disponible, key, serial, pieza, date_in, date_out, quantity, falla)
            )
            self.conn.commit()

            # Restar la cantidad del stock de la pieza
            nuevo_stock = stock_actual - quantity
            self.cursor.execute("UPDATE piezas SET stock = %s WHERE descripcion = %s", (nuevo_stock, pieza))
            self.conn.commit()

            messagebox.showinfo("Éxito", f"Reparación guardada exitosamente con folio {folio_mas_bajo_disponible} y stock actualizado.")
            self.cancelar_reparacion()

        except Exception as e:
            self.conn.rollback()  # En caso de error, revertir los cambios en la base de datos
            messagebox.showerror("Error", f"Error al guardar reparación: {e}")

    def cancelar_reparacion(self):
        self.entry_folio.delete(0, tk.END)
        self.entry_key.delete(0, tk.END)
        self.combobox_serial.set('')
        self.combobox_pieza.set('')
        self.entry_date_in.set_date(datetime.today())  # Restablecer la fecha a la actual
        self.entry_date_out.set_date(datetime.today())  # Restablecer la fecha a la actual
        self.entry_quantity.delete(0, tk.END)
        self.entry_falla.delete(0, tk.END)

    def editar_reparacion(self):
        folio = self.entry_folio.get()
        if not folio:
            messagebox.showerror("Error", "Debe ingresar un folio.")
            return

        key = self.entry_key.get()
        serial = self.combobox_serial.get()
        pieza = self.combobox_pieza.get()
        date_in = self.entry_date_in.get_date()  # Obtén la fecha seleccionada
        date_out = self.entry_date_out.get_date()  # Obtén la fecha seleccionada
        quantity = self.entry_quantity.get()
        falla = self.entry_falla.get()

        if not (key and serial and pieza and date_in and date_out and quantity and falla):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            # Actualizar la reparación existente
            self.cursor.execute(
                "UPDATE reparaciones SET key_field=%s, serial=%s, pieza=%s, fecha_entrada=%s, fecha_salida=%s, cantidad=%s, falla=%s WHERE folio=%s",
                (key, serial, pieza, date_in, date_out, quantity, falla, folio)
            )
            self.conn.commit()
            messagebox.showinfo("Éxito", "Reparación actualizada exitosamente.")
            self.cancelar_reparacion()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar reparación: {e}")

    def volver_menu(self):
        self.root.destroy()
        menu_root = tk.Tk()
        MenuApp(menu_root, self.username, self.perfil)  # Volver al menú principal con usuario y perfil
        menu_root.mainloop()


# Inicializar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    login_app = LoginApp(root)
    root.mainloop()
