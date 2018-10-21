from Agente import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from rrdtool1 import *
from rrdtool2 import *
import rrdtool
from MinimosCuadrados import *
#from Graficar import *
import time
#from PIL import Image, ImageTk

def printinfo(indice, columna,pes3):
    while (1):
        lineas = []
        fila = 0
        archivo = open("informacion/informacion" + str(indice) + ".txt", "r")
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
        time.sleep(2)

def actualizarDatosGrafica():
    total_input_traffic = 0
    total_output_traffic = 0
    total_input_SegTCP = 0
    total_output_SegTCP = 0
    total_input_DatUDP = 0
    total_output_DatUDP = 0
    total_input_PaqSNMP = 0
    total_output_PaqSNMP = 0
    total_input_ICP = 0
    total_output_ICP = 0
    session = Session(hostname='localhost', community='comunidadASR', version=2)

    while 1:
        total_input_traffic = int(obtenerValor(monitoreosSNMP[0][1]))
        total_output_traffic = int(obtenerValor(monitoreosSNMP[0][2]))
        total_input_SegTCP = int(obtenerValor(monitoreosSNMP[1][1]))
        total_output_SegTCP = int(obtenerValor(monitoreosSNMP[1][2]))
        total_input_DatUDP = int(obtenerValor(monitoreosSNMP[2][1]))
        total_output_DatUDP = int(obtenerValor(monitoreosSNMP[2][2]))
        total_input_PaqSNMP = int(obtenerValor(monitoreosSNMP[3][1]))
        total_output_PaqSNMP = int(obtenerValor(monitoreosSNMP[3][2]))
        total_input_ICP = int(obtenerValor(monitoreosSNMP[4][1]))
        total_output_ICP = int(obtenerValor(monitoreosSNMP[4][2]))

        valor1 = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
        valor2 = "N:" + str(total_input_SegTCP) + ':' + str(total_output_SegTCP)
        valor3 = "N:" + str(total_input_DatUDP) + ':' + str(total_output_DatUDP)
        valor4 = "N:" + str(total_input_PaqSNMP) + ':' + str(total_output_PaqSNMP)
        valor5 = "N:" + str(total_input_ICP) + ':' + str(total_output_ICP)

        rrdtool.update('bdrrdtool/g1.rrd', valor1)
        rrdtool.dump('bdrrdtool/g1.rrd', 'bdrrdtool/g1.xml')

        rrdtool.update('bdrrdtool/g2.rrd', valor2)
        rrdtool.dump('bdrrdtool/g2.rrd', 'bdrrdtool/g2.xml')

        rrdtool.update('bdrrdtool/g3.rrd', valor3)
        rrdtool.dump('bdrrdtool/g3.rrd', 'bdrrdtool/g3.xml')

        rrdtool.update('bdrrdtool/g4.rrd', valor4)
        rrdtool.dump('bdrrdtool/g4.rrd', 'bdrrdtool/g4.xml')

        rrdtool.update('bdrrdtool/g5.rrd', valor5)
        rrdtool.dump('bdrrdtool/g5.rrd', 'bdrrdtool/g5.xml')

        time.sleep(1)




def obtenerValor(OID):
    session = Session(hostname='localhost', community='comunidadASR', version=2)
    description = str(session.get(OID))
    inicio = description.index("=")
    sub = description[inicio + 2:]
    fin = sub.index("'")

    return sub[:fin]


