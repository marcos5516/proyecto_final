# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 14:04:33 2024

@author: Juan Vazquez
"""

import tkinter as tk
from tkinter import END,messagebox,ttk

class Interfaz_Usuario:
    def interfaz(self):
        root=tk.Tk()
        root.config(width=500,height=400)
        root.title("USUARIOS")
        
        tk.Label(root,text="Codigo a buscar:").place(x=35,y=5)
        self.txIdBus=tk.Entry(root)
        self.txIdBus.place(x=150,y=5)
        
        tk.Label(root,text="ID:").place(x=10,y=30)
        self.txId=tk.Entry(root)
        self.txId.place(x=10,y=50)
        
        tk.Label(root,text="Nombre:").place(x=10,y=70)
        self.txnombre=tk.Entry(root, width=30)
        self.txnombre.place(x=10,y=90)
        
        tk.Label(root,text="A Paterno:").place(x=10,y=110)
        self.txAPaterno=tk.Entry(root, width=30)
        self.txAPaterno.place(x=10,y=130)
        
        tk.Label(root,text="A Materno:").place(x=10,y=150)
        self.txAMaterno=tk.Entry(root, width=30)
        self.txAMaterno.place(x=10,y=170)
        
        tk.Label(root,text="email:").place(x=10,y=190)
        self.txemail=tk.Entry(root, width=30)
        self.txemail.place(x=10,y=210)
        
        tk.Label(root,text="Username:").place(x=230,y=70)
        self.txusername=tk.Entry(root, width=30)
        self.txusername.place(x=230,y=90)
        
        tk.Label(root,text="password:").place(x=230,y=110)
        self.txpasword=tk.Entry(root, width=30)
        self.txpasword.place(x=230,y=130)
        
        tk.Label(root,text="Perfil:").place(x=230,y=150)
        self.cbperfil=ttk.Combobox(root,state="normal",
                                     values=["admin","Maestro","Alumno"])
        self.cbperfil.place(x=230,y=175)
        
        self.btnNuevo=tk.Button(root,text="Nuevo",command=lambda:self.Nuevo())
        self.btnNuevo.place(x=20,y=280)
        
        self.btnSalvar=tk.Button(root,text="Salvar",command=lambda:self.Salvar())
        self.btnSalvar.place(x=70,y=280)
        
        self.btnCancelar=tk.Button(root,text="Cancelar",command=lambda:self.Cancelar())
        self.btnCancelar.place(x=115,y=280)
        
        self.btnBaja=tk.Button(root,text="Baja",command=lambda:self.Baja())
        self.btnBaja.place(x=180,y=280)
        
        self.btnEditar=tk.Button(root,text="Editar",command=lambda:self.Editar())
        self.btnEditar.place(x=220,y=280)
        
        self.btnBuscar=tk.Button(root,text="Buscar",command=lambda:self.Buscar())
        self.btnBuscar.place(x=285,y=5)
        
        root.mainloop()
        
class interfaz_Alumnos:
    def interfaz(self):
        root=tk.Tk()
        root.config(width=500,height=400)
        root.title("ALUMNOS")
        
        tk.Label(root,text="Codigo a buscar:").place(x=35,y=5)
        self.txIdBus=tk.Entry(root)
        self.txIdBus.place(x=150,y=5)
        
        tk.Label(root,text="ID:").place(x=10,y=30)
        self.txId=tk.Entry(root)
        self.txId.place(x=10,y=50)
        
        tk.Label(root,text="Nombre:").place(x=10,y=70)
        self.txnombre=tk.Entry(root, width=30)
        self.txnombre.place(x=10,y=90)
        
        tk.Label(root,text="A Paterno:").place(x=10,y=110)
        self.txAPaterno=tk.Entry(root, width=30)
        self.txAPaterno.place(x=10,y=130)
        
        tk.Label(root,text="A Materno:").place(x=10,y=150)
        self.txAMaterno=tk.Entry(root, width=30)
        self.txAMaterno.place(x=10,y=170)
        
        tk.Label(root,text="email:").place(x=10,y=190)
        self.txemail=tk.Entry(root, width=30)
        self.txemail.place(x=10,y=210)
        
        tk.Label(root,text="Estado:").place(x=230,y=30)
        self.cbestado=ttk.Combobox(root,state="normal",
                                     values=[""])
        self.cbestado.place(x=230,y=50)
        
        tk.Label(root,text="Fecha Na:").place(x=230,y=75)
        self.txfecha=tk.Entry(root, width=30)
        self.txfecha.place(x=230,y=95)
        
        tk.Label(root,text="Carrera:").place(x=230,y=115)
        self.cbcarrera=ttk.Combobox(root,state="normal",
                                     values=[""])
        self.cbcarrera.place(x=230,y=135)
        
        tk.Label(root,text="Materias:").place(x=230,y=160)
        self.cbmaterias=ttk.Combobox(root,state="normal",
                                     values=[""])
        self.cbmaterias.place(x=230,y=180)
        
        self.btnNuevo=tk.Button(root,text="Nuevo",command=lambda:self.Nuevo())
        self.btnNuevo.place(x=20,y=280)
        
        self.btnSalvar=tk.Button(root,text="Salvar",command=lambda:self.Salvar())
        self.btnSalvar.place(x=70,y=280)
        
        self.btnCancelar=tk.Button(root,text="Cancelar",command=lambda:self.Cancelar())
        self.btnCancelar.place(x=115,y=280)
        
        self.btnBaja=tk.Button(root,text="Baja",command=lambda:self.Baja())
        self.btnBaja.place(x=180,y=280)
        
        self.btnEditar=tk.Button(root,text="Editar",command=lambda:self.Editar())
        self.btnEditar.place(x=220,y=280)
        
        self.btnBuscar=tk.Button(root,text="Buscar",command=lambda:self.Buscar())
        self.btnBuscar.place(x=285,y=5)
        
        root.mainloop()
        
        
class Interfaz_Maestros:
    def interfaz(self):
        root=tk.Tk()
        root.config(width=500,height=400)
        root.title("MAESTROS")
        
        tk.Label(root,text="Codigo a buscar:").place(x=35,y=5)
        self.txIdBus=tk.Entry(root)
        self.txIdBus.place(x=150,y=5)
        
        tk.Label(root,text="ID:").place(x=10,y=30)
        self.txId=tk.Entry(root)
        self.txId.place(x=10,y=50)
        
        tk.Label(root,text="Nombre:").place(x=10,y=70)
        self.txnombre=tk.Entry(root, width=30)
        self.txnombre.place(x=10,y=90)
        
        tk.Label(root,text="A Paterno:").place(x=10,y=110)
        self.txAPaterno=tk.Entry(root, width=30)
        self.txAPaterno.place(x=10,y=130)
        
        tk.Label(root,text="A Materno:").place(x=10,y=150)
        self.txAMaterno=tk.Entry(root, width=30)
        self.txAMaterno.place(x=10,y=170)
        
        tk.Label(root,text="email:").place(x=10,y=190)
        self.txemail=tk.Entry(root, width=30)
        self.txemail.place(x=10,y=210)
        
        tk.Label(root,text="Carrera:").place(x=230,y=70)
        self.cbcarrera=ttk.Combobox(root,state="normal",
                                     values=[""])
        self.cbcarrera.place(x=230,y=90)
        
        tk.Label(root,text="Materias:").place(x=230,y=115)
        self.cbmaterias=ttk.Combobox(root,state="normal",
                                     values=[""])
        self.cbmaterias.place(x=230,y=135)
        
        tk.Label(root,text="Grado de estudios:").place(x=230,y=190)
        self.txemail=tk.Entry(root, width=30)
        self.txemail.place(x=230,y=210)
        
        self.btnNuevo=tk.Button(root,text="Nuevo",command=lambda:self.Nuevo())
        self.btnNuevo.place(x=20,y=280)
        
        self.btnSalvar=tk.Button(root,text="Salvar",command=lambda:self.Salvar())
        self.btnSalvar.place(x=70,y=280)
        
        self.btnCancelar=tk.Button(root,text="Cancelar",command=lambda:self.Cancelar())
        self.btnCancelar.place(x=115,y=280)
        
        self.btnBaja=tk.Button(root,text="Baja",command=lambda:self.Baja())
        self.btnBaja.place(x=180,y=280)
        
        self.btnEditar=tk.Button(root,text="Editar",command=lambda:self.Editar())
        self.btnEditar.place(x=220,y=280)
        
        self.btnBuscar=tk.Button(root,text="Buscar",command=lambda:self.Buscar())
        self.btnBuscar.place(x=285,y=5)
        
        root.mainloop()
        
class Interfaz_Materias:
    def interfaz(self):
        root=tk.Tk()
        root.config(width=500,height=400)
        root.title("MATERIAS")
        
        tk.Label(root,text="Codigo a buscar:").place(x=35,y=5)
        self.txIdBus=tk.Entry(root)
        self.txIdBus.place(x=150,y=5)
        
        tk.Label(root,text="ID:").place(x=10,y=30)
        self.txId=tk.Entry(root)
        self.txId.place(x=10,y=50)
        
        tk.Label(root,text="Asignatura:").place(x=10,y=70)
        self.txasignatura=tk.Entry(root, width=30)
        self.txasignatura.place(x=10,y=90)
        
        tk.Label(root,text="Creditos:").place(x=10,y=110)
        self.txcreditos=tk.Entry(root, width=30)
        self.txcreditos.place(x=10,y=130)
        
        tk.Label(root,text="Semestre:").place(x=10,y=150)
        self.txsemestre=tk.Entry(root, width=30)
        self.txsemestre.place(x=10,y=170)
        
        tk.Label(root,text="Carrera:").place(x=230,y=70)
        self.cbcarrera=ttk.Combobox(root,state="normal",
                                     values=[""])
        self.cbcarrera.place(x=230,y=90)
        
        self.btnNuevo=tk.Button(root,text="Nuevo",command=lambda:self.Nuevo())
        self.btnNuevo.place(x=20,y=280)
        
        self.btnSalvar=tk.Button(root,text="Salvar",command=lambda:self.Salvar())
        self.btnSalvar.place(x=70,y=280)
        
        self.btnCancelar=tk.Button(root,text="Cancelar",command=lambda:self.Cancelar())
        self.btnCancelar.place(x=115,y=280)
        
        self.btnBaja=tk.Button(root,text="Baja",command=lambda:self.Baja())
        self.btnBaja.place(x=180,y=280)
        
        self.btnEditar=tk.Button(root,text="Editar",command=lambda:self.Editar())
        self.btnEditar.place(x=220,y=280)
        
        self.btnBuscar=tk.Button(root,text="Buscar",command=lambda:self.Buscar())
        self.btnBuscar.place(x=285,y=5)
        
        root.mainloop()
        
class Interfaz_Grupos:
    def interfaz(self):
        root=tk.Tk()
        root.config(width=500,height=400)
        root.title("GRUPOS")
        
        tk.Label(root,text="Codigo a buscar:").place(x=35,y=5)
        self.txIdBus=tk.Entry(root)
        self.txIdBus.place(x=150,y=5)
        
        tk.Label(root,text="ID:").place(x=10,y=30)
        self.txId=tk.Entry(root)
        self.txId.place(x=10,y=50)
        
        tk.Label(root,text="Nombre grupo:").place(x=10,y=70)
        self.txnombre=tk.Entry(root, width=30)
        self.txnombre.place(x=10,y=90)
        
        tk.Label(root,text="Fecha:").place(x=10,y=110)
        self.txfecha=tk.Entry(root, width=30)
        self.txfecha.place(x=10,y=130)
        
        tk.Label(root,text="Carrera:").place(x=10,y=150)
        self.cbcarrera=ttk.Combobox(root,state="normal",
                                     values=[""])
        self.cbcarrera.place(x=10,y=170)
        
        tk.Label(root,text="Materia:").place(x=10,y=195)
        self.cbmateria=ttk.Combobox(root,state="normal",
                                     values=[""])
        self.cbmateria.place(x=10,y=215)
        
        tk.Label(root,text="Maestro:").place(x=10,y=240)
        self.cbmaestro=ttk.Combobox(root,state="normal",
                                     values=[""])
        self.cbmaestro.place(x=10,y=265)
        
        tk.Label(root,text="Salon:").place(x=230,y=70)
        self.cbsalon=ttk.Combobox(root,state="normal",
                                     values=[""])
        self.cbsalon.place(x=230,y=90)
        
        tk.Label(root,text="Horario:").place(x=230,y=115)
        self.cbhorario=ttk.Combobox(root,state="normal",
                                     values=[""])
        self.cbhorario.place(x=230,y=135)
        
        tk.Label(root,text="Semestre:").place(x=230,y=160)
        self.txsemestre=tk.Entry(root, width=30)
        self.txsemestre.place(x=230,y=180)
        
        tk.Label(root,text="Max Alumnos:").place(x=230,y=200)
        self.cbmaxalumnos=ttk.Combobox(root,state="normal",
                                     values=[""])
        self.cbmaxalumnos.place(x=230,y=225)
        
        self.btnNuevo=tk.Button(root,text="Nuevo",command=lambda:self.Nuevo())
        self.btnNuevo.place(x=20,y=300)
        
        self.btnSalvar=tk.Button(root,text="Salvar",command=lambda:self.Salvar())
        self.btnSalvar.place(x=70,y=300)
        
        self.btnCancelar=tk.Button(root,text="Cancelar",command=lambda:self.Cancelar())
        self.btnCancelar.place(x=115,y=300)
        
        self.btnBaja=tk.Button(root,text="Baja",command=lambda:self.Baja())
        self.btnBaja.place(x=180,y=300)
        
        self.btnEditar=tk.Button(root,text="Editar",command=lambda:self.Editar())
        self.btnEditar.place(x=220,y=300)
        
        self.btnBuscar=tk.Button(root,text="Buscar",command=lambda:self.Buscar())
        self.btnBuscar.place(x=285,y=5)
        
        root.mainloop()
        
class Interfaz_Horarios:
    def interfaz(self):
        root=tk.Tk()
        root.config(width=500,height=400)
        root.title("HORARIOS")
        
        tk.Label(root,text="Codigo a buscar:").place(x=35,y=5)
        self.txIdBus=tk.Entry(root)
        self.txIdBus.place(x=150,y=5)
        
        tk.Label(root,text="ID:").place(x=10,y=30)
        self.txId=tk.Entry(root)
        self.txId.place(x=10,y=50)
        
        tk.Label(root,text="Turno:").place(x=10,y=70)
        self.cbturno=ttk.Combobox(root,state="normal",
                                     values=[""])
        self.cbturno.place(x=10,y=90)
        
        tk.Label(root,text="Hora:").place(x=10,y=115)
        self.txhora=tk.Entry(root, width=30)
        self.txhora.place(x=10,y=135)
        
        self.btnNuevo=tk.Button(root,text="Nuevo",command=lambda:self.Nuevo())
        self.btnNuevo.place(x=20,y=280)
        
        self.btnSalvar=tk.Button(root,text="Salvar",command=lambda:self.Salvar())
        self.btnSalvar.place(x=70,y=280)
        
        self.btnCancelar=tk.Button(root,text="Cancelar",command=lambda:self.Cancelar())
        self.btnCancelar.place(x=115,y=280)
        
        self.btnBaja=tk.Button(root,text="Baja",command=lambda:self.Baja())
        self.btnBaja.place(x=180,y=280)
        
        self.btnEditar=tk.Button(root,text="Editar",command=lambda:self.Editar())
        self.btnEditar.place(x=220,y=280)
        
        self.btnBuscar=tk.Button(root,text="Buscar",command=lambda:self.Buscar())
        self.btnBuscar.place(x=285,y=5)
        
        root.mainloop()
        
class Interfaz_Salon:
    def interfaz(self):
        root=tk.Tk()
        root.config(width=500,height=400)
        root.title("SALON")
        
        tk.Label(root,text="Codigo a buscar:").place(x=35,y=5)
        self.txIdBus=tk.Entry(root)
        self.txIdBus.place(x=150,y=5)
        
        tk.Label(root,text="ID:").place(x=10,y=30)
        self.txId=tk.Entry(root)
        self.txId.place(x=10,y=50)
        
        tk.Label(root,text="Nombre salon:").place(x=10,y=70)
        self.txnombre=tk.Entry(root, width=30)
        self.txnombre.place(x=10,y=90)
        
        tk.Label(root,text="Edificio:").place(x=10,y=110)
        self.cbedificio=ttk.Combobox(root,state="normal",
                                     values=[""])
        self.cbedificio.place(x=10,y=130)
        
        self.btnNuevo=tk.Button(root,text="Nuevo",command=lambda:self.Nuevo())
        self.btnNuevo.place(x=20,y=280)
        
        self.btnSalvar=tk.Button(root,text="Salvar",command=lambda:self.Salvar())
        self.btnSalvar.place(x=70,y=280)
        
        self.btnCancelar=tk.Button(root,text="Cancelar",command=lambda:self.Cancelar())
        self.btnCancelar.place(x=115,y=280)
        
        self.btnBaja=tk.Button(root,text="Baja",command=lambda:self.Baja())
        self.btnBaja.place(x=180,y=280)
        
        self.btnEditar=tk.Button(root,text="Editar",command=lambda:self.Editar())
        self.btnEditar.place(x=220,y=280)
        
        self.btnBuscar=tk.Button(root,text="Buscar",command=lambda:self.Buscar())
        self.btnBuscar.place(x=285,y=5)
        
        root.mainloop()
        
class Interfaz_Carrera:
    
    def Iniciar(self):
        self.txId.config(state=tk.DISABLED)
        self.txnombre.config(state=tk.DISABLED)
        self.cbedificio.config(state=tk.DISABLED)
        
        self.btnNuevo.config(state=tk.NORMAL)
        self.btnSalvar.config(state=tk.DISABLED)
        self.btnCancelar.config(state=tk.DISABLED)
        self.btnBaja.config(state=tk.DISABLED)
        self.btnEditar.config(state=tk.DISABLED)
        
    
    def Nuevo(self):
        self.txId.config(state=tk.NORMAL)
        self.txnombre.config(state=tk.NORMAL)
        self.cbedificio.config(state=tk.NORMAL)
        
        self.btnSalvar.config(state=tk.NORMAL)
        self.btnCancelar.config(state=tk.NORMAL)
    
    def interfaz(self):
        root=tk.Tk()
        root.config(width=500,height=400)
        root.title("CARRERA")
        
        tk.Label(root,text="Codigo a buscar:").place(x=35,y=5)
        self.txIdBus=tk.Entry(root)
        self.txIdBus.place(x=150,y=5)
        
        tk.Label(root,text="ID:").place(x=10,y=30)
        self.txId=tk.Entry(root)
        self.txId.place(x=10,y=50)
        
        tk.Label(root,text="Nombre salon:").place(x=10,y=70)
        self.txnombre=tk.Entry(root, width=30)
        self.txnombre.place(x=10,y=90)
        
        tk.Label(root,text="Edificio:").place(x=10,y=110)
        self.cbedificio=ttk.Combobox(root,state="normal",
                                     values=[""])
        self.cbedificio.place(x=10,y=130)
        
        self.btnNuevo=tk.Button(root,text="Nuevo",command=lambda:self.Nuevo())
        self.btnNuevo.place(x=20,y=280)
        
        self.btnSalvar=tk.Button(root,text="Salvar",command=lambda:self.Salvar())
        self.btnSalvar.place(x=70,y=280)
        
        self.btnCancelar=tk.Button(root,text="Cancelar",command=lambda:self.Cancelar())
        self.btnCancelar.place(x=115,y=280)
        
        self.btnBaja=tk.Button(root,text="Baja",command=lambda:self.Baja())
        self.btnBaja.place(x=180,y=280)
        
        self.btnEditar=tk.Button(root,text="Editar",command=lambda:self.Editar())
        self.btnEditar.place(x=220,y=280)
        
        self.btnBuscar=tk.Button(root,text="Buscar",command=lambda:self.Buscar())
        self.btnBuscar.place(x=285,y=5)
        
        self.Iniciar()
        root.mainloop()
        
inter=Interfaz_Usuario()
inter.interfaz()

inter=interfaz_Alumnos()
inter.interfaz()

inter=Interfaz_Maestros()
inter.interfaz()

inter=Interfaz_Materias()
inter.interfaz()

inter=Interfaz_Grupos()
inter.interfaz()

inter=Interfaz_Salon()
inter.interfaz()

inter=Interfaz_Carrera()
inter.interfaz()
