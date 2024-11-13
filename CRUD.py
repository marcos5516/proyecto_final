import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk

# Conexión a la base de datos
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Cambia a tu contraseña de MySQL
        database="SistemaControlEscolar"
    )

class SchoolControlApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Control Escolar - Login")
        self.geometry("300x240")  # Tamaño inicial para la pantalla de login
         # Evitar redimensionamiento manual
        self.current_user = None
        self.create_login_screen()
        self.bind("<Return>", lambda event: self.authenticate_user())

    def create_login_screen(self):
        # Limpiar la ventana y establecer el tamaño
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("300x240")
        
        # Crear los elementos de la pantalla de login
        tk.Label(self, text="Usuario o Correo:").pack(pady=(20, 5))
        self.user_entry = tk.Entry(self)
        self.user_entry.pack(padx=20, pady=5)

        tk.Label(self, text="Contraseña:").pack(pady=(10, 5))
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(padx=20, pady=5)

        tk.Button(self, text="Iniciar Sesión", command=self.authenticate_user).pack(pady=(20, 10))

    def authenticate_user(self):
        user_input = self.user_entry.get()  # Puede ser correo o nombre de usuario
        contraseña = self.password_entry.get()

        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        cursor.execute("""
            SELECT perfil FROM Usuarios 
            WHERE (correo = %s OR nombre_usuario = %s) AND contraseña = %s
        """, (user_input, user_input, contraseña))
        
        user = cursor.fetchone()
        conexion.close()

        if user:
            self.current_user = user[0]
            messagebox.showinfo("Login Exitoso", f"Bienvenido {self.current_user}")
            self.show_main_menu()  # Mostrar el menú principal
        else:
            messagebox.showerror("Error", "Usuario/Correo o contraseña incorrectos")

    def show_main_menu(self):
        # Limpiar la ventana y ajustar el tamaño
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("300x400")

        self.title("Sistema de Control Escolar - Menú Principal")
        botones = [
            ("Usuarios", self.users_menu),
            ("Alumnos", self.students_menu),
            ("Maestros", self.teachers_menu),
            ("Materias", self.subjects_menu),
            ("Grupos", self.groups_menu),
            ("Horario", self.schedule_menu),
            ("Salón", self.classroom_menu),
            ("Carrera", self.career_menu),
            ("Planeación", self.planning_menu)
        ]
        
        for texto, comando in botones:
            tk.Button(self, text=texto, command=comando).pack(fill="x", padx=10, pady=5)

    def users_menu(self):
        if self.current_user == "Administrador":
            self.create_user_interface()
        else:
            messagebox.showerror("Acceso denegado", "Solo el administrador puede acceder a esta sección.")

    def create_user_interface(self):
        # Limpiar la ventana y ajustar el tamaño
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("600x400")
        
        self.title("Sistema de Control Escolar - Usuarios")
        
        # Campos de búsqueda
        tk.Label(self, text="Ingrese código usuario:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.search_entry = tk.Entry(self)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Button(self, text="Buscar", command=self.search_user).grid(row=0, column=2, padx=5, pady=5)

        # Campos del formulario
        tk.Label(self, text="ID:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.id_entry = tk.Entry(self)
        self.id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Nombre:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.nombre_entry = tk.Entry(self)
        self.nombre_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="A Paterno:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.apaterno_entry = tk.Entry(self)
        self.apaterno_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="A Materno:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.amaterno_entry = tk.Entry(self)
        self.amaterno_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Nombre Usuario:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Password:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Perfil:").grid(row=3, column=2, padx=5, pady=5, sticky="e")
        self.perfil_combobox = ttk.Combobox(self, values=["Administrador", "Maestro", "Alumno"])
        self.perfil_combobox.grid(row=3, column=3, padx=5, pady=5, sticky="w")

        # Botones de acción
        tk.Button(self, text="Nuevo", command=self.new_user).grid(row=6, column=0, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Guardar", command=self.save_user).grid(row=6, column=1, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Cancelar", command=self.clear_fields).grid(row=6, column=2, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Editar", command=self.update_user).grid(row=6, column=3, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Baja", command=self.delete_user).grid(row=6, column=4, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Volver al Menú Principal", command=self.show_main_menu).grid(row=7, column=0, columnspan=5, pady=20)


    def search_user(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        codigo = self.search_entry.get()

        cursor.execute("SELECT * FROM Usuarios WHERE id_usuario = %s", (codigo,))
        user = cursor.fetchone()
        conexion.close()

        if user:
            print("Datos obtenidos de la base de datos:", user)  # Para verificar el orden de los datos
            try:
                # Asignar cada valor al campo correspondiente en la interfaz
                self.id_entry.delete(0, tk.END)
                self.id_entry.insert(0, user[0])  # ID de usuario
                
                self.nombre_entry.delete(0, tk.END)
                self.nombre_entry.insert(0, user[5])  # Nombre

                self.apaterno_entry.delete(0, tk.END)
                self.apaterno_entry.insert(0, user[6])  # Apellido Paterno

                self.amaterno_entry.delete(0, tk.END)
                self.amaterno_entry.insert(0, user[7])  # Apellido Materno

                self.username_entry.delete(0, tk.END)
                self.username_entry.insert(0, user[4])  # Nombre de Usuario

                self.password_entry.delete(0, tk.END)
                self.password_entry.insert(0, user[2])  # Contraseña

                self.perfil_combobox.set(user[3])  # Perfil
            except IndexError:
                messagebox.showerror("Error", "La estructura de la base de datos no coincide con el código.")
        else:
            messagebox.showerror("Error", "Usuario no encontrado")
            
    def new_user(self):
        self.clear_fields()

    def save_user(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()

        # Datos para la tabla Usuarios, incluyendo el ID ingresado
        datos_usuario = (
            self.id_entry.get(),  # ID de usuario ingresado
            self.nombre_entry.get(),
            self.apaterno_entry.get(),
            self.amaterno_entry.get(),
            f"{self.username_entry.get()}@alumnos.com",  # Genera el correo automáticamente
            self.username_entry.get(),
            self.password_entry.get(),
            self.perfil_combobox.get()  # Perfil seleccionado en el combobox
        )

        try:
            # Inserta el nuevo usuario con el ID especificado en la tabla Usuarios
            cursor.execute("""
                INSERT INTO Usuarios (id_usuario, nombre, apellido_paterno, apellido_materno, correo, nombre_usuario, contraseña, perfil) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, datos_usuario)
            
            # Si el perfil es "Alumno", insertar automáticamente en la tabla Alumnos con el estado predeterminado
            if datos_usuario[-1] == "Alumno":
                estado = self.estado_entry.get() if hasattr(self, 'estado_entry') else "Activo"

                datos_alumno = (
                    self.id_entry.get(),  # Usar el ID ingresado como ID del alumno
                    estado
                )

                cursor.execute("""
                    INSERT INTO Alumnos (id_usuario, estado)
                    VALUES (%s, %s)
                """, datos_alumno)
            
            # Confirmar transacción
            conexion.commit()
            messagebox.showinfo("Guardar", "Usuario y perfil de alumno creados exitosamente")
        except mysql.connector.IntegrityError as e:
            messagebox.showerror("Error", f"Error al guardar el usuario o el perfil de alumno: {e}")
        finally:
            # Cerrar conexión y limpiar campos
            conexion.close()
            self.clear_fields()


    def update_user(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        email = f"{self.username_entry.get()}@alumnos.com"
        
        datos = (
            self.nombre_entry.get(),
            self.apaterno_entry.get(),
            self.amaterno_entry.get(),
            email,
            self.username_entry.get(),
            self.password_entry.get(),
            self.perfil_combobox.get(),
            self.id_entry.get()
        )
        
        cursor.execute("UPDATE Usuarios SET nombre=%s, apellido_paterno=%s, apellido_materno=%s, correo=%s, nombre_usuario=%s, contraseña=%s, perfil=%s WHERE id_usuario=%s", datos)
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Actualizar", "Usuario actualizado exitosamente")
        self.clear_fields()

    def delete_user(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        id_usuario = self.id_entry.get()
        cursor.execute("DELETE FROM Usuarios WHERE id_usuario = %s", (id_usuario,))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Eliminar", "Usuario eliminado exitosamente")
        self.clear_fields()

    def clear_fields(self):
        # Campos comunes
        if hasattr(self, 'id_entry'):
            self.id_entry.delete(0, tk.END)
        if hasattr(self, 'nombre_entry'):
            self.nombre_entry.delete(0, tk.END)
        if hasattr(self, 'apaterno_entry'):
            self.apaterno_entry.delete(0, tk.END)
        if hasattr(self, 'amaterno_entry'):
            self.amaterno_entry.delete(0, tk.END)
        if hasattr(self, 'username_entry'):
            self.username_entry.delete(0, tk.END)
        if hasattr(self, 'password_entry'):
            self.password_entry.delete(0, tk.END)
        if hasattr(self, 'perfil_combobox'):
            self.perfil_combobox.set("")

        # Campos específicos de la ventana de Alumnos
        if hasattr(self, 'carrera_combobox'):
            self.carrera_combobox.set("")
        if hasattr(self, 'materia_listbox'):
            self.materia_listbox.selection_clear(0, tk.END)

    def students_menu(self):
        # Limpiar la ventana actual
        for widget in self.winfo_children():
            widget.destroy()

        # Configurar la ventana
        self.title("Sistema de Control Escolar - Alumnos")
        self.geometry("700x700")

        # Campos de búsqueda y formulario
        tk.Label(self, text="Ingrese código alumno:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.search_entry = tk.Entry(self)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Button(self, text="Buscar", command=self.search_student).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(self, text="ID:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.id_entry = tk.Entry(self)
        self.id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Nombre:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.nombre_entry = tk.Entry(self)
        self.nombre_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="A Paterno:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.apaterno_entry = tk.Entry(self)
        self.apaterno_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="A Materno:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.amaterno_entry = tk.Entry(self)
        self.amaterno_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Email:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Estado:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.estado_entry = tk.Entry(self)
        self.estado_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Fecha Nac:").grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.fecha_nac_entry = tk.Entry(self)
        self.fecha_nac_entry.grid(row=7, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Carrera:").grid(row=8, column=0, padx=5, pady=5, sticky="e")
        self.carrera_combobox = ttk.Combobox(self, values=["Ingeniería en Computación", "Ingeniería Civil", "Medicina", "Derecho"])
        self.carrera_combobox.grid(row=8, column=1, padx=5, pady=5, sticky="w")
        self.carrera_combobox.bind("<<ComboboxSelected>>", self.cargar_materias)

        # Combobox para seleccionar materias y listbox para mostrar materias seleccionadas
        tk.Label(self, text="Materia").grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.materia_combobox = ttk.Combobox(self)
        self.materia_combobox.grid(row=5, column=2, padx=5, pady=5, sticky="w")

        tk.Button(self, text="Añadir Materia", command=self.add_materia).grid(row=6, column=2, padx=5, pady=5)

        tk.Label(self, text="Materias Seleccionadas:").grid(row=7, column=2, padx=5, pady=5, sticky="w")
        self.materia_listbox = tk.Listbox(self)
        self.materia_listbox.grid(row=8, column=2, columnspan=2, padx=5, pady=5, sticky="w")

        # Botón para guardar las materias en la base de datos
        tk.Button(self, text="Guardar Materias", command=self.guardar_materias).grid(row=9, column=2, pady=10)

        # Botones de acción
        tk.Button(self, text="Nuevo", command=self.new_student).grid(row=12, column=0, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Guardar", command=self.save_student).grid(row=12, column=1, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Cancelar", command=self.clear_fields).grid(row=12, column=2, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Editar", command=self.update_student).grid(row=12, column=3, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Baja", command=self.delete_student).grid(row=12, column=4, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Volver al Menú Principal", command=self.show_main_menu).grid(row=13, column=0, columnspan=5, pady=20)

    def cargar_materias(self, event):
        carrera = self.carrera_combobox.get()
        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT nombre_materia FROM Materias
            JOIN Carreras ON Materias.id_carrera = Carreras.id_carrera
            WHERE Carreras.nombre_carrera = %s
        """, (carrera,))
        materias = cursor.fetchall()
        conexion.close()

        self.materia_combobox['values'] = [materia[0] for materia in materias]

    def add_materia(self):
        materia = self.materia_combobox.get()
        if materia and materia not in self.materia_listbox.get(0, tk.END):
            self.materia_listbox.insert(tk.END, materia)

    def guardar_materias(self):
        id_alumno = self.id_entry.get()
        if not id_alumno:
            messagebox.showerror("Error", "Primero ingresa un ID de alumno.")
            return

        conexion = conectar_bd()
        cursor = conexion.cursor()

        for materia in self.materia_listbox.get(0, tk.END):
            cursor.execute("SELECT id_materia FROM Materias WHERE nombre_materia = %s", (materia,))
            id_materia = cursor.fetchone()
            if id_materia:
                cursor.execute("INSERT INTO Alumno_Materia (id_alumno, id_materia) VALUES (%s, %s)", (id_alumno, id_materia[0]))

        conexion.commit()
        conexion.close()
        messagebox.showinfo("Guardar Materias", "Materias guardadas exitosamente para el alumno.")


    def search_student(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        codigo = self.search_entry.get()

        cursor.execute("""
            SELECT a.id_alumno, u.nombre, u.apellido_paterno, u.apellido_materno, u.correo, 
                a.estado, a.fecha_nac, c.nombre_carrera AS carrera, u.perfil
            FROM Alumnos a
            JOIN Usuarios u ON a.id_usuario = u.id_usuario
            LEFT JOIN Carreras c ON a.id_carrera = c.id_carrera
            WHERE a.id_alumno = %s
        """, (codigo,))
        student = cursor.fetchone()
        conexion.close()

        if student:
            student_id, nombre, apellido_paterno, apellido_materno, correo, estado, fecha_nac, carrera, perfil = student
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, student_id)
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, nombre)
            self.apaterno_entry.delete(0, tk.END)
            self.apaterno_entry.insert(0, apellido_paterno)
            self.amaterno_entry.delete(0, tk.END)
            self.amaterno_entry.insert(0, apellido_materno)
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, correo)
            self.estado_entry.delete(0, tk.END)
            self.estado_entry.insert(0, estado)

            # Verificar si `fecha_nac` y `carrera` están vacíos antes de mostrarlos
            if fecha_nac:
                self.fecha_nac_entry.delete(0, tk.END)
                self.fecha_nac_entry.insert(0, fecha_nac)
            else:
                self.fecha_nac_entry.delete(0, tk.END)

            if carrera:
                self.carrera_combobox.set(carrera)
                self.carrera_combobox.config(state="disabled")  # Deshabilitar si ya tiene carrera
                self.cargar_materias(carrera)  # Cargar materias de la carrera
            else:
                self.carrera_combobox.set("")
                self.carrera_combobox.config(state="normal")  # Habilitar si no tiene carrera
                self.materia_combobox['values'] = []  # Limpiar materias si no hay carrera seleccionada
        else:
            messagebox.showerror("Error", "Alumno no encontrado")
        

    def new_student(self):
        self.clear_fields()
        self.carrera_combobox.config(state="normal")

    def save_student(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        datos_usuario = (
            self.nombre_entry.get(),
            self.apaterno_entry.get(),
            self.amaterno_entry.get(),
            self.email_entry.get(),
            "Alumno"
        )

        try:
            cursor.execute("""
                INSERT INTO Usuarios (nombre, apellido_paterno, apellido_materno, correo, perfil) 
                VALUES (%s, %s, %s, %s, %s)
            """, datos_usuario)
            
            id_usuario = cursor.lastrowid

            datos_alumno = (
                id_usuario,
                self.estado_entry.get() if self.estado_entry.get() else "Activo",
                self.fecha_nac_entry.get(),
                self.carrera_combobox.get()
            )

            cursor.execute("""
                INSERT INTO Alumnos (id_usuario, estado, fecha_nac, id_carrera)
                VALUES (%s, %s, %s, (SELECT id_carrera FROM Carreras WHERE nombre_carrera = %s))
            """, datos_alumno)

            conexion.commit()
            messagebox.showinfo("Guardar", "Alumno guardado exitosamente")
        except mysql.connector.IntegrityError as e:
            messagebox.showerror("Error", f"Error al guardar el alumno: {e}")
        finally:
            conexion.close()
            self.clear_fields()

    def update_student(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()

        datos = (
            self.nombre_entry.get(),
            self.apaterno_entry.get(),
            self.amaterno_entry.get(),
            self.email_entry.get(),
            self.estado_entry.get(),
            self.fecha_nac_entry.get(),
            self.carrera_combobox.get(),
            self.id_entry.get()
        )

        cursor.execute("""
            UPDATE Usuarios SET nombre=%s, apellido_paterno=%s, apellido_materno=%s, correo=%s
            WHERE id_usuario=(SELECT id_usuario FROM Alumnos WHERE id_alumno=%s)
        """, datos[:4] + (datos[7],))

        cursor.execute("""
            UPDATE Alumnos SET estado=%s, fecha_nac=%s, id_carrera=(SELECT id_carrera FROM Carreras WHERE nombre_carrera = %s)
            WHERE id_alumno=%s
        """, (datos[4], datos[5], datos[6], datos[7]))

        conexion.commit()
        conexion.close()
        messagebox.showinfo("Actualizar", "Alumno actualizado exitosamente")
        self.clear_fields()

    def delete_student(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        id_alumno = self.id_entry.get()
        cursor.execute("DELETE FROM Alumnos WHERE id_alumno = %s", (id_alumno,))
        cursor.execute("DELETE FROM Usuarios WHERE id_usuario = (SELECT id_usuario FROM Alumnos WHERE id_alumno = %s)", (id_alumno,))
        
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Eliminar", "Alumno eliminado exitosamente")
        self.clear_fields()

    def clear_fields(self):
        self.id_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.apaterno_entry.delete(0, tk.END)
        self.amaterno_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.estado_entry.delete(0, tk.END)
        self.fecha_nac_entry.delete(0, tk.END)
        self.carrera_combobox.set("")
        self.materia_combobox.set("")
        self.materia_listbox.delete(0, tk.END)

    def teachers_menu(self):
        self.geometry("300x400")
        messagebox.showinfo("Maestros", "Funcionalidad de Maestros no implementada.")

    def subjects_menu(self):
        # Limpiar la ventana y ajustar el tamaño
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("600x400")
        
        self.title("Sistema de Control Escolar - Materias")

        # Campos de búsqueda
        tk.Label(self, text="Ingrese código materia:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.search_entry = tk.Entry(self)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Button(self, text="Buscar", command=self.search_subject).grid(row=0, column=2, padx=5, pady=5)

        # Campos del formulario
        tk.Label(self, text="ID:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.id_entry = tk.Entry(self)
        self.id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Asignatura:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.asignatura_entry = tk.Entry(self)
        self.asignatura_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Carrera:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.carrera_combobox = ttk.Combobox(self, values=["Ingeniería en Computación", "Ingeniería Civil", "Medicina", "Derecho"])
        self.carrera_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Créditos:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.creditos_entry = tk.Entry(self)
        self.creditos_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Semestre:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.semestre_entry = tk.Entry(self)
        self.semestre_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Botones de acción
        tk.Button(self, text="Nuevo", command=self.new_subject).grid(row=6, column=0, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Guardar", command=self.save_subject).grid(row=6, column=1, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Cancelar", command=self.clear_fields).grid(row=6, column=2, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Editar", command=self.update_subject).grid(row=6, column=3, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Baja", command=self.delete_subject).grid(row=6, column=4, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Volver al Menú Principal", command=self.show_main_menu).grid(row=7, column=0, columnspan=5, pady=20)

    def search_subject(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        codigo = self.search_entry.get()

        cursor.execute("SELECT * FROM Materias WHERE id_materia = %s", (codigo,))
        materia = cursor.fetchone()
        conexion.close()

        if materia:
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, materia[0])

            self.asignatura_entry.delete(0, tk.END)
            self.asignatura_entry.insert(0, materia[1])

            self.carrera_combobox.set(materia[2])
            self.creditos_entry.delete(0, tk.END)
            self.creditos_entry.insert(0, materia[3])

            self.semestre_entry.delete(0, tk.END)
            self.semestre_entry.insert(0, materia[4])
        else:
            messagebox.showerror("Error", "Materia no encontrada")

    def save_subject(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()

        # Obtén el id_carrera basado en el nombre de la carrera seleccionada
        carrera_nombre = self.carrera_combobox.get()
        cursor.execute("SELECT id_carrera FROM Carreras WHERE nombre_carrera = %s", (carrera_nombre,))
        carrera = cursor.fetchone()

        if carrera:
            id_carrera = carrera[0]  # Extrae el id_carrera
            datos_materia = (
                self.asignatura_entry.get(),
                id_carrera,
                self.creditos_entry.get(),
                self.semestre_entry.get()
            )

            try:
                cursor.execute("""
                    INSERT INTO Materias (nombre_materia, id_carrera, creditos, semestre) 
                    VALUES (%s, %s, %s, %s)
                """, datos_materia)
                conexion.commit()
                messagebox.showinfo("Guardar", "Materia guardada exitosamente")
            except mysql.connector.IntegrityError as e:
                messagebox.showerror("Error", f"Error al guardar la materia: {e}")
            finally:
                conexion.close()
                self.clear_fields()
        else:
            messagebox.showerror("Error", "Carrera no encontrada en la base de datos")

    def update_subject(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()

        datos_materia = (
            self.asignatura_entry.get(),
            self.carrera_combobox.get(),
            self.creditos_entry.get(),
            self.semestre_entry.get(),
            self.id_entry.get()
        )

        cursor.execute("""
            UPDATE Materias SET nombre_materia=%s, id_carrera=%s, creditos=%s, semestre=%s 
            WHERE id_materia=%s
        """, datos_materia)
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Actualizar", "Materia actualizada exitosamente")
        self.clear_fields()


    def delete_subject(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        id_materia = self.id_entry.get()
        cursor.execute("DELETE FROM Materias WHERE id_materia = %s", (id_materia,))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Eliminar", "Materia eliminada exitosamente")
        self.clear_fields()

    def new_subject(self):
        self.clear_fields()


    def clear_fields(self):
        self.id_entry.delete(0, tk.END)
        self.asignatura_entry.delete(0, tk.END)
        self.carrera_combobox.set("")
        self.creditos_entry.delete(0, tk.END)
        self.semestre_entry.delete(0, tk.END)


    def groups_menu(self):
        # Limpiar la ventana y ajustar el tamaño
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("600x500")
        
        self.title("Sistema de Control Escolar - Grupos")

        # Campos de búsqueda
        tk.Label(self, text="Ingrese código grupo:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.search_entry = tk.Entry(self)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Button(self, text="Buscar", command=self.search_group).grid(row=0, column=2, padx=5, pady=5)

        # Campos del formulario
        tk.Label(self, text="ID:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.id_entry = tk.Entry(self)
        self.id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Nombre grupo:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.nombre_grupo_entry = tk.Entry(self)
        self.nombre_grupo_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Fecha:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.fecha_entry = tk.Entry(self)
        self.fecha_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Carrera:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.carrera_combobox = ttk.Combobox(self, values=["Ingeniería en Computación", "Ingeniería Civil", "Medicina", "Derecho"])
        self.carrera_combobox.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.carrera_combobox.bind("<<ComboboxSelected>>", self.search_subject)

        tk.Label(self, text="Materia:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.materia_combobox = ttk.Combobox(self)
        self.materia_combobox.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Salón:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.salon_combobox = ttk.Combobox(self, values=["Salón 1", "Salón 2", "Salón 3"])
        self.salon_combobox.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Horario:").grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.horario_entry = tk.Entry(self)
        self.horario_entry.grid(row=7, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Semestre:").grid(row=8, column=0, padx=5, pady=5, sticky="e")
        self.semestre_entry = tk.Entry(self)
        self.semestre_entry.grid(row=8, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Máx num Alumnos:").grid(row=9, column=0, padx=5, pady=5, sticky="e")
        self.max_alumnos_entry = tk.Entry(self)
        self.max_alumnos_entry.grid(row=9, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Maestro:").grid(row=10, column=0, padx=5, pady=5, sticky="e")
        self.maestro_combobox = ttk.Combobox(self, values=["Maestro 1", "Maestro 2", "Maestro 3"])  # Valores de ejemplo
        self.maestro_combobox.grid(row=10, column=1, padx=5, pady=5, sticky="w")

        # Botones de acción
        tk.Button(self, text="Nuevo", command=self.new_group).grid(row=11, column=0, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Guardar", command=self.save_group).grid(row=11, column=1, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Cancelar", command=self.clear_fields).grid(row=11, column=2, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Editar", command=self.update_group).grid(row=11, column=3, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Baja", command=self.delete_group).grid(row=11, column=4, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Volver al Menú Principal", command=self.show_main_menu).grid(row=12, column=0, columnspan=5, pady=20)

    def search_group(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        codigo = self.search_entry.get()

        cursor.execute("SELECT * FROM Grupos WHERE id_grupo = %s", (codigo,))
        grupo = cursor.fetchone()
        conexion.close()

        if grupo:
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, grupo[0])

            self.nombre_grupo_entry.delete(0, tk.END)
            self.nombre_grupo_entry.insert(0, grupo[1])

            self.fecha_entry.delete(0, tk.END)
            self.fecha_entry.insert(0, grupo[2])

            self.carrera_combobox.set(grupo[3])
            self.materia_combobox.set(grupo[4])
            self.salon_combobox.set(grupo[5])
            self.horario_entry.delete(0, tk.END)
            self.horario_entry.insert(0, grupo[6])

            self.semestre_entry.delete(0, tk.END)
            self.semestre_entry.insert(0, grupo[7])

            self.max_alumnos_entry.delete(0, tk.END)
            self.max_alumnos_entry.insert(0, grupo[8])

            self.maestro_combobox.set(grupo[9])
        else:
            messagebox.showerror("Error", "Grupo no encontrado")

    def save_group(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()

        datos_grupo = (
            self.nombre_grupo_entry.get(),
            self.fecha_entry.get(),
            self.carrera_combobox.get(),
            self.materia_combobox.get(),
            self.salon_combobox.get(),
            self.horario_entry.get(),
            self.semestre_entry.get(),
            self.max_alumnos_entry.get(),
            self.maestro_combobox.get()
        )

        try:
            cursor.execute("""
                INSERT INTO Grupos (nombre_grupo, fecha, carrera, materia, salon, horario, semestre, max_alumnos, maestro) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, datos_grupo)
            conexion.commit()
            messagebox.showinfo("Guardar", "Grupo guardado exitosamente")
        except mysql.connector.IntegrityError as e:
            messagebox.showerror("Error", f"Error al guardar el grupo: {e}")
        finally:
            conexion.close()
            self.clear_fields()

    def update_group(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()

        datos_grupo = (
            self.nombre_grupo_entry.get(),
            self.fecha_entry.get(),
            self.carrera_combobox.get(),
            self.materia_combobox.get(),
            self.salon_combobox.get(),
            self.horario_entry.get(),
            self.semestre_entry.get(),
            self.max_alumnos_entry.get(),
            self.maestro_combobox.get(),
            self.id_entry.get()
        )

        cursor.execute("""
            UPDATE Grupos SET nombre_grupo=%s, fecha=%s, carrera=%s, materia=%s, salon=%s, horario=%s, semestre=%s, max_alumnos=%s, maestro=%s
            WHERE id_grupo=%s
        """, datos_grupo)
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Actualizar", "Grupo actualizado exitosamente")
        self.clear_fields()

            
    def new_group(self):
        self.clear_fields()


    def delete_group(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        id_grupo = self.id_entry.get()
        cursor.execute("DELETE FROM Grupos WHERE id_grupo = %s", (id_grupo,))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Eliminar", "Grupo eliminado exitosamente")
        self.clear_fields()


    def clear_fields(self):
        self.id_entry.delete(0, tk.END)
        self.nombre_grupo_entry.delete(0, tk.END)
        self.fecha_entry.delete(0, tk.END)
        self.carrera_combobox.set("")
        self.materia_combobox.set("")
        self.salon_combobox.set("")
        self.horario_entry.delete(0, tk.END)
        self.semestre_entry.delete(0, tk.END)
        self.max_alumnos_entry.delete(0, tk.END)
        self.maestro_combobox.set("")


    def schedule_menu(self):
        # Limpiar la ventana y ajustar el tamaño
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("600x400")
        
        self.title("Sistema de Control Escolar - Horario")

        # Campos de búsqueda
        tk.Label(self, text="Ingrese código grupo:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.search_entry = tk.Entry(self)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Button(self, text="Buscar", command=self.search_schedule).grid(row=0, column=2, padx=5, pady=5)

        # Campos del formulario
        tk.Label(self, text="ID:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.id_entry = tk.Entry(self)
        self.id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Turno:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.turno_combobox = ttk.Combobox(self, values=["Matutino", "Vespertino", "Nocturno"])
        self.turno_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Hora:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.hora_entry = tk.Entry(self)
        self.hora_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Botones de acción
        tk.Button(self, text="Nuevo", command=self.new_schedule).grid(row=4, column=0, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Guardar", command=self.save_schedule).grid(row=4, column=1, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Cancelar", command=self.clear_fields).grid(row=4, column=2, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Editar", command=self.update_schedule).grid(row=4, column=3, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Baja", command=self.delete_schedule).grid(row=4, column=4, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Volver al Menú Principal", command=self.show_main_menu).grid(row=5, column=0, columnspan=5, pady=20)

                
    def new_schedule(self):
        self.clear_fields()


    def search_schedule(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        codigo = self.search_entry.get()

        cursor.execute("SELECT * FROM Horarios WHERE id_horario = %s", (codigo,))
        horario = cursor.fetchone()
        conexion.close()

        if horario:
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, horario[0])

            self.turno_combobox.set(horario[1])
            self.hora_entry.delete(0, tk.END)
            self.hora_entry.insert(0, horario[2])
        else:
            messagebox.showerror("Error", "Horario no encontrado")


    def save_schedule(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()

        datos_horario = (
            self.turno_combobox.get(),
            self.hora_entry.get()
        )

        try:
            cursor.execute("""
                INSERT INTO Horarios (turno, hora) 
                VALUES (%s, %s)
            """, datos_horario)
            conexion.commit()
            messagebox.showinfo("Guardar", "Horario guardado exitosamente")
        except mysql.connector.IntegrityError as e:
            messagebox.showerror("Error", f"Error al guardar el horario: {e}")
        finally:
            conexion.close()
            self.clear_fields()
        

    def delete_schedule(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        id_horario = self.id_entry.get()
        cursor.execute("DELETE FROM Horarios WHERE id_horario = %s", (id_horario,))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Eliminar", "Horario eliminado exitosamente")
        self.clear_fields()


    def update_schedule(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()

        datos_horario = (
            self.turno_combobox.get(),
            self.hora_entry.get(),
            self.id_entry.get()
        )

        cursor.execute("""
            UPDATE Horarios SET turno=%s, hora=%s WHERE id_horario=%s
        """, datos_horario)
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Actualizar", "Horario actualizado exitosamente")
        self.clear_fields()

    def clear_fields(self):
        self.id_entry.delete(0, tk.END)
        self.turno_combobox.set("")
        self.hora_entry.delete(0, tk.END)


    def classroom_menu(self):
        self.geometry("300x400")
        messagebox.showinfo("Salón", "Funcionalidad de Salón no implementada.")

    def career_menu(self):
        # Limpiar la ventana y ajustar el tamaño
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("600x400")
        
        self.title("Sistema de Control Escolar - Carrera")

        # Campos de búsqueda
        tk.Label(self, text="Ingrese código carrera:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.search_entry = tk.Entry(self)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Button(self, text="Buscar", command=self.search_career).grid(row=0, column=2, padx=5, pady=5)

        # Campos del formulario
        tk.Label(self, text="ID:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.id_entry = tk.Entry(self)
        self.id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Nombre carrera:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.nombre_carrera_entry = tk.Entry(self)
        self.nombre_carrera_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Número semestres:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.num_semestres_entry = tk.Entry(self)
        self.num_semestres_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Botones de acción
        tk.Button(self, text="Nuevo", command=self.new_career).grid(row=4, column=0, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Guardar", command=self.save_career).grid(row=4, column=1, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Cancelar", command=self.clear_fields).grid(row=4, column=2, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Editar", command=self.update_career).grid(row=4, column=3, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Baja", command=self.delete_career).grid(row=4, column=4, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Volver al Menú Principal", command=self.show_main_menu).grid(row=5, column=0, columnspan=5, pady=20)

    def search_career(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        codigo = self.search_entry.get()

        cursor.execute("SELECT * FROM Carreras WHERE id_carrera = %s", (codigo,))
        carrera = cursor.fetchone()
        conexion.close()

        if carrera:
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, carrera[0])

            self.nombre_carrera_entry.delete(0, tk.END)
            self.nombre_carrera_entry.insert(0, carrera[1])

            self.num_semestres_entry.delete(0, tk.END)
            self.num_semestres_entry.insert(0, carrera[2])
        else:
            messagebox.showerror("Error", "Carrera no encontrada")

    def save_career(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()

        datos_carrera = (
            self.nombre_carrera_entry.get(),
            self.num_semestres_entry.get()
        )

        try:
            cursor.execute("""
                INSERT INTO Carreras (nombre_carrera, semestres) 
                VALUES (%s, %s)
            """, datos_carrera)
            conexion.commit()
            messagebox.showinfo("Guardar", "Carrera guardada exitosamente")
        except mysql.connector.IntegrityError as e:
            messagebox.showerror("Error", f"Error al guardar la carrera: {e}")
        finally:
            conexion.close()
            self.clear_fields()

    def update_career(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()

        datos_carrera = (
            self.nombre_carrera_entry.get(),
            self.num_semestres_entry.get(),
            self.id_entry.get()
        )

        cursor.execute("""
            UPDATE Carreras SET nombre_carrera=%s, num_semestres=%s WHERE id_carrera=%s
        """, datos_carrera)
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Actualizar", "Carrera actualizada exitosamente")
        self.clear_fields()

    def delete_career(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        id_carrera = self.id_entry.get()
        cursor.execute("DELETE FROM Carreras WHERE id_carrera = %s", (id_carrera,))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Eliminar", "Carrera eliminada exitosamente")
        self.clear_fields()
  
    def new_career(self):
        self.clear_fields()

    def clear_fields(self):
        self.id_entry.delete(0, tk.END)
        self.nombre_carrera_entry.delete(0, tk.END)
        self.num_semestres_entry.delete(0, tk.END)


    def planning_menu(self):
        self.geometry("300x400")
        messagebox.showinfo("Planeación", "Funcionalidad de Planeación no implementada.")

if __name__ == "__main__":
    app = SchoolControlApp()
    app.mainloop()