def graficar(pes4):
    tiempo_actual = int(time.time())
    tiempo_final = tiempo_actual - 86400
    tiempo_inicial = tiempo_final - 25920000
    fila=0
    columna=0
    Label(pes4, text="Graficas agente").grid(row=fila, column=columna)
    fila += 1
    while 1:
        fila=1

        ret1 = rrdtool.graph("graficas/g1.png",
                             "--start", str(tiempo_actual),
                             #                    "--end","N",
                             "--vertical-label=Bytes/s",
                             "DEF:inoctets=bdrrdtool/g1.rrd:inoctets:AVERAGE",
                             "DEF:outoctets=bdrrdtool/g1.rrd:outoctets:AVERAGE",
                             "AREA:inoctets#00FF00:In traffic",
                             "LINE1:outoctets#0000FF:Out traffic\r")

        img1 = PhotoImage(file="graficas/g1.png")
        a1 = Label(pes4, image=img1)
        a1.image = img1
        a1.grid(row=fila, column=columna)
        ret2 = rrdtool.graph("graficas/g2.png",
                             "--start", str(tiempo_actual),
                             #                    "--end","N",
                             "--vertical-label=Bytes/s",
                             "DEF:inoctets=bdrrdtool/g2.rrd:inoctets:AVERAGE",
                             "DEF:outoctets=bdrrdtool/g2.rrd:outoctets:AVERAGE",
                             "AREA:inoctets#00FF00:In TCP segments",
                             "LINE1:outoctets#0000FF:Out TCP segments\r")
        columna=1
        img2 = PhotoImage(file="graficas/g2.png")
        a2 = Label(pes4, image=img2)
        a2.image = img2
        a2.grid(row=fila, column=columna)
        fila += 1
        ret3 = rrdtool.graph("graficas/g3.png",
                             "--start", str(tiempo_actual),
                             #                    "--end","N",
                             "--vertical-label=Bytes/s",
                             "DEF:inoctets=bdrrdtool/g3.rrd:inoctets:AVERAGE",
                             "DEF:outoctets=bdrrdtool/g3.rrd:outoctets:AVERAGE",
                             "AREA:inoctets#00FF00:In UDP datagram",
                             "LINE1:outoctets#0000FF:Out UDP datagram\r")
        columna = 0
        img3 = PhotoImage(file="graficas/g3.png")
        a3 = Label(pes4, image=img3)
        a3.image = img3
        a3.grid(row=fila, column=columna)


        ret4 = rrdtool.graph("graficas/g4.png",
                             "--start", str(tiempo_actual),
                             #                    "--end","N",
                             "--vertical-label=Bytes/s",
                             "DEF:inoctets=bdrrdtool/g4.rrd:inoctets:AVERAGE",
                             "DEF:outoctets=bdrrdtool/g4.rrd:outoctets:AVERAGE",
                             "AREA:inoctets#00FF00:In SNMP packages",
                             "LINE1:outoctets#0000FF:Out SNMP packages\r")
        columna = 1
        img4 = PhotoImage(file="graficas/g4.png")
        a4 = Label(pes4, image=img4)
        a4.image = img4
        a4.grid(row=fila, column=columna)
        fila +=1

        ret5 = rrdtool.graph("graficas/g5.png",
                             "--start", str(tiempo_actual),
                             #                    "--end","N",
                             "--vertical-label=Bytes/s",
                             "DEF:inoctets=bdrrdtool/g5.rrd:inoctets:AVERAGE",
                             "DEF:outoctets=bdrrdtool/g5.rrd:outoctets:AVERAGE",
                             "AREA:inoctets#00FF00:In ICP entries",
                             "LINE1:outoctets#0000FF:Out ICP entries\r")
        columna = 0
        img5 = PhotoImage(file="graficas/g5.png")
        a5 = Label(pes4, image=img5)
        a5.image = img5
        a5.grid(row=fila, column=columna)


        time.sleep(3)


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
        self.inicio()

    def inicio(self):
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill='both', expand='yes')
        self.pestInicio()
        self.pestInsertarAgente()
        self.pestEliminarAgente()
        self.pestEstadoDispositivo()
        self.pestGraficas()
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

    """def minimoscuadrados(self,pes5):
        minCuadBD()
        t3 = Thread(target=actualizarMinCuad)
        t4 = Thread(target=graficarMinCuad, args=(pes5,))
        t3.start()
        t4.start()
        self.archivorrd.set("")
        self.start.set("")
        self.end.set("")
        self.umbral.set("")
        #resultado = mincuad(self.archivorrd, self.start, self.end, self.umbral)
        resultado=0
        messagebox.showinfo("Resultados","Se llegará al umbral en: " + resultado)"""

    def minimoscuadrados(self,pestana):
        tiempo = mincuad(self.archivorrd.get(),self.start.get(),self.end.get(), self.umbral.get())
        self.archivorrd.set("")
        self.start.set("")
        self.end.set("")
        self.umbral.set("")
        Label(pestana, text="Momento en que pasara el umbral: "+tiempo).grid(row=5, column=0)
        img = PhotoImage(file="graficas/prediction.png")
        a1 = Label(pestana, image=img)
        a1.image = img
        a1.grid(row=6, column=0)

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