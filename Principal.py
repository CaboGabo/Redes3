from Agente import *
from tkinter import ttk
from tkinter import messagebox
from rrdtool1 import *
from rrdtool2 import *
from MinimosCuadrados import *
from hilos import *
from holtwinters import *
#from Graficar import *
from tkinter import *

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
        self.start = StringVar()
        self.end = StringVar()
        self.umbral = IntVar()
        self.archivorrd = StringVar()
        self.alpha = DoubleVar()
        self.beta = DoubleVar()
        self.gamma = DoubleVar()
        self.inicio()

    def inicio(self):
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill='both', expand='yes')
        self.pestInicio()
        self.pestInsertarAgente()
        self.pestEliminarAgente()
        self.pestEstadoDispositivo()
        self.pestGraficas()
        self.pesHoltWinters()
        self.pestMinimoscuadrados()

        self.window.geometry("600x650")
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

    def minimoscuadrados(self,pestana):
        tiempo = mincuad(self.archivorrd.get(),self.start.get(),self.end.get(), self.umbral.get())
        self.archivorrd.set("")
        self.start.set("")
        self.end.set("")
        self.umbral.set("")
        Label(pestana, text="Momento en que pasara el umbral: "+tiempo).grid(row=5, column=0)
        img = PhotoImage(file='graficas/prediction.png')
        a1 = Label(pestana, image=img)
        a1.image = img
        a1.grid(row=6, column=0)

    def holtwinters(self,pes):
        crearBDRRDHW(self.alpha.get(),self.beta.get(),self.gamma.get())

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
            columna+=5

    def pestGraficas(self):
        pes4 = ttk.Frame(self.notebook)
        self.notebook.add(pes4, text="Gráficas")
        grafica1()
        grafica2()
        grafica3()
        grafica4()
        grafica5()
        graficaCPU()
        graficaRAM()

        t1 = Thread(target=actualizarDatosGrafica)
        t2 = Thread(target=graficar, args=(pes4,))
        t1.start()
        t2.start()

    def pestMinimoscuadrados(self):
        pes5 = ttk.Frame(self.notebook)

        self.notebook.add(pes5, text="Minimos cuadrados")
        Label(pes5, text="Inicio: ").grid(row=0, column=0)
        Entry(pes5, textvariable=self.start).grid(row=0, column=1)
        Label(pes5, text="Final: ").grid(row=1, column=0)
        Entry(pes5, textvariable=self.end).grid(row=1, column=1)
        Label(pes5, text="Umbral: ").grid(row=2, column=0)
        Entry(pes5, textvariable=self.umbral).grid(row=2, column=1)
        Label(pes5, text="Archivo .rrd: ").grid(row=3, column=0)
        Entry(pes5, textvariable=self.archivorrd).grid(row=3, column=1)
        Button(pes5, text="Calcular minimos cuadrados", command=lambda: self.minimoscuadrados(pes5)).grid(row=4, column=0)


    def pesHoltWinters(self):
        pes6 = ttk.Frame(self.notebook)

        self.notebook.add(pes6, text="Holt Winters")
        Label(pes6, text="Alpha: ").grid(row=0, column=0)
        Entry(pes6, textvariable=self.alpha).grid(row=0, column=1)
        Label(pes6, text="Beta: ").grid(row=1, column=0)
        Entry(pes6, textvariable=self.beta).grid(row=1, column=1)
        Label(pes6, text="Gamma: ").grid(row=2, column=0)
        Entry(pes6, textvariable=self.gamma).grid(row=2, column=1)
        Button(pes6, text="Hot Wheels", command=lambda: self.holtwinters(pes6)).grid(row=3, column=0)
