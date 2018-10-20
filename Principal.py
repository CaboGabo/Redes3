from Agente import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from rrdtool1 import *
from rrdtool2 import *
from Graficar import *
import time
#from PIL import Image, ImageTk

def printinfo(indice, columna,pes3):
    while (1):
        lineas = []
        fila = 0
        archivo = open("informacion" + str(indice) + ".txt", "r")
        for linea in archivo:
            lineas.append(linea)
        if (len(lineas) > 0):
            Label(pes3, text="Hostname: " + lineas[0]).grid(row=fila, column=columna)
            fila += 1
            Label(pes3, text="Version: " + lineas[1]).grid(row=fila, column=columna)
            fila += 1
            Label(pes3, text="Comunidad: " + lineas[2]).grid(row=fila, column=columna)
            fila += 1
            Label(pes3, text="Dirección IP: " + lineas[3]).grid(row=fila, column=columna)
            fila += 1
            Label(pes3, text="Nombre: " + lineas[4]).grid(row=fila, column=columna)
            fila += 1
            sistemaop = lineas[5]
            Label(pes3, text="Sistema operativo: " + sistemaop).grid(row=fila, column=columna)
            fila += 1
            Label(pes3, text="Número de interfaces de red: " + lineas[6]).grid(row=fila, column=columna)
            fila += 1
            Label(pes3, text="Tiempo desde el último reinicio: " + lineas[7]).grid(row=fila, column=columna)
            fila += 1
            Label(pes3, text="Ubicacion: " + lineas[8]).grid(row=fila, column=columna)
            fila += 1
            Label(pes3, text="Correo de contacto: " + lineas[9]).grid(row=fila, column=columna)
            fila += 1
            Label(pes3, text="Porcentaje de CPU: " + lineas[10]).grid(row=fila, column=columna)
            fila += 1
            Label(pes3, text="Memoria RAM usada: " + lineas[11]).grid(row=fila, column=columna)
            fila += 1
            if (sistemaop == "Windows\n"):
                img1 = PhotoImage(file="windows.png")
                a = Label(pes3, image=img1)
                a.image = img1
                a.grid(row=fila, column=columna)
            elif (sistemaop == "Linux\n"):
                img2 = PhotoImage(file="linux.png")
                a = Label(pes3, image=img2)
                a.image = img2
                a.grid(row=fila, column=columna)
            else:
                img3 = PhotoImage(file="desconocido.png")
                a = Label(pes3, image=img3)
                a.image = img3
                a.grid(row=fila, column=columna)
            archivo.close()
        time.sleep(1)

