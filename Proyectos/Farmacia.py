import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from fpdf import FPDF

# Conectar con la base de datos MySQL
def conectar_bd():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="farmacia_cucei"
    )
    return conexion

# Función para gestionar usuarios (CRUD)
def gestionar_usuarios():
    ventana_usuarios = tk.Toplevel(ventana)
    ventana_usuarios.title("Gestionar Usuarios")
    
    # Obtener usuarios desde la base de datos
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, usuario, rol FROM Usuarios")
    usuarios = cursor.fetchall()
    conexion.close()

    # Mostrar los usuarios en la interfaz
    tree = ttk.Treeview(ventana_usuarios, columns=("ID", "Usuario", "Rol"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Usuario", text="Usuario")
    tree.heading("Rol", text="Rol")
    tree.pack()

    for usr in usuarios:
        tree.insert("", tk.END, values=usr)

    btn_agregar = tk.Button(ventana_usuarios, text="Agregar Usuario", command=agregar_usuario)
    btn_agregar.pack()
    btn_modificar = tk.Button(ventana_usuarios, text="Modificar Usuario", command=lambda: modificar_usuario(tree))
    btn_modificar.pack()
    btn_eliminar = tk.Button(ventana_usuarios, text="Eliminar Usuario", command=lambda: eliminar_usuario(tree))
    btn_eliminar.pack()

# Función para agregar un nuevo usuario
def agregar_usuario():
    ventana_nuevo_usuario = tk.Toplevel(ventana)
    ventana_nuevo_usuario.title("Agregar Usuario")

    tk.Label(ventana_nuevo_usuario, text="Nombre de Usuario:").pack()
    entry_nombre = tk.Entry(ventana_nuevo_usuario)
    entry_nombre.pack()

    tk.Label(ventana_nuevo_usuario, text="Contraseña:").pack()
    entry_password = tk.Entry(ventana_nuevo_usuario, show="*")
    entry_password.pack()

    tk.Label(ventana_nuevo_usuario, text="Rol:").pack()
    combo_rol = ttk.Combobox(ventana_nuevo_usuario, values=["Admin", "Gerente", "Cajero"])
    combo_rol.pack()

    def guardar_usuario():
        nombre = entry_nombre.get()
        password = entry_password.get()
        rol = combo_rol.get()

        if nombre and password and rol:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            query = "INSERT INTO Usuarios (usuario, password, rol) VALUES (%s, %s, %s)"
            cursor.execute(query, (nombre, password, rol))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
            ventana_nuevo_usuario.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    tk.Button(ventana_nuevo_usuario, text="Guardar", command=guardar_usuario).pack()

# Función para modificar un usuario existente
def modificar_usuario(tree):
    seleccion = tree.focus()
    valores = tree.item(seleccion, "values")
    
    if not valores:
        messagebox.showerror("Error", "Seleccione un usuario para modificar")
        return

    ventana_mod_usuario = tk.Toplevel(ventana)
    ventana_mod_usuario.title("Modificar Usuario")
    
    tk.Label(ventana_mod_usuario, text="Nombre de Usuario:").pack()
    entry_nombre = tk.Entry(ventana_mod_usuario)
    entry_nombre.insert(0, valores[1])
    entry_nombre.pack()

    tk.Label(ventana_mod_usuario, text="Contraseña:").pack()
    entry_password = tk.Entry(ventana_mod_usuario, show="*")
    entry_password.pack()

    tk.Label(ventana_mod_usuario, text="Rol:").pack()
    combo_rol = ttk.Combobox(ventana_mod_usuario, values=["Admin", "Gerente", "Cajero"])
    combo_rol.set(valores[2])  # Asignar valor actual
    combo_rol.pack()

    def actualizar_usuario():
        nombre = entry_nombre.get()
        password = entry_password.get()
        rol = combo_rol.get()

        if nombre and rol:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            query = "UPDATE Usuarios SET usuario=%s, password=%s, rol=%s WHERE id=%s"
            cursor.execute(query, (nombre, password, rol, valores[0]))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Usuario modificado correctamente")
            ventana_mod_usuario.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    tk.Button(ventana_mod_usuario, text="Actualizar", command=actualizar_usuario).pack()

# Función para eliminar un usuario existente
def eliminar_usuario(tree):
    seleccion = tree.focus()
    valores = tree.item(seleccion, "values")

    if not valores:
        messagebox.showerror("Error", "Seleccione un usuario para eliminar")
        return

    confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este usuario?")
    if confirmar:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        query = "DELETE FROM Usuarios WHERE id=%s"
        cursor.execute(query, (valores[0],))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Usuario eliminado correctamente")

# Validar el login del usuario
def validar_login(usuario, password):
    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)
    query = "SELECT * FROM Usuarios WHERE usuario=%s AND password=%s"
    cursor.execute(query, (usuario, password))
    resultado = cursor.fetchone()
    conexion.close()
    return resultado

def obtener_productos():
    conexion = conectar_bd()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.id, p.nombre, i.precio, i.cantidad 
        FROM Productos p 
        JOIN Inventario i ON p.id = i.producto_id
    """)  # Join with Inventario to get price and quantity
    productos = cursor.fetchall()
    conexion.close()
    return productos

def agregar_producto_a_venta():
    producto_seleccionado = combo_producto.get()
    cantidad = entry_cantidad.get()

    if producto_seleccionado and cantidad:
        # Verificar si la cantidad ingresada es válida
        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0")
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad válida.")
            return

        # Buscar si el producto ya está en la lista
        for item in tree.get_children():
            item_values = tree.item(item, "values")
            producto_id_en_lista, producto_nombre_en_lista, cantidad_en_lista, importe_en_lista, subtotal_en_lista = item_values

            # Si el producto ya está en la lista, actualizamos la cantidad y el subtotal
            if producto_nombre_en_lista == producto_seleccionado:
                nueva_cantidad = int(cantidad_en_lista) + cantidad
                precio = float(importe_en_lista)  # Obtener el precio original
                nuevo_importe = precio * nueva_cantidad
                nuevo_subtotal = nuevo_importe * 1.16  # Aplicar IVA del 16%

                # Actualizar los valores en la tabla
                tree.item(item, values=(producto_id_en_lista, producto_seleccionado, nueva_cantidad, nuevo_importe, nuevo_subtotal))

                # Actualizar el total acumulado
                total_actual = float(label_total["text"])
                nuevo_total = total_actual + (precio * cantidad * 1.16)  # Subtotal con IVA
                label_total.config(text=f"{nuevo_total:.2f}")  # Formatear con dos decimales
                return

        # Si el producto no está en la lista, lo agregamos como una nueva entrada
        for producto in productos:
            if producto['nombre'] == producto_seleccionado:
                producto_id = producto['id']
                precio = float(producto['precio'])  # Convertir el precio a float
                cantidad_disponible = producto['cantidad']  # Cantidad en inventario

                # Verificar si hay suficiente inventario
                if cantidad > cantidad_disponible:
                    messagebox.showerror("Error", f"No hay suficiente inventario. Solo hay {cantidad_disponible} disponibles.")
                    return

                importe = precio * cantidad
                subtotal = importe * 1.16  # Aplicar IVA del 16%

                # Agregar el producto a la tabla de productos seleccionados
                tree.insert("", "end", values=(producto_id, producto_seleccionado, cantidad, importe, subtotal))
                
                # Actualizar el total acumulado
                total_actual = float(label_total["text"])
                nuevo_total = total_actual + subtotal  # Subtotal ya incluye IVA
                label_total.config(text=f"{nuevo_total:.2f}")  # Formatear con dos decimales
                break
    else:
        messagebox.showerror("Error", "Seleccione un producto y cantidad válidos.")

# Modify the buscar_cliente_por_nombre function
def buscar_cliente_por_nombre():
    clientes = obtener_clientes()
    return [cliente[1] for cliente in clientes]  # Return names instead of IDs


def registrar_venta():
    cliente_seleccionado = combo_cliente.get()
    dinero_cliente = entry_dinero_cliente.get()

    if cliente_seleccionado and dinero_cliente:
        dinero_cliente = float(dinero_cliente)
        total_venta = float(label_total["text"])  # Total con IVA incluido

        if dinero_cliente < total_venta:
            messagebox.showerror("Error", f"El dinero ingresado ({dinero_cliente}) no es suficiente para cubrir el total ({total_venta}).")
            return
        
        cambio = dinero_cliente - total_venta

        conexion = conectar_bd()
        cursor = conexion.cursor(dictionary=True)

        # Obtener el id del cliente por su nombre
        query_cliente = "SELECT id FROM Clientes WHERE nombre=%s"
        cursor.execute(query_cliente, (cliente_seleccionado,))
        cliente = cursor.fetchone()
        cliente_id = cliente['id'] if cliente else None

        if cliente_id:
            # Registrar la venta principal
            query_venta = "INSERT INTO Ventas (cliente_id, total) VALUES (%s, %s)"
            cursor.execute(query_venta, (cliente_id, total_venta))
            venta_id = cursor.lastrowid

            # Registrar los detalles de la venta
            for row in tree.get_children():
                producto_id, nombre, cantidad, importe, subtotal = tree.item(row, 'values')
                
                # Actualizar inventario en la tabla 'Inventario'
                query_inventario = "UPDATE Inventario SET cantidad = cantidad - %s WHERE producto_id = %s"
                cursor.execute(query_inventario, (cantidad, producto_id))

                query_detalle = "INSERT INTO DetalleVentas (venta_id, producto_id, cantidad, subtotal) VALUES (%s, %s, %s, %s)"
                cursor.execute(query_detalle, (venta_id, producto_id, cantidad, subtotal))

            # Aplicar y acumular puntos al cliente (1 punto por cada $100 gastados)
            puntos_a_sumar = int(total_venta // 100)
            query_puntos_cliente = "SELECT puntos FROM Clientes WHERE id = %s"
            cursor.execute(query_puntos_cliente, (cliente_id,))
            cliente = cursor.fetchone()

            if cliente:
                puntos_totales = cliente['puntos'] + puntos_a_sumar
                query_actualizar_puntos = "UPDATE Clientes SET puntos = %s WHERE id = %s"
                cursor.execute(query_actualizar_puntos, (puntos_totales, cliente_id))

            conexion.commit()
            conexion.close()

            # Reiniciar la interfaz
            tree.delete(*tree.get_children())
            label_total.config(text="0.00")
            combo_cliente.set('')
            entry_dinero_cliente.delete(0, tk.END)

            # Mostrar el mensaje final con puntos acumulados
            messagebox.showinfo("Venta registrada", f"Total a pagar: {total_venta}\nDinero recibido: {dinero_cliente}\nCambio: {cambio}\nPuntos acumulados: {puntos_totales}")
        else:
            messagebox.showerror("Error", "Cliente no encontrado.")
    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")

# Función para cancelar una venta
def cancelar_venta():
    if not tree.get_children():
        messagebox.showerror("Error", "No hay productos en la venta para cancelar.")
        return

    # Solo Gerente o Admin puede cancelar la venta
    if usuario_actual['rol'] == 'Cajero':
        login_gerente_admin = tk.Toplevel(ventana)
        login_gerente_admin.title("Confirmar Cancelación (Gerente/Admin)")
        login_gerente_admin.geometry("300x200")

        tk.Label(login_gerente_admin, text="Usuario:").pack(pady=5)
        entry_usuario_confirm = tk.Entry(login_gerente_admin)
        entry_usuario_confirm.pack(pady=5)

        tk.Label(login_gerente_admin, text="Contraseña:").pack(pady=5)
        entry_password_confirm = tk.Entry(login_gerente_admin, show="*")
        entry_password_confirm.pack(pady=5)

        def confirmar_cancelacion():
            usuario_confirm = entry_usuario_confirm.get()
            password_confirm = entry_password_confirm.get()

            if usuario_confirm and password_confirm:
                resultado = validar_login(usuario_confirm, password_confirm)
                if resultado and resultado['rol'] in ['Gerente', 'Admin']:
                    # Proceder con la cancelación
                    tree.delete(*tree.get_children())
                    label_total.config(text="0.00")
                    login_gerente_admin.destroy()
                    messagebox.showinfo("Cancelación", "Venta cancelada correctamente.")
                else:
                    messagebox.showerror("Error", "Credenciales incorrectas o permiso denegado.")
            else:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")

        tk.Button(login_gerente_admin, text="Confirmar", command=confirmar_cancelacion).pack(pady=10)

    else:
        # Si es Admin o Gerente, se permite cancelar sin confirmación
        tree.delete(*tree.get_children())
        label_total.config(text="0.00")
        messagebox.showinfo("Cancelación", "Venta cancelada correctamente.")

def crear_venta():
    global combo_cliente  # Declare this global
    ventana_venta = tk.Toplevel(ventana)
    ventana_venta.title("Registrar Venta")

    tk.Label(ventana_venta, text="Seleccione Cliente:").pack()
    combo_cliente = ttk.Combobox(ventana_venta, values=buscar_cliente_por_nombre())
    combo_cliente.pack()

    # Obtener productos y mostrarlos en el combobox
    global productos
    productos = obtener_productos()
    nombres_productos = [producto['nombre'] for producto in productos]

    tk.Label(ventana_venta, text="Seleccione Producto:").pack()
    global combo_producto
    combo_producto = ttk.Combobox(ventana_venta, values=nombres_productos)
    combo_producto.pack()

    tk.Label(ventana_venta, text="Cantidad:").pack()
    global entry_cantidad
    entry_cantidad = tk.Entry(ventana_venta)
    entry_cantidad.pack()

    # Botón para agregar el producto a la lista
    tk.Button(ventana_venta, text="Agregar Producto", command=agregar_producto_a_venta).pack()

    # Tabla para mostrar productos seleccionados
    global tree
    tree = ttk.Treeview(ventana_venta, columns=("ID", "Producto", "Cantidad", "Importe", "Subtotal"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Producto", text="Producto")
    tree.heading("Cantidad", text="Cantidad")
    tree.heading("Importe", text="Importe")
    tree.heading("Subtotal", text="Subtotal")
    tree.pack()

    # Total acumulado
    tk.Label(ventana_venta, text="Total:").pack()
    global label_total
    label_total = tk.Label(ventana_venta, text="0.00")
    label_total.pack()

    tk.Label(ventana_venta, text="Dinero del Cliente:").pack()
    global entry_dinero_cliente
    entry_dinero_cliente = tk.Entry(ventana_venta)
    entry_dinero_cliente.pack()

    # Botón para registrar la venta
    tk.Button(ventana_venta, text="Registrar Venta", command=registrar_venta).pack()

    # Botón para eliminar producto seleccionado
    tk.Button(ventana_venta, text="Eliminar Producto", command=eliminar_producto_venta).pack(pady=10)

    # Botón para modificar la cantidad de un producto seleccionado
    tk.Button(ventana_venta, text="Modificar Cantidad", command=modificar_cantidad_producto_venta).pack(pady=10)


def eliminar_producto_venta():
    seleccion = tree.focus()
    if not seleccion:
        messagebox.showerror("Error", "Seleccione un producto para eliminar")
        return

    confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este producto?")
    if confirmar:
        tree.delete(seleccion)
        # Actualizar el total después de eliminar el producto
        actualizar_total()

def modificar_cantidad_producto_venta():
    seleccion = tree.focus()
    if not seleccion:
        messagebox.showerror("Error", "Seleccione un producto para modificar la cantidad")
        return

    ventana_mod_cantidad = tk.Toplevel(ventana)
    ventana_mod_cantidad.title("Modificar Cantidad")

    tk.Label(ventana_mod_cantidad, text="Nueva Cantidad:").pack()
    entry_nueva_cantidad = tk.Entry(ventana_mod_cantidad)
    entry_nueva_cantidad.pack()

    def actualizar_cantidad():
        nueva_cantidad = entry_nueva_cantidad.get()
        if nueva_cantidad.isdigit() and int(nueva_cantidad) > 0:
            item_values = tree.item(seleccion, "values")
            producto_id, nombre, cantidad, importe, subtotal = item_values
            precio_unitario = float(importe) / int(cantidad)
            nuevo_importe = precio_unitario * int(nueva_cantidad)
            nuevo_subtotal = nuevo_importe * 1.16  # Aplicar IVA del 16%

            tree.item(seleccion, values=(producto_id, nombre, nueva_cantidad, nuevo_importe, nuevo_subtotal))
            actualizar_total()
            ventana_mod_cantidad.destroy()
        else:
            messagebox.showerror("Error", "Ingrese una cantidad válida")

    tk.Button(ventana_mod_cantidad, text="Actualizar", command=actualizar_cantidad).pack()

def actualizar_total():
    total = 0.0
    for item in tree.get_children():
        subtotal = float(tree.item(item, "values")[4])  # Tomar el subtotal
        total += subtotal

    label_total.config(text=f"{total:.2f}")



def generar_pdf():
    # Datos del cliente
    rfc = entry_rfc.get()
    nombre = entry_nombre.get()
    apellidos = entry_apellidos.get()
    calle = entry_calle.get()
    numero_exterior = entry_numero_exterior.get()
    codigo_postal = entry_codigo_postal.get()
    regimen_fiscal = combo_regimen_fiscal.get()
    uso_CFDI = combo_uso_CFDI.get()
    id_venta = combo_ventas.get()

    if not all([rfc, nombre, apellidos, calle, numero_exterior, codigo_postal, regimen_fiscal]):
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return

    if not id_venta:
        messagebox.showerror("Error", "Debe seleccionar una venta")
        return

    # Verificar si la venta está cancelada o facturada
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT estado, facturada FROM Ventas WHERE id = %s", (id_venta,))
    resultado = cursor.fetchone()
    conexion.close()

    if resultado:
        estado, facturada = resultado
        if estado == "Cancelada":
            messagebox.showerror("Error", f"La venta con ID {id_venta} está cancelada y no se puede facturar.")
            return
        if facturada == 1:
            messagebox.showerror("Error", f"La venta con ID {id_venta} ya ha sido facturada.")
            return
    else:
        messagebox.showerror("Error", f"La venta con ID {id_venta} no existe.")
        return

    # Crear PDF
    pdf = FPDF()
    pdf.add_page()

    # Encabezado
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(200, 10, 'Factura', ln=True, align='C')
    pdf.set_font('Arial', '', 10)
    
    # Datos del cliente
    pdf.cell(200, 10, f"RFC: {rfc}", ln=True)
    pdf.cell(200, 10, f"Nombre: {nombre} {apellidos}", ln=True)
    pdf.cell(200, 10, f"Domicilio: {calle} No. {numero_exterior}", ln=True)
    pdf.cell(200, 10, f"Código Postal: {codigo_postal}", ln=True)
    pdf.cell(200, 10, f"Régimen Fiscal: {regimen_fiscal}", ln=True)
    pdf.cell(200, 10, f"Uso de CFDI: {uso_CFDI}", ln=True)

    # Detalles de la venta
    pdf.cell(200, 10, "Detalles de la Venta:", ln=True)
    pdf.cell(60, 10, 'Producto', 1)
    pdf.cell(40, 10, 'Cantidad', 1)
    pdf.cell(40, 10, 'Subtotal', 1)
    pdf.ln()

    for item in tree_factura.get_children():
        producto, cantidad, subtotal = tree_factura.item(item, 'values')
        pdf.cell(60, 10, producto, 1)
        pdf.cell(40, 10, str(cantidad), 1)
        pdf.cell(40, 10, f"${subtotal}", 1)
        pdf.ln()

    # Guardar PDF en la carpeta
    pdf.output(f'/Users/alan/Desktop/facturas/factura_{id_venta}.pdf')
    
    messagebox.showinfo("Éxito", f"Factura generada correctamente")

    # Marcar la venta como facturada (asumiendo que existe la columna 'facturada')
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("UPDATE Ventas SET facturada = 1 WHERE id = %s", (id_venta,))
    conexion.commit()
    conexion.close()

# Función para cargar la factura en la interfaz
def cargar_factura():
    id_venta = combo_ventas.get()
    if id_venta:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        query = """
        SELECT p.nombre, dv.cantidad, dv.subtotal
        FROM DetalleVentas dv
        JOIN Productos p ON dv.producto_id = p.id
        WHERE dv.venta_id = %s
        """
        cursor.execute(query, (id_venta,))
        detalles = cursor.fetchall()
        conexion.close()

        # Limpiar la tabla antes de cargar nuevos detalles
        for row in tree_factura.get_children():
            tree_factura.delete(row)

        for detalle in detalles:
            tree_factura.insert("", "end", values=detalle)

# Crear la ventana para la generación de facturas
def generar_factura():
    ventana_factura = tk.Toplevel(ventana)
    ventana_factura.title("Generar Factura")

    # Formulario de datos del cliente
    tk.Label(ventana_factura, text="RFC:").pack()
    global entry_rfc
    entry_rfc = tk.Entry(ventana_factura)
    entry_rfc.pack()

    tk.Label(ventana_factura, text="Nombre:").pack()
    global entry_nombre
    entry_nombre = tk.Entry(ventana_factura)
    entry_nombre.pack()

    tk.Label(ventana_factura, text="Apellidos:").pack()
    global entry_apellidos
    entry_apellidos = tk.Entry(ventana_factura)
    entry_apellidos.pack()

    tk.Label(ventana_factura, text="Calle:").pack()
    global entry_calle
    entry_calle = tk.Entry(ventana_factura)
    entry_calle.pack()

    tk.Label(ventana_factura, text="Número Exterior:").pack()
    global entry_numero_exterior
    entry_numero_exterior = tk.Entry(ventana_factura)
    entry_numero_exterior.pack()

    tk.Label(ventana_factura, text="Código Postal:").pack()
    global entry_codigo_postal
    entry_codigo_postal = tk.Entry(ventana_factura)
    entry_codigo_postal.pack()

    tk.Label(ventana_factura, text="Régimen Fiscal:").pack()
    global combo_regimen_fiscal
    combo_regimen_fiscal = ttk.Combobox(ventana_factura, values=["General ley de personas morales", "Personas morales con fines no lucrativos", "Sueldos y asalariados", "Simplificado de confianza", "Persona física con actividad empresarial"])
    combo_regimen_fiscal.pack()

    tk.Label(ventana_factura, text="Uso de CFDI:").pack()
    global combo_uso_CFDI
    combo_uso_CFDI = ttk.Combobox(ventana_factura, values=["Gastos en general", "Adquisisión de mercancias", "Otros"])
    combo_uso_CFDI.pack()

    # Selección de venta
    tk.Label(ventana_factura, text="Seleccione Ticket (ID Venta):").pack()
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM Ventas")
    ventas = cursor.fetchall()
    conexion.close()
    global combo_ventas
    combo_ventas = ttk.Combobox(ventana_factura, values=[venta[0] for venta in ventas])
    combo_ventas.pack()

    # Botones
    tk.Button(ventana_factura, text="Cargar Factura", command=cargar_factura).pack()
    tk.Button(ventana_factura, text="Generar PDF", command=generar_pdf).pack()

    # Tabla para mostrar los productos de la venta seleccionada
    global tree_factura
    tree_factura = ttk.Treeview(ventana_factura, columns=("Producto", "Cantidad", "Subtotal"), show="headings")
    tree_factura.heading("Producto", text="Producto")
    tree_factura.heading("Cantidad", text="Cantidad")
    tree_factura.heading("Subtotal", text="Subtotal")
    tree_factura.pack()




# Obtener clientes desde la base de datos para combobox
def obtener_clientes():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM Clientes")
    clientes = cursor.fetchall()
    conexion.close()
    return clientes

# Modificación: Buscar clientes por nombre en lugar de ID
def buscar_cliente_por_nombre():
    clientes = obtener_clientes()
    return [cliente[1] for cliente in clientes]


# Crear ventana para el historial de compras (tickets)
def mostrar_historial_compras():
    ventana_historial = tk.Toplevel(ventana)
    ventana_historial.title("Historial de Compras")

    # Etiqueta y combobox para filtrar por cliente
    tk.Label(ventana_historial, text="Filtrar por Cliente:").pack()
    clientes = buscar_cliente_por_nombre()  # Obtener nombres de clientes
    combo_clientes = ttk.Combobox(ventana_historial, values=clientes)
    combo_clientes.pack()

    # Tabla para mostrar las compras (tickets)
    tree_historial = ttk.Treeview(ventana_historial, columns=("ID Venta", "Cliente", "Fecha", "Total", "Estado"), show="headings")
    tree_historial.heading("ID Venta", text="ID Venta")
    tree_historial.heading("Cliente", text="Cliente")
    tree_historial.heading("Fecha", text="Fecha")
    tree_historial.heading("Total", text="Total")
    tree_historial.heading("Estado", text="Estado")  # Nueva columna para mostrar si la venta fue cancelada
    tree_historial.pack()

    # Función para cargar compras desde la base de datos
    def cargar_compras(cliente_seleccionado=None):
        conexion = conectar_bd()
        cursor = conexion.cursor()
        if cliente_seleccionado:
            query = "SELECT v.id, c.nombre, v.fecha, v.total, v.estado FROM Ventas v JOIN Clientes c ON v.cliente_id = c.id WHERE c.nombre = %s"
            cursor.execute(query, (cliente_seleccionado,))
        else:
            query = "SELECT v.id, c.nombre, v.fecha, v.total, v.estado FROM Ventas v JOIN Clientes c ON v.cliente_id = c.id"
            cursor.execute(query)
        compras = cursor.fetchall()
        conexion.close()

        # Limpiar la tabla antes de insertar nuevos datos
        for row in tree_historial.get_children():
            tree_historial.delete(row)

        # Insertar las compras en la tabla
        for compra in compras:
            tree_historial.insert("", "end", values=compra)

    # Cargar todas las compras inicialmente
    cargar_compras()

    # Función para filtrar por cliente seleccionado
    def filtrar_por_cliente():
        cliente_seleccionado = combo_clientes.get()
        cargar_compras(cliente_seleccionado)

    tk.Button(ventana_historial, text="Filtrar", command=filtrar_por_cliente).pack()

    # Función para cancelar una venta desde el historial
    def cancelar_venta_historial():
        seleccion = tree_historial.focus()
        valores = tree_historial.item(seleccion, "values")

        if not valores:
            messagebox.showerror("Error", "Seleccione una venta para cancelar")
            return

        confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de cancelar esta venta?")
        if confirmar:
            # Verificar si es Cajero
            if usuario_actual['rol'] == 'Cajero':
                # Solicitar credenciales de Gerente o Admin
                login_gerente_admin = tk.Toplevel(ventana)
                login_gerente_admin.title("Confirmar Cancelación (Gerente/Admin)")
                login_gerente_admin.geometry("300x200")

                tk.Label(login_gerente_admin, text="Usuario:").pack(pady=5)
                entry_usuario_confirm = tk.Entry(login_gerente_admin)
                entry_usuario_confirm.pack(pady=5)

                tk.Label(login_gerente_admin, text="Contraseña:").pack(pady=5)
                entry_password_confirm = tk.Entry(login_gerente_admin, show="*")
                entry_password_confirm.pack(pady=5)

                def confirmar_cancelacion():
                    usuario_confirm = entry_usuario_confirm.get()
                    password_confirm = entry_password_confirm.get()

                    if usuario_confirm and password_confirm:
                        resultado = validar_login(usuario_confirm, password_confirm)
                        if resultado and resultado['rol'] in ['Gerente', 'Admin']:
                            # Proceder con la cancelación
                            realizar_cancelacion(valores[0])  # Pasar el ID de la venta
                            login_gerente_admin.destroy()
                        else:
                            messagebox.showerror("Error", "Credenciales incorrectas o permiso denegado.")
                    else:
                        messagebox.showerror("Error", "Todos los campos son obligatorios.")

                tk.Button(login_gerente_admin, text="Confirmar", command=confirmar_cancelacion).pack(pady=10)

            else:
                # Si es Admin o Gerente, se permite cancelar sin confirmación adicional
                realizar_cancelacion(valores[0])  # Pasar el ID de la venta

    # Botón para cancelar la venta seleccionada
    tk.Button(ventana_historial, text="Cancelar Venta", command=cancelar_venta_historial).pack(pady=10)


    def realizar_cancelacion(id_venta):
        conexion = conectar_bd()
        cursor = conexion.cursor(dictionary=True)

        # Obtener los productos de la venta para devolver al inventario
        query_detalles = "SELECT producto_id, cantidad FROM DetalleVentas WHERE venta_id = %s"
        cursor.execute(query_detalles, (id_venta,))
        productos = cursor.fetchall()

        # Devolver cada producto al inventario
        for producto in productos:
            query_actualizar_inventario = "UPDATE Inventario SET cantidad = cantidad + %s WHERE producto_id = %s"
            cursor.execute(query_actualizar_inventario, (producto['cantidad'], producto['producto_id']))

        # Marcar la venta como cancelada
        query_cancelar_venta = "UPDATE Ventas SET estado = 'Cancelada' WHERE id = %s"
        cursor.execute(query_cancelar_venta, (id_venta,))

        conexion.commit()
        conexion.close()

        messagebox.showinfo("Éxito", "Venta cancelada y productos devueltos al inventario correctamente.")
        cargar_compras()  # Recargar el historial para reflejar el cambio



# Panel de administración según el rol del usuario
def abrir_panel_rol(usuario):
    global usuario_actual
    usuario_actual = usuario
    if usuario['rol'] == "Admin":
        abrir_panel_admin()
    elif usuario['rol'] == "Gerente":
        abrir_panel_gerente()
    elif usuario['rol'] == "Cajero":
        abrir_panel_cajero()
    else:
        messagebox.showerror("Error", "Rol no reconocido")

# Panel de administración con permisos de Admin
def abrir_panel_admin():
    ventana_admin = tk.Toplevel(ventana)
    ventana_admin.title("Panel de Administración")
    ventana_admin.geometry("350x400")
    ventana_admin.resizable(False, False)
    ventana_admin.config(bg="#2c2c2c")

    frame_principal = ttk.Frame(ventana_admin, padding="10")
    frame_principal.pack(expand=True, fill=tk.BOTH)

    ttk.Label(frame_principal, text="Panel de Administración", font=("Helvetica", 16, "bold")).pack(pady=10)

    ttk.Button(frame_principal, text="Gestionar Usuarios", command=agregar_usuario).pack(pady=10, fill=tk.X)
    ttk.Button(frame_principal, text="Gestionar Inventario", command=gestionar_inventario).pack(pady=10, fill=tk.X)
    ttk.Button(frame_principal, text="Gestionar Ventas", command=crear_venta).pack(pady=10, fill=tk.X)
    ttk.Button(frame_principal, text="Gestionar Clientes", command=gestionar_clientes).pack(pady=10, fill=tk.X)
    ttk.Button(frame_principal, text="Historial de Compras", command=mostrar_historial_compras).pack(pady=10, fill=tk.X)
    ttk.Button(frame_principal, text="Generar Factura", command=generar_factura).pack(pady=10, fill=tk.X)

# Panel del gerente con acceso solo a Clientes y Ventas
def abrir_panel_gerente():
    ventana_gerente = tk.Toplevel(ventana)
    ventana_gerente.title("Panel del Gerente")
    ventana_gerente.geometry("350x300")
    ventana_gerente.resizable(False, False)
    ventana_gerente.config(bg="#2c2c2c")

    frame_principal = ttk.Frame(ventana_gerente, padding="10")
    frame_principal.pack(expand=True, fill=tk.BOTH)

    ttk.Label(frame_principal, text="Panel del Gerente", font=("Helvetica", 16, "bold")).pack(pady=10)
    
    ttk.Button(frame_principal, text="Gestionar Ventas", command=crear_venta).pack(pady=10, fill=tk.X)
    ttk.Button(frame_principal, text="Gestionar Clientes", command=gestionar_clientes).pack(pady=10, fill=tk.X)
    ttk.Button(frame_principal, text="Historial de Compras", command=mostrar_historial_compras).pack(pady=10, fill=tk.X)
    ttk.Button(frame_principal, text="Generar Factura", command=generar_factura).pack(pady=10, fill=tk.X)

# Panel del cajero con acceso a ventas
def abrir_panel_cajero():
    ventana_cajero = tk.Toplevel(ventana)
    ventana_cajero.title("Panel del Cajero")
    ventana_cajero.geometry("350x250")
    ventana_cajero.resizable(False, False)
    ventana_cajero.config(bg="#2c2c2c")

    frame_principal = ttk.Frame(ventana_cajero, padding="10")
    frame_principal.pack(expand=True, fill=tk.BOTH)

    ttk.Label(frame_principal, text="Panel del Cajero", font=("Helvetica", 16, "bold")).pack(pady=10)

    ttk.Button(frame_principal, text="Registrar Venta", command=crear_venta).pack(pady=10, fill=tk.X)
    ttk.Button(frame_principal, text="Gestionar Clientes", command=gestionar_clientes).pack(pady=10, fill=tk.X)
    ttk.Button(frame_principal, text="Historial de Compras", command=mostrar_historial_compras).pack(pady=10, fill=tk.X)

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

# Conectar con la base de datos MySQL
def conectar_bd():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="farmacia_cucei"
    )
    return conexion

# Función principal para gestionar el inventario
def gestionar_inventario():
    ventana_inv = tk.Toplevel(ventana)
    ventana_inv.title("Gestionar Inventario")
    
    # Obtener productos desde la base de datos junto con su proveedor
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT i.id, p.nombre, i.precio, i.cantidad, pr.nombre as proveedor 
        FROM Inventario i
        JOIN Productos p ON i.producto_id = p.id
        JOIN Proveedores pr ON i.proveedor_id = pr.id
    """)
    productos = cursor.fetchall()
    conexion.close()

    # Mostrar los productos en la interfaz
    tree = ttk.Treeview(ventana_inv, columns=("ID", "Nombre", "Precio", "Cantidad", "Proveedor"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Precio", text="Precio")
    tree.heading("Cantidad", text="Cantidad")
    tree.heading("Proveedor", text="Proveedor")
    tree.pack()

    for prod in productos:
        tree.insert("", tk.END, values=prod)

    # Botones para agregar, modificar y eliminar productos del inventario
    btn_agregar = tk.Button(ventana_inv, text="Agregar Producto al Inventario", command=lambda: agregar_producto_inventario(tree))
    btn_agregar.pack()
    btn_modificar = tk.Button(ventana_inv, text="Modificar Producto en Inventario", command=lambda: modificar_producto(tree))
    btn_modificar.pack()
    btn_eliminar = tk.Button(ventana_inv, text="Eliminar Producto del Inventario", command=lambda: eliminar_producto(tree))
    btn_eliminar.pack()

    # Botón para gestionar productos por proveedor
    btn_gestionar_productos_proveedor = tk.Button(ventana_inv, text="Gestionar Productos por Proveedor", command=gestionar_proveedores)
    btn_gestionar_productos_proveedor.pack()

def agregar_producto_inventario(tree):
    ventana_inv_prod = tk.Toplevel(ventana)
    ventana_inv_prod.title("Agregar Producto al Inventario")

    # Obtener proveedores desde la base de datos
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM Proveedores")
    proveedores = cursor.fetchall()
    conexion.close()

    tk.Label(ventana_inv_prod, text="Proveedor:").pack()
    combo_proveedor = ttk.Combobox(ventana_inv_prod, values=[prov[1] for prov in proveedores])
    combo_proveedor.pack()

    # Función para cargar productos del proveedor seleccionado
    def cargar_productos(event):
        proveedor_seleccionado = combo_proveedor.get()
        proveedor_id = next((prov[0] for prov in proveedores if prov[1] == proveedor_seleccionado), None)

        conexion = conectar_bd()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT p.nombre 
            FROM Productos p
            JOIN ProductosProveedores pp ON p.id = pp.producto_id
            WHERE pp.proveedor_id = %s
        """, (proveedor_id,))
        productos = cursor.fetchall()
        conexion.close()

        combo_producto['values'] = [prod[0] for prod in productos]

    combo_proveedor.bind("<<ComboboxSelected>>", cargar_productos)

    tk.Label(ventana_inv_prod, text="Producto:").pack()
    combo_producto = ttk.Combobox(ventana_inv_prod)
    combo_producto.pack()

    tk.Label(ventana_inv_prod, text="Cantidad a agregar:").pack()
    entry_cantidad = tk.Entry(ventana_inv_prod)
    entry_cantidad.pack()

    def guardar_inventario():
        proveedor_seleccionado = combo_proveedor.get()
        producto_seleccionado = combo_producto.get()
        cantidad = entry_cantidad.get()

        if proveedor_seleccionado and producto_seleccionado and cantidad:
            proveedor_id = next((prov[0] for prov in proveedores if prov[1] == proveedor_seleccionado), None)
            
            # Obtener el ID del producto seleccionado
            conexion = conectar_bd()
            cursor = conexion.cursor()

            cursor.execute("SELECT id FROM Productos WHERE nombre=%s", (producto_seleccionado,))
            producto_id = cursor.fetchone()[0]

            # Verificar si el producto ya está en el inventario
            query_check = "SELECT cantidad FROM Inventario WHERE producto_id = %s AND proveedor_id = %s"
            cursor.execute(query_check, (producto_id, proveedor_id))
            producto_existente = cursor.fetchone()

            if producto_existente:
                # Si el producto ya existe, se actualiza la cantidad
                nueva_cantidad = producto_existente[0] + int(cantidad)
                query_update = "UPDATE Inventario SET cantidad = %s WHERE producto_id = %s AND proveedor_id = %s"
                cursor.execute(query_update, (nueva_cantidad, producto_id, proveedor_id))
                messagebox.showinfo("Éxito", "Cantidad actualizada correctamente")
            else:
                # Si el producto no existe en el inventario, lo agrega
                query_insert = "INSERT INTO Inventario (proveedor_id, producto_id, cantidad) VALUES (%s, %s, %s)"
                cursor.execute(query_insert, (proveedor_id, producto_id, cantidad))
                messagebox.showinfo("Éxito", "Producto agregado al inventario correctamente")

            conexion.commit()
            conexion.close()
            ventana_inv_prod.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    tk.Button(ventana_inv_prod, text="Guardar", command=guardar_inventario).pack()
    
    def guardar_inventario():
        proveedor_seleccionado = combo_proveedor.get()
        producto_seleccionado = combo_producto.get()
        cantidad = entry_cantidad.get()
        precio = entry_precio.get() # type: ignore

        if proveedor_seleccionado and producto_seleccionado and cantidad and precio:
            proveedor_id = next((prov[0] for prov in proveedores if prov[1] == proveedor_seleccionado), None)
            
            # Obtener el ID del producto seleccionado
            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Verificar si el producto ya está en el inventario
            query_check = "SELECT * FROM Inventario WHERE producto_id = (SELECT id FROM Productos WHERE nombre = %s)"
            cursor.execute(query_check, (producto_seleccionado,))
            producto_existente = cursor.fetchone()

            if producto_existente:
                messagebox.showerror("Error", "Este producto ya está en el inventario.")
            else:
                cursor.execute("SELECT id FROM Productos WHERE nombre=%s", (producto_seleccionado,))
                producto_id = cursor.fetchone()[0]

                # Insertar en el inventario
                query_inventario = "INSERT INTO Inventario (proveedor_id, producto_id, cantidad, precio) VALUES (%s, %s, %s, %s)"
                cursor.execute(query_inventario, (proveedor_id, producto_id, cantidad, precio))

                conexion.commit()
                messagebox.showinfo("Éxito", "Producto agregado al inventario correctamente")

            conexion.close()
            ventana_inv_prod.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    tk.Button(ventana_inv_prod, text="Guardar", command=guardar_inventario).pack()

# Función para modificar un producto en el inventario
def modificar_producto(tree):
    seleccion = tree.focus()
    valores = tree.item(seleccion, "values")

    if not valores:
        messagebox.showerror("Error", "Seleccione un producto para modificar")
        return

    ventana_mod = tk.Toplevel(ventana)
    ventana_mod.title("Modificar Producto en Inventario")

    tk.Label(ventana_mod, text="Nombre:").pack()
    entry_nombre = tk.Entry(ventana_mod)
    entry_nombre.insert(0, valores[1])
    entry_nombre.pack()

    tk.Label(ventana_mod, text="Precio:").pack()
    entry_precio = tk.Entry(ventana_mod)
    entry_precio.insert(0, valores[2])
    entry_precio.pack()

    tk.Label(ventana_mod, text="Cantidad:").pack()
    entry_cantidad = tk.Entry(ventana_mod)
    entry_cantidad.insert(0, valores[3])
    entry_cantidad.pack()

    def actualizar_producto():
        nombre = entry_nombre.get()
        precio = entry_precio.get()
        cantidad = entry_cantidad.get()

        if nombre and precio and cantidad:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            query = "UPDATE Inventario SET precio=%s, cantidad=%s WHERE id=%s"
            cursor.execute(query, (precio, cantidad, valores[0]))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Producto modificado correctamente")
            ventana_mod.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    tk.Button(ventana_mod, text="Actualizar", command=actualizar_producto).pack()

# Función para eliminar un producto del inventario
def eliminar_producto(tree):
    seleccion = tree.focus()
    valores = tree.item(seleccion, "values")

    if not valores:
        messagebox.showerror("Error", "Seleccione un producto para eliminar")
        return

    confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este producto?")
    if confirmar:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        query = "DELETE FROM Inventario WHERE id=%s"
        cursor.execute(query, (valores[0],))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Producto eliminado correctamente")

# Función para gestionar proveedores y productos por proveedor
def gestionar_proveedores():
    ventana_proveedores = tk.Toplevel(ventana)
    ventana_proveedores.title("Gestionar Proveedores y Productos")

    # Obtener proveedores desde la base de datos
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Proveedores")
    proveedores = cursor.fetchall()
    conexion.close()

    # Mostrar los proveedores en la interfaz
    tree_prov = ttk.Treeview(ventana_proveedores, columns=("ID", "Nombre", "Contacto"), show="headings")
    tree_prov.heading("ID", text="ID")
    tree_prov.heading("Nombre", text="Nombre")
    tree_prov.heading("Contacto", text="Contacto")
    tree_prov.pack()

    for prov in proveedores:
        tree_prov.insert("", tk.END, values=prov)

    # Botones para agregar, modificar y eliminar proveedores
    btn_agregar_proveedor = tk.Button(ventana_proveedores, text="Agregar Proveedor", command=agregar_proveedor)
    btn_agregar_proveedor.pack()

    # Botón para agregar productos a un proveedor
    btn_agregar_producto_proveedor = tk.Button(ventana_proveedores, text="Agregar Producto a Proveedor", command=agregar_producto_proveedor)
    btn_agregar_producto_proveedor.pack()

# Función para agregar un nuevo proveedor
def agregar_proveedor():
    ventana_proveedor = tk.Toplevel(ventana)
    ventana_proveedor.title("Agregar Proveedor")

    tk.Label(ventana_proveedor, text="Nombre del Proveedor:").pack()
    entry_nombre_proveedor = tk.Entry(ventana_proveedor)
    entry_nombre_proveedor.pack()

    tk.Label(ventana_proveedor, text="Contacto:").pack()
    entry_contacto = tk.Entry(ventana_proveedor)
    entry_contacto.pack()

    def guardar_proveedor():
        nombre = entry_nombre_proveedor.get()
        contacto = entry_contacto.get()

        if nombre and contacto:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            query = "INSERT INTO Proveedores (nombre, contacto) VALUES (%s, %s)"
            cursor.execute(query, (nombre, contacto))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Proveedor agregado correctamente")
            ventana_proveedor.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    tk.Button(ventana_proveedor, text="Guardar Proveedor", command=guardar_proveedor).pack()

# Función para agregar un nuevo producto a un proveedor
def agregar_producto_proveedor():
    ventana_prod_proveedor = tk.Toplevel(ventana)
    ventana_prod_proveedor.title("Agregar Producto a Proveedor")

    # Obtener proveedores desde la base de datos
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM Proveedores")
    proveedores = cursor.fetchall()
    conexion.close()

    nombres_proveedores = [prov[1] for prov in proveedores]

    tk.Label(ventana_prod_proveedor, text="Proveedor:").pack()
    combo_proveedor = ttk.Combobox(ventana_prod_proveedor, values=nombres_proveedores)
    combo_proveedor.pack()

    tk.Label(ventana_prod_proveedor, text="Producto:").pack()
    entry_producto = tk.Entry(ventana_prod_proveedor)
    entry_producto.pack()

    def guardar_producto_proveedor():
        producto_nombre = entry_producto.get()
        proveedor_seleccionado = combo_proveedor.get()

        if producto_nombre and proveedor_seleccionado:
            proveedor_id = next((prov[0] for prov in proveedores if prov[1] == proveedor_seleccionado), None)

            conexion = conectar_bd()
            cursor = conexion.cursor()

            # Check if the product already exists for the supplier
            query_check = "SELECT * FROM ProductosProveedores WHERE proveedor_id = %s AND producto_id = (SELECT id FROM Productos WHERE nombre = %s)"
            cursor.execute(query_check, (proveedor_id, producto_nombre))
            producto_existente = cursor.fetchone()

            if producto_existente:
                messagebox.showerror("Error", "Este producto ya está registrado para este proveedor.")
            else:
                # Insertar el producto si no existe
                query_producto = "INSERT INTO Productos (nombre) VALUES (%s)"
                cursor.execute(query_producto, (producto_nombre,))
                producto_id = cursor.lastrowid

                # Vincular producto con proveedor
                query_vincular = "INSERT INTO ProductosProveedores (proveedor_id, producto_id) VALUES (%s, %s)"
                cursor.execute(query_vincular, (proveedor_id, producto_id))

                conexion.commit()
                messagebox.showinfo("Éxito", "Producto agregado al proveedor correctamente")
            conexion.close()
            ventana_prod_proveedor.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    tk.Button(ventana_prod_proveedor, text="Guardar", command=guardar_producto_proveedor).pack()

# Función para gestionar clientes
def gestionar_clientes():
    ventana_clientes = tk.Toplevel(ventana)
    ventana_clientes.title("Gestionar Clientes")

    # Tabla para mostrar clientes existentes
    tree = ttk.Treeview(ventana_clientes, columns=("ID", "Nombre", "Puntos"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Puntos", text="Puntos")
    tree.pack()

    # Cargar los clientes desde la base de datos y mostrarlos en la tabla
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Clientes")
    clientes = cursor.fetchall()
    conexion.close()

    for cliente in clientes:
        tree.insert("", tk.END, values=cliente)

    btn_agregar_cliente = tk.Button(ventana_clientes, text="Agregar Cliente", command=agregar_cliente)
    btn_agregar_cliente.pack()

# Agregar un nuevo cliente
def agregar_cliente():
    ventana_nuevo_cliente = tk.Toplevel(ventana)
    ventana_nuevo_cliente.title("Registrar Cliente")

    tk.Label(ventana_nuevo_cliente, text="ID Cliente:").pack()
    entry_id_cliente = tk.Entry(ventana_nuevo_cliente)
    entry_id_cliente.pack()

    tk.Label(ventana_nuevo_cliente, text="Nombre del Cliente:").pack()
    entry_nombre_cliente = tk.Entry(ventana_nuevo_cliente)
    entry_nombre_cliente.pack()

    def guardar_cliente():
        cliente_id = entry_id_cliente.get()
        nombre_cliente = entry_nombre_cliente.get()
        
        if cliente_id and nombre_cliente:
            conexion = conectar_bd()
            cursor = conexion.cursor()
            query = "INSERT INTO Clientes (id, nombre, puntos) VALUES (%s, %s, %s)"
            cursor.execute(query, (cliente_id, nombre_cliente, 0))  # Registrar cliente con 0 puntos
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Cliente registrado correctamente")
            ventana_nuevo_cliente.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    tk.Button(ventana_nuevo_cliente, text="Guardar Cliente", command=guardar_cliente).pack()

# Crear la ventana principal de login
def login():
    usuario = entry_usuario.get()
    password = entry_password.get()

    if usuario and password:
        resultado = validar_login(usuario, password)
        if resultado:
            abrir_panel_rol(resultado)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios")

# Ventana de Login
ventana = tk.Tk()
ventana.title("Sistema de Farmacia CUCEI")
ventana.geometry("300x220")
ventana.config(bg="#2c2c2c")

# Login Form
ttk.Label(ventana, text="Iniciar Sesión", font=("Helvetica", 16, "bold")).pack(pady=10)
frame_login = ttk.Frame(ventana, padding="10")
frame_login.pack(expand=True, fill=tk.BOTH)

ttk.Label(frame_login, text="Usuario:").pack(pady=5)
entry_usuario = ttk.Entry(frame_login)
entry_usuario.pack()

ttk.Label(frame_login, text="Contraseña:").pack(pady=5)
entry_password = ttk.Entry(frame_login, show="*")
entry_password.pack()

ttk.Button(ventana, text="Iniciar Sesión", command=login).pack(pady=10)

ventana.mainloop()
