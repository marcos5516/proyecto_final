import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox, ttk


# Conexión a la base de datos
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="SistemaControlEscolar"
    )

class SchoolControlApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Control Escolar - Login")
        self.geometry("300x240")  # Tamaño inicial para la pantalla de login
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
        self.user_entry.pack(pady=(0, 20))
        tk.Label(self, text="Contraseña:").pack(pady=(0, 5))
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=(0, 20))
        tk.Button(self, text="Login", command=self.authenticate_user).pack(pady=(0, 20))

    def authenticate_user(self):
        user_input = self.user_entry.get()  # Puede ser correo o nombre de usuario
        contraseña = self.password_entry.get()

        conexion = conectar_bd()
        if conexion:
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

    def save_data(self):
        # Lógica para guardar datos en la base de datos
        connection = conectar_bd()
        if connection:
            cursor = connection.cursor()
            try:
                # Ejemplo de inserción de datos
                cursor.execute("INSERT INTO tabla (campo1, campo2) VALUES (%s, %s)", (self.user_entry.get(), self.password_entry.get()))
                connection.commit()
                messagebox.showinfo("Éxito", "Datos guardados correctamente")
                self.clear_fields()
            except Error as e:
                messagebox.showerror("Error", f"No se pudieron guardar los datos: {e}")
            finally:
                cursor.close()
                connection.close()

    def clear_fields(self):
        # Limpiar los campos de entrada
        self.user_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        self.asignatura_entry.delete(0, tk.END)
        self.carrera_combobox.set('')
        self.creditos_entry.delete(0, tk.END)
        self.semestre_entry.delete(0, tk.END)

    def load_user_data(self, user):
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
        self.geometry("750x400")
        
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
        tk.Button(self, text="Cancelar", command=self.clear_user_fields).grid(row=6, column=2, padx=5, pady=10, sticky="w")
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
            self.load_user_data(user)
        else:
            messagebox.showerror("Error", "Usuario no encontrado")
            
    def new_user(self):
        self.clear_user_fields(self.id_entry, self.nombre_entry, self.apaterno_entry, self.amaterno_entry, self.username_entry, self.password_entry, self.perfil_combobox)

    def save_user(self):
        connection = conectar_bd()
        if connection:
            cursor = connection.cursor()
            try:
                # Obtener los valores de los campos de entrada
                id_usuario = self.id_entry.get() if hasattr(self, 'id_entry') else None
                correo = self.correo_entry.get() if hasattr(self, 'correo_entry') else None
                contraseña = self.password_entry.get() if hasattr(self, 'password_entry') else None
                perfil = self.perfil_combobox.get() if hasattr(self, 'perfil_combobox') else None
                nombre_usuario = self.username_entry.get() if hasattr(self, 'username_entry') else None
                nombre = self.nombre_entry.get() if hasattr(self, 'nombre_entry') else None
                apellido_paterno = self.apaterno_entry.get() if hasattr(self, 'apaterno_entry') else None
                apellido_materno = self.amaterno_entry.get() if hasattr(self, 'amaterno_entry') else None
                estado = "Activo"

                # Generar el correo automáticamente si no se proporciona
                if not correo:
                    correo = f"{nombre_usuario}@alumnos.com"

                # Verificar si el ID de usuario ya existe
                cursor.execute("SELECT COUNT(*) FROM Usuarios WHERE id_usuario = %s", (id_usuario,))
                if cursor.fetchone()[0] > 0:
                    messagebox.showerror("Error", "El ID de usuario ya existe")
                    return

                # Insertar el usuario en la base de datos
                cursor.execute("""
                    INSERT INTO Usuarios (id_usuario, correo, contraseña, perfil, nombre_usuario, nombre, apellido_paterno, apellido_materno)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (id_usuario, correo, contraseña, perfil, nombre_usuario, nombre, apellido_paterno, apellido_materno))
                connection.commit()

                # Si el perfil es Alumno, insertar en la tabla Alumnos
                if perfil == 'Alumno':
                    cursor.execute("""
                        INSERT INTO Alumnos (id_usuario, estado)
                        VALUES (%s, %s)
                    """, (id_usuario, estado))
                    connection.commit()
                if perfil == 'Maestro':
                    cursor.execute("""
                        INSERT INTO Maestros (id_usuario)
                        VALUES (%s)
                    """, (id_usuario,))
                    connection.commit()
                messagebox.showinfo("Éxito", "Usuario guardado correctamente")
            except Error as e:
                messagebox.showerror("Error", f"No se pudo guardar el usuario: {e}")
            finally:
                cursor.close()
                connection.close()

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
        self.clear_user_fields()

    def delete_user(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        id_usuario = self.id_entry.get()
        cursor.execute("DELETE FROM Usuarios WHERE id_usuario = %s", (id_usuario,))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Eliminar", "Usuario eliminado exitosamente")
        self.clear_user_fields()

    def clear_user_fields(self, *fields):
        for field in fields:
            if isinstance(field, tk.Entry):
                field.delete(0, tk.END)
            elif isinstance(field, ttk.Combobox):
                field.set("")
            elif isinstance(field, tk.Listbox):
                field.selection_clear(0, tk.END)

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
        tk.Button(self, text="Cancelar", command=self.clear_student_fields).grid(row=12, column=2, padx=5, pady=10, sticky="w")
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
        materia_nombre = self.materia_combobox.get()
        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_materia FROM Materias WHERE nombre_materia = %s", (materia_nombre,))
        id_materia = cursor.fetchone()[0]
        conexion.close()

        # Verificar si el alumno ya está inscrito en la materia
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="SistemaControlEscolar"
        )
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM Alumno_Materia WHERE id_alumno = %s AND id_materia = %s", (id_alumno, id_materia))
        if cursor.fetchone()[0] > 0:
            print("El alumno ya está inscrito en esta materia.")
            cursor.close()
            conexion.close()
            return

        try:
            # Insertar la materia para el alumno
            cursor.execute("INSERT INTO Alumno_Materia (id_alumno, id_materia) VALUES (%s, %s)", (id_alumno, id_materia))

            # Restar el cupo disponible
            cursor.execute("UPDATE Materias SET cupos_disponibles = cupos_disponibles - 1 WHERE id_materia = %s", (id_materia,))

            # Confirmar los cambios
            conexion.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            conexion.rollback()

        finally:
            # Cerrar la conexión
            cursor.close()
            conexion.close()

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
        self.clear_student_fields()
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
            self.clear_student_fields()

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
        self.clear_student_fields()

    def delete_student(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        id_alumno = self.id_entry.get()
        cursor.execute("DELETE FROM Alumnos WHERE id_alumno = %s", (id_alumno,))
        cursor.execute("DELETE FROM Usuarios WHERE id_usuario = (SELECT id_usuario FROM Alumnos WHERE id_alumno = %s)", (id_alumno,))
        
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Eliminar", "Alumno eliminado exitosamente")
        self.clear_student_fields()

    def clear_student_fields(self):
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
        # Limpiar la ventana y ajustar el tamaño
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("800x600")
        
        self.title("Sistema de Control Escolar - Maestros")

        # Campos de búsqueda
        tk.Label(self, text="Ingrese código maestro:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.codigo_entry = tk.Entry(self, width=30)
        self.codigo_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        tk.Button(self, text="Buscar", width=10, command=self.search_teacher).grid(row=0, column=2, padx=10, pady=10)

        # Campos del formulario
        tk.Label(self, text="ID:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.id_entry = tk.Entry(self, width=30)
        self.id_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self, text="Nombre:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.nombre_entry = tk.Entry(self, width=30)
        self.nombre_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self, text="A Paterno:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.paterno_entry = tk.Entry(self, width=30)
        self.paterno_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self, text="A Materno:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.materno_entry = tk.Entry(self, width=30)
        self.materno_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self, text="Email:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.email_entry = tk.Entry(self, width=30)
        self.email_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self, text="Carrera:").grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.carrera_combo = ttk.Combobox(self, width=25, state="readonly")
        self.carrera_combo.grid(row=6, column=1, padx=10, pady=10, sticky="w")
        self.carrera_combo.bind("<<ComboboxSelected>>", self.load_materias)

        tk.Label(self, text="Materias:").grid(row=7, column=0, padx=10, pady=10, sticky="e")
        self.materia_listbox = tk.Listbox(self, selectmode="multiple", height=5)
        self.materia_listbox.grid(row=7, column=1, rowspan=3, padx=10, pady=10, sticky="w")

        # Botones de acción
        tk.Button(self, text="Nuevo", width=10, command=self.new_teacher).grid(row=10, column=0, padx=10, pady=20)
        tk.Button(self, text="Guardar", width=10, command=self.save_teacher).grid(row=10, column=1, padx=10, pady=20)
        tk.Button(self, text="Cancelar", width=10, command=self.clear_teacher_fields).grid(row=10, column=2, padx=10, pady=20)
        tk.Button(self, text="Volver al Menú Principal", command=self.show_main_menu).grid(row=11, column=0, columnspan=3, pady=20)

        self.load_carreras()

    def load_carreras(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre_carrera FROM Carreras")
        carreras = [row[0] for row in cursor.fetchall()]
        self.carrera_combo["values"] = carreras
        cursor.close()
        conexion.close()

    def load_materias(self, event=None):
        carrera = self.carrera_combo.get()
        if not carrera:
            return

        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT m.nombre_materia
            FROM Materias m
            JOIN Carreras c ON m.id_carrera = c.id_carrera
            WHERE c.nombre_carrera = %s
        """, (carrera,))
        materias = [row[0] for row in cursor.fetchall()]
        self.materia_listbox.delete(0, tk.END)
        for materia in materias:
            self.materia_listbox.insert(tk.END, materia)
        cursor.close()
        conexion.close()

    def new_teacher(self):
        self.clear_teacher_fields()

    def save_teacher(self):
        nombre = self.nombre_entry.get()
        paterno = self.paterno_entry.get()
        materno = self.materno_entry.get()
        email = self.email_entry.get()
        carrera = self.carrera_combo.get()
        materias = [self.materia_listbox.get(i) for i in self.materia_listbox.curselection()]

        if not nombre or not paterno or not materno or not email or not carrera or not materias:
            print("Todos los campos son obligatorios.")
            return

        conexion = conectar_bd()
        cursor = conexion.cursor()

        try:
            # Insertar en la tabla Usuarios
            cursor.execute("INSERT INTO Usuarios (correo, contraseña, perfil, nombre, apellido_paterno, apellido_materno) VALUES (%s, %s, %s, %s, %s, %s)",
                           (email, '123', 'Maestro', nombre, paterno, materno))
            id_usuario = cursor.lastrowid

            # Obtener id_carrera
            cursor.execute("SELECT id_carrera FROM Carreras WHERE nombre_carrera = %s", (carrera,))
            id_carrera = cursor.fetchone()[0]

            # Insertar en la tabla Maestros
            cursor.execute("INSERT INTO Maestros (id_usuario, id_carrera) VALUES (%s, %s)", (id_usuario, id_carrera))
            id_maestro = cursor.lastrowid

            # Asignar materias al maestro
            for materia in materias:
                cursor.execute("SELECT id_materia FROM Materias WHERE nombre_materia = %s", (materia,))
                id_materia = cursor.fetchone()[0]
                cursor.execute("INSERT INTO Maestro_Materia (id_maestro, id_materia) VALUES (%s, %s)", (id_maestro, id_materia))

            conexion.commit()
            print("Maestro guardado exitosamente.")
            messagebox.showinfo("Éxito", "Maestro guardado exitosamente")

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            conexion.rollback()
            messagebox.showerror("Error", f"No se pudo guardar el maestro: {err}")

        finally:
            cursor.close()
            conexion.close()

    def clear_teacher_fields(self):
        self.nombre_entry.delete(0, tk.END)
        self.paterno_entry.delete(0, tk.END)
        self.materno_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.carrera_combo.set("")
        self.materia_listbox.selection_clear(0, tk.END)

    def search_teacher(self): 
        connection = conectar_bd()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    SELECT Usuarios.*
                    FROM Maestros
                    JOIN Usuarios ON Maestros.id_usuario = Usuarios.id_usuario
                    WHERE Maestros.id_maestro = %s
                """, (self.codigo_entry.get(),))
                maestro = cursor.fetchone()
                if maestro:
                    self.asignar_datos_maestro(maestro)
                else:
                    messagebox.showerror("Error", "Maestro no encontrado")
            except Error as e:
                messagebox.showerror("Error", f"No se pudo buscar el maestro: {e}")
            finally:
                cursor.close()
                connection.close()

    def update_teacher(self):
        connection = conectar_bd()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    UPDATE Maestros SET nombre = %s, apellido_paterno = %s, apellido_materno = %s, correo = %s, carrera = %s, grado_estudios = %s
                    WHERE id_maestro = %s
                """, (self.nombre_entry.get(), self.paterno_entry.get(), self.materno_entry.get(), self.email_entry.get(), self.carrera_combo.get(), self.grado_entry.get(), self.id_entry.get()))
                connection.commit()
                messagebox.showinfo("Éxito", "Maestro actualizado correctamente")
            except Error as e:
                messagebox.showerror("Error", f"No se pudo actualizar el maestro: {e}")
            finally:
                cursor.close()
                connection.close()

    def delete_teacher(self):
        connection = conectar_bd()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("DELETE FROM Maestros WHERE id_maestro = %s", (self.id_entry.get(),))
                connection.commit()
                messagebox.showinfo("Éxito", "Maestro eliminado correctamente")
            except Error as e:
                messagebox.showerror("Error", f"No se pudo eliminar el maestro: {e}")
            finally:
                cursor.close()
                connection.close()

    def asignar_datos_maestro(self, maestro):
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, maestro[0])  # id_usuario
        self.nombre_entry.delete(0, tk.END)
        self.nombre_entry.insert(0, maestro[5])  # nombre
        self.paterno_entry.delete(0, tk.END)
        self.paterno_entry.insert(0, maestro[6])  # apellido_paterno
        self.materno_entry.delete(0, tk.END)
        self.materno_entry.insert(0, maestro[7])  # apellido_materno
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, maestro[1])  # correo

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

        tk.Label(self, text="Cupos:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.cupos_entry = tk.Entry(self)
        self.cupos_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # Botones de acción
        tk.Button(self, text="Nuevo", command=self.new_subject).grid(row=7, column=0, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Guardar", command=self.save_subject).grid(row=7, column=1, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Cancelar", command=self.clear_subject_fields).grid(row=7, column=2, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Editar", command=self.update_subject).grid(row=7, column=3, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Baja", command=self.delete_subject).grid(row=7, column=4, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Volver al Menú Principal", command=self.show_main_menu).grid(row=8, column=0, columnspan=5, pady=20)

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

            # Obtener nombre de carrera basado en id_carrera
            conexion = conectar_bd()
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre_carrera FROM Carreras WHERE id_carrera = %s", (materia[2],))
            carrera = cursor.fetchone()
            conexion.close()

            if carrera:
                self.carrera_combobox.set(carrera[0])
            else:
                self.carrera_combobox.set('')

            self.creditos_entry.delete(0, tk.END)
            self.creditos_entry.insert(0, materia[3])

            self.semestre_entry.delete(0, tk.END)
            self.semestre_entry.insert(0, materia[4])

            self.cupos_entry.delete(0, tk.END)
            self.cupos_entry.insert(0, materia[5])
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
                self.id_entry.get(),
                self.asignatura_entry.get(),
                id_carrera,
                self.creditos_entry.get(),
                self.semestre_entry.get(),
                self.cupos_entry.get()
            )

            try:
                cursor.execute("""
                    INSERT INTO Materias (id_materia, nombre_materia, id_carrera, creditos, semestre, cupo_maximo) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, datos_materia)
                conexion.commit()
                messagebox.showinfo("Guardar", "Materia guardada exitosamente")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error al guardar la materia: {e}")
            finally:
                conexion.close()
                self.clear_subject_fields()
        else:
            messagebox.showerror("Error", "Carrera no encontrada en la base de datos")

    def update_subject(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()

        # Obtener id_carrera basado en nombre de la carrera seleccionada
        carrera_nombre = self.carrera_combobox.get()
        cursor.execute("SELECT id_carrera FROM Carreras WHERE nombre_carrera = %s", (carrera_nombre,))
        carrera = cursor.fetchone()

        if carrera:
            id_carrera = carrera[0]
            datos_materia = (
                self.asignatura_entry.get(),
                id_carrera,
                self.creditos_entry.get(),
                self.semestre_entry.get(),
                self.cupos_entry.get(),
                self.id_entry.get()
            )

            cursor.execute("""
                UPDATE Materias SET nombre_materia=%s, id_carrera=%s, creditos=%s, semestre=%s, cupo_maximo=%s 
                WHERE id_materia=%s
            """, datos_materia)
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Actualizar", "Materia actualizada exitosamente")
            self.clear_subject_fields()
        else:
            conexion.close()
            messagebox.showerror("Error", "Carrera no encontrada en la base de datos")

    def delete_subject(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        id_materia = self.id_entry.get()
        cursor.execute("DELETE FROM Materias WHERE id_materia = %s", (id_materia,))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Eliminar", "Materia eliminada exitosamente")
        self.clear_subject_fields()

    def new_subject(self):
        self.clear_subject_fields()

    def clear_subject_fields(self):
        if hasattr(self, 'id_entry'):
            self.id_entry.delete(0, tk.END)
        if hasattr(self, 'asignatura_entry'):
            self.asignatura_entry.delete(0, tk.END)
        if hasattr(self, 'carrera_combobox'):
            self.carrera_combobox.set("")
        if hasattr(self, 'creditos_entry'):
            self.creditos_entry.delete(0, tk.END)
        if hasattr(self, 'semestre_entry'):
            self.semestre_entry.delete(0, tk.END)
        if hasattr(self, 'cupos_entry'):
            self.cupos_entry.delete(0, tk.END)

    def mostrar_grupos_materia(self):
        materia_nombre = self.materia_combobox.get()
        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT g.nombre_grupo, g.fecha, c.nombre_carrera, m.nombre_materia, g.salon, g.horario, g.semestre, g.max_alumnos, g.alumnos_inscritos
            FROM Grupos g
            JOIN Materias m ON g.materia = m.id_materia
            JOIN Carreras c ON g.carrera = c.id_carrera
            WHERE m.nombre_materia = %s
        """, (materia_nombre,))
        grupos = cursor.fetchall()
        conexion.close()

        for grupo in grupos:
            print(f"Grupo: {grupo[0]}, Fecha: {grupo[1]}, Carrera: {grupo[2]}, Materia: {grupo[3]}, Salón: {grupo[4]}, Horario: {grupo[5]}, Semestre: {grupo[6]}, Máx. Alumnos: {grupo[7]}, Alumnos Inscritos: {grupo[8]}")

    def groups_menu(self):
        # Limpiar la ventana y ajustar el tamaño
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("600x500")
        
        self.title("Sistema de Control Escolar - Grupos")

        # Campo de búsqueda
        tk.Label(self, text="Ingrese código grupo:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.search_entry = tk.Entry(self)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Button(self, text="Buscar", command=self.search_group).grid(row=0, column=2, padx=5, pady=5)

        # Campos del formulario (solo lectura)
        tk.Label(self, text="ID:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.id_entry = tk.Entry(self, state='readonly')
        self.id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Nombre grupo:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.nombre_grupo_entry = tk.Entry(self, state='readonly')
        self.nombre_grupo_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Fecha:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.fecha_entry = tk.Entry(self, state='readonly')
        self.fecha_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Carrera:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.carrera_entry = tk.Entry(self, state='readonly')
        self.carrera_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Materia:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.materia_entry = tk.Entry(self, state='readonly')
        self.materia_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Salón:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.salon_entry = tk.Entry(self, state='readonly')
        self.salon_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Horario:").grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.horario_entry = tk.Entry(self, state='readonly')
        self.horario_entry.grid(row=7, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Semestre:").grid(row=8, column=0, padx=5, pady=5, sticky="e")
        self.semestre_entry = tk.Entry(self, state='readonly')
        self.semestre_entry.grid(row=8, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Máx num Alumnos:").grid(row=9, column=0, padx=5, pady=5, sticky="e")
        self.max_alumnos_entry = tk.Entry(self, state='readonly')
        self.max_alumnos_entry.grid(row=9, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Maestro:").grid(row=10, column=0, padx=5, pady=5, sticky="e")
        self.maestro_entry = tk.Entry(self, state='readonly')
        self.maestro_entry.grid(row=10, column=1, padx=5, pady=5, sticky="w")

        # Botón para volver al menú principal
        tk.Button(self, text="Volver al Menú Principal", command=self.show_main_menu).grid(row=11, column=0, columnspan=3, pady=20)

    def search_group(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        codigo = self.search_entry.get()

        cursor.execute("""
            SELECT g.id_grupo, g.nombre_grupo, c.nombre_carrera, m.nombre_materia, s.nombre_salon, h.hora, g.semestre, g.max_alumnos, u.nombre, u.apellido_paterno, u.apellido_materno
            FROM Grupos g
            JOIN Carreras c ON g.carrera = c.id_carrera
            JOIN Materias m ON g.materia = m.id_materia
            JOIN Salones s ON g.salon = s.id_salon
            JOIN Horarios h ON g.horario = h.id_horario
            JOIN Maestros ma ON g.maestro = ma.id_maestro
            JOIN Usuarios u ON ma.id_usuario = u.id_usuario
            WHERE g.id_grupo = %s
        """, (codigo,))
        result = cursor.fetchone()
        if result:
            # Asignar los valores a los campos correspondientes
            self.id_grupo_entry.delete(0, tk.END)
            self.id_grupo_entry.insert(0, result[0])
            self.nombre_grupo_entry.delete(0, tk.END)
            self.nombre_grupo_entry.insert(0, result[1])
            self.carrera_entry.delete(0, tk.END)
            self.carrera_entry.insert(0, result[2])
            self.materia_entry.delete(0, tk.END)
            self.materia_entry.insert(0, result[3])
            self.salon_entry.delete(0, tk.END)
            self.salon_entry.insert(0, result[4])
            self.horario_entry.delete(0, tk.END)
            self.horario_entry.insert(0, result[5])
            self.semestre_entry.delete(0, tk.END)
            self.semestre_entry.insert(0, result[6])
            self.max_alumnos_entry.delete(0, tk.END)
            self.max_alumnos_entry.insert(0, result[7])
            self.maestro_entry.delete(0, tk.END)
            self.maestro_entry.insert(0, f"{result[8]} {result[9]} {result[10]}")
        else:
            messagebox.showinfo("Buscar", "Grupo no encontrado")
        cursor.close()
        conexion.close()

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
        tk.Button(self, text="Cancelar", command=self.clear_schedule_fields).grid(row=4, column=2, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Editar", command=self.update_schedule).grid(row=4, column=3, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Baja", command=self.delete_schedule).grid(row=4, column=4, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Volver al Menú Principal", command=self.show_main_menu).grid(row=5, column=0, columnspan=5, pady=20)

                
    def new_schedule(self):
        self.clear_schedule_fields()


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
            self.clear_schedule_fields()
        

    def delete_schedule(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        id_horario = self.id_entry.get()
        cursor.execute("DELETE FROM Horarios WHERE id_horario = %s", (id_horario,))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Eliminar", "Horario eliminado exitosamente")
        self.clear_schedule_fields()


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
        self.clear_schedule_fields()

    def clear_schedule_fields(self):
        self.id_entry.delete(0, tk.END)
        self.turno_combobox.set("")
        self.hora_entry.delete(0, tk.END)


    def classroom_menu(self):
        # Limpiar la ventana y ajustar el tamaño
        for widget in self.winfo_children():
            widget.destroy()
        self.geometry("600x400")
        
        self.title("Sistema de Control Escolar - Salón")

        # Campos de búsqueda
        tk.Label(self, text="Ingrese código salón:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.search_entry = tk.Entry(self)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Button(self, text="Buscar", command=lambda: self.buscar_salon(self.search_entry.get())).grid(row=0, column=2, padx=5, pady=5)

        # Campos del formulario
        tk.Label(self, text="ID:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.id_entry = tk.Entry(self)
        self.id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Nombre salón:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.nombre_entry = tk.Entry(self)
        self.nombre_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Edificio:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.edificio_combo = ttk.Combobox(self, values=["Edificio A", "Edificio B", "Edificio C", "Edificio D"])
        self.edificio_combo.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Botones de acción
        tk.Button(self, text="Nuevo", command=self.nuevo_salon).grid(row=4, column=0, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Guardar", command=self.guardar_salon).grid(row=4, column=1, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Cancelar", command=self.cancelar).grid(row=4, column=2, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Editar", command=self.editar_salon).grid(row=4, column=3, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Baja", command=self.baja_salon).grid(row=4, column=4, padx=5, pady=10, sticky="w")
        tk.Button(self, text="Volver al Menú Principal", command=self.show_main_menu).grid(row=5, column=0, columnspan=5, pady=20)


    def nuevo_salon(self):
        self.id_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.edificio_combo.set('')

    def guardar_salon(self):
        nombre_salon = self.nombre_entry.get()
        if nombre_salon:
            self.cursor.execute("INSERT INTO Salones (nombre_salon) VALUES (?)", (nombre_salon,))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Salón guardado exitosamente")
        else:
            messagebox.showerror("Error", "El nombre del salón no puede estar vacío")

    def buscar_salon(self, codigo_salon):
        self.cursor.execute("SELECT * FROM Salones WHERE id_salon=?", (codigo_salon,))
        salon = self.cursor.fetchone()
        if salon:
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, salon[0])
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, salon[1])
        else:
            messagebox.showerror("Error", "Salón no encontrado")

    def editar_salon(self):
        id_salon = self.id_entry.get()
        nombre_salon = self.nombre_entry.get()
        if id_salon and nombre_salon:
            self.cursor.execute("UPDATE Salones SET nombre_salon=? WHERE id_salon=?", (nombre_salon, id_salon))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Salón actualizado exitosamente")
        else:
            messagebox.showerror("Error", "Debe ingresar el ID y el nombre del salón")

    def baja_salon(self):
        id_salon = self.id_entry.get()
        if id_salon:
            self.cursor.execute("DELETE FROM Salones WHERE id_salon=?", (id_salon,))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Salón eliminado exitosamente")
        else:
            messagebox.showerror("Error", "Debe ingresar el ID del salón")

    def cancelar(self):
        self.nuevo_salon()

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
        tk.Button(self, text="Cancelar", command=self.clear_career_fields).grid(row=4, column=2, padx=5, pady=10, sticky="w")
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
            self.clear_career_fields()

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
        self.clear_career_fields()

    def delete_career(self):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        id_carrera = self.id_entry.get()
        cursor.execute("DELETE FROM Carreras WHERE id_carrera = %s", (id_carrera,))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Eliminar", "Carrera eliminada exitosamente")
        self.clear_career_fields()
  
    def new_career(self):
        self.clear_career_fields()

    def clear_career_fields(self):
        self.id_entry.delete(0, tk.END)
        self.nombre_carrera_entry.delete(0, tk.END)
        self.num_semestres_entry.delete(0, tk.END)


    def planning_menu(self):
        root = tk.Tk()
        root.title("Control Escolar - Planeación")
        root.geometry("800x500")  # Ajusta el tamaño de la ventana

        # Crear una estructura en blanco para la planeación
        tk.Label(root, text="Planeación", font=("Arial", 16)).pack(pady=10)

        # Frame para organizar la cuadrícula de planeación
        planeacion_frame = tk.Frame(root, relief="solid", borderwidth=1)
        planeacion_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Obtener los grupos y horarios de la base de datos
        self.cursor.execute("""
            SELECT G.nombre_grupo, G.horario, M.nombre_materia, S.nombre_salon
            FROM Grupos G
            JOIN Materias M ON G.materia = M.id_materia
            JOIN Salones S ON G.salon = S.id_salon
            ORDER BY G.horario
        """)
        grupos = self.cursor.fetchall()

        # Crear la cuadrícula de planeación (4x4 como ejemplo)
        for row in range(4):
            for col in range(4):
                frame = tk.Frame(
                    planeacion_frame, 
                    relief="solid", 
                    borderwidth=1, 
                    width=150, 
                    height=100
                )
                frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                planeacion_frame.grid_columnconfigure(col, weight=1)
                planeacion_frame.grid_rowconfigure(row, weight=1)

                # Mostrar los grupos en la cuadrícula
                if grupos:
                    grupo = grupos.pop(0)
                    tk.Label(frame, text=f"Grupo: {grupo[0]}\nHorario: {grupo[1]}\nMateria: {grupo[2]}\nSalón: {grupo[3]}").pack()

    def add_student_to_subject(self):
        connection = conectar_bd()
        if connection:
            cursor = connection.cursor()
            try:
                # Insertar el alumno en la materia
                cursor.execute("""
                    INSERT INTO Alumno_Materia (id_alumno, id_materia)
                    VALUES (%s, %s)
                """, (self.id_alumno_entry.get(), self.id_materia_entry.get()))
                connection.commit()
                messagebox.showinfo("Éxito", "Alumno añadido a la materia correctamente")
            except Error as e:
                messagebox.showerror("Error", f"No se pudo añadir el alumno a la materia: {e}")
            finally:
                cursor.close()
                connection.close()

if __name__ == "__main__":
    app = SchoolControlApp()
    app.mainloop()