class Principal():

    def __init__(self, usr):
        self.window = Tk()
        self.window.title("Observatorium-Pantitlan")
        self.Hostname = StringVar()
        self.Version = IntVar()
        self.Puerto = IntVar()
        self.Comunidad = StringVar()
        self.Usuario = StringVar()
        self.usuario = usr
        self.inicio()

    def inicio(self):
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill='both', expand='yes')
        self.pestInicio()
        self.pestInsertarAgente()
        self.pestEliminarAgente()
        self.pestEstadoDispositivo()
        #self.pestGraficas()

        self.window.geometry("400x350")
        self.window.mainloop()

    def insertar(self):
        agente = Agente()
        agente.insertar(self.Hostname.get(), self.Version.get(), self.Puerto.get(), self.Comunidad.get(), self.usuario)
        self.Hostname.set("")
        self.Version.set("")
        self.Puerto.set("")
        self.Comunidad.set("")
        messagebox.showinfo("Registro exitoso", "Agente registrado correctamente")
        self.mostrarDispositivos()

    def eliminar(self):
        agente = Agente()
        agente.eliminar(self.Comunidad.get(), self.usuario)
        self.Comunidad.set("")
        messagebox.showinfo("Eliminado exitoso", "Agente eliminado correctamente")

    def mostrarDispositivos(self):
        agente = Agente()
        return agente.mostrarDispositivos(self.usuario)

    def estadoDispositivo(self):
        agente = Agente()
        return agente.mostrarEstados(self.usuario)

    def pestInicio(self):
        pes0 = ttk.Frame(self.notebook)
        self.notebook.add(pes0, text="Inicio")

        [dispMoni, estados, interfaces, estadosInterfaces] = self.mostrarDispositivos()
        Label(pes0, text="Dispositivos monitorizados: "+str(dispMoni)).grid(row=0, column=3)
        i=1
        renglon=1
        for estado in estados:
            Label(pes0, text="Dispositivo "+str(i)+": "+estado).grid(row=renglon, column=3)
            i=i+1
            renglon=renglon+1

        i=1
        for interfaz in interfaces:
            Label(pes0, text="Numero de interfaces de red en dispositivo "+str(i)+": "+ interfaz).grid(row=renglon, column=3)
            i=i+1
            renglon=renglon+1

        i=1
        for interfaz in estadosInterfaces:
            Label(pes0, text="Estado de las interfaces del dispositivo "+str(i)).grid(row=renglon,column=3)
            renglon=renglon+1
            j=1
            for estadoInterfaz in interfaz:
                Label(pes0, text="Interfaz " +str(j)+": "+estadoInterfaz).grid(row=renglon,column=3)
                renglon=renglon+1
                j=j+1
            i=i+1

    def pestInsertarAgente(self):
        pes1 = ttk.Frame(self.notebook)
        self.notebook.add(pes1, text="Insertar agente")
        Label(pes1, text="Hostname: ").grid(row=0, column=0)
        Label(pes1, text="Version SNMP: ").grid(row=1, column=0)
        Label(pes1, text="Puerto SNMP: ").grid(row=2, column=0)
        Label(pes1, text="Comunidad SNMP: ").grid(row=3, column=0)

        # Las cajitas
        Entry(pes1, textvariable=self.Hostname).grid(row=0, column=1)
        Entry(pes1, textvariable=self.Version).grid(row=1, column=1)
        Entry(pes1, textvariable=self.Puerto).grid(row=2, column=1)
        Entry(pes1, textvariable=self.Comunidad).grid(row=3, column=1)

        Button(pes1, text="Agregar", command=self.insertar).grid(row=4, column=0)

    def pestEliminarAgente(self):
        pes2 = ttk.Frame(self.notebook)
        self.notebook.add(pes2, text="Eliminar agente")
        Label(pes2, text="Comunidad:").grid(row=0, column=0)
        Entry(pes2, textvariable=self.Comunidad).grid(row=0, column=1)
        Button(pes2, text="Borrar", command=self.eliminar).grid(row=1, column=0)

    def pestEstadoDispositivo(self):
        pes3 = ttk.Frame(self.notebook)
        self.notebook.add(pes3, text="Estado del dispositivo")
        nagentes = self.estadoDispositivo()
        columna = 0
        for i in range (0, nagentes):
            t = Thread(target=printinfo, args=(i,columna,pes3,))
            t.start()
            columna+=15

    """"def pestGraficas(self):
        pes4 = ttk.Frame(self.notebook)
        self.notebook.add(pes4, text="Gráfica de dispositivos")
        grafica1()
        grafica2()
        grafica3()
        grafica4()
        grafica5()
        actualizarDatos()
        graficacion()
        while 1:
            g1 = PhotoImage(file="g1.png")
            g2 = PhotoImage(file="g2.png")
            g3 = PhotoImage(file="g3.png")
            g4 = PhotoImage(file="g4.png")
            g5 = PhotoImage(file="g5.png")

            f1 = Label(pes4,image=g1).grid(row=0, column=0)
            f2 = Label(pes4,image=g2).grid(row=0, column=1)
            f3 = Label(pes4,image=g3).grid(row=1, column=0)
            f4 = Label(pes4,image=g4).grid(row=1, column=1)
            f5 = Label(pes4,image=g5).grid(row=2, column=0)
            time.sleep(5)"""
