from Consultadispositivo import *
from tkinter import *
import rrdtool
import time
from Notify import send_alert_attached

def getinfo(hostname,version,comunidad,indice):

    while(1):
        archivo = open("informacion/informacion"+str(indice)+".txt", "w")
        ip = direccionip(hostname, comunidad, version)
        nombre = nombreDis(hostname, comunidad, version)
        sistemaop = so(hostname, comunidad, version)
        interfaces = noInterfacesRed(hostname, comunidad, version)
        tiempo = tiempoUltimoReinicio(hostname, comunidad, version)
        ubicacion = ubicacionFisica(hostname, comunidad, version)
        contacto = infContacto(hostname, comunidad, version)
        porCPU = porcentajeCPU(hostname, comunidad, version)
        porRAM = porcentajeRAM(hostname, comunidad, version)
        archivo.write(hostname + '\n')
        archivo.write(str(version) + '\n')
        archivo.write(comunidad+ '\n')
        archivo.write(ip + '\n')
        archivo.write(nombre + '\n')
        archivo.write(sistemaop + '\n')
        archivo.write(interfaces + '\n')
        archivo.write(tiempo+'\n')
        archivo.write(ubicacion+'\n')
        archivo.write(contacto+ '\n')
        archivo.write(porCPU+ '\n')
        archivo.write(porRAM+'\n')
        archivo.close()
        time.sleep(2)

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
            Label(pes3, text="Porcentaje RAM usada: " + lineas[11]).grid(row=fila, column=columna)
            fila += 1
            if (sistemaop == "Windows\n"):
                img1 = PhotoImage(file="imagenes/windows.png")
                a = Label(pes3, image=img1)
                a.image = img1
                a.grid(row=fila, column=columna)
            elif (sistemaop == "Linux\n"):
                img2 = PhotoImage(file="imagenes/linux.png")
                a = Label(pes3, image=img2)
                a.image = img2
                a.grid(row=fila, column=columna)
            else:
                img3 = PhotoImage(file="imagenes/desconocido.png")
                a = Label(pes3, image=img3)
                a.image = img3
                a.grid(row=fila, column=columna)
            archivo.close()
        time.sleep(2)

def actualizarDatosGrafica():
    session = Session(hostname='localhost', community='comunidadASR', version=2)
    enviadoReadyCPU = True
    enviadoSetCPU = True
    enviadoGoCPU = True
    enviadoReadyRAM = True
    enviadoSetRAM = True
    enviadoGoRAM = True
    while 1:

        #Para las graficas normales
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

        # Empieza linea base

        uso_CPU1 = int(obtenerValor(cpuSNMP[0]))
        valor1 = "N:" + str(uso_CPU1)
        rrdtool.update("bdrrdtool/gCPU1.rrd", valor1)
        uso_CPU2 = int(obtenerValor(cpuSNMP[1]))
        valor2 = "N:" + str(uso_CPU1)
        rrdtool.update("bdrrdtool/gCPU2.rrd", valor2)
        uso_CPU3 = int(obtenerValor(cpuSNMP[2]))
        valor3 = "N:" + str(uso_CPU1)
        rrdtool.update("bdrrdtool/gCPU3.rrd", valor3)
        uso_CPU4 = int(obtenerValor(cpuSNMP[3]))
        valor4 = "N:" + str(uso_CPU1)
        rrdtool.update("bdrrdtool/gCPU4.rrd", valor4)

        ramusada = int(obtenerValor(rendimientoSNMP[1]))
        ramtotal = int(obtenerValor(rendimientoSNMP[2]))
        porcentaje = int((ramusada * 100) / ramtotal)
        valor2 = "N:" + str(porcentaje)
        rrdtool.update("bdrrdtool/gRAM.rrd", valor2)
        cpu_utilizado=0
        if (uso_CPU1 > 40):
            cpu_utilizado = 1
        elif (uso_CPU2 > 40):
            cpu_utilizado = 2
        elif (uso_CPU3 > 40):
            cpu_utilizado = 3
        elif (uso_CPU4 > 40):
            cpu_utilizado = 4

        if (uso_CPU1 > 40 or uso_CPU2>40 or uso_CPU3>40 or uso_CPU4>40 and enviadoReadyCPU):
            send_alert_attached("Sobrepasa Umbral ready del uso del CPU", "CPU",cpu_utilizado)
            enviadoReadyCPU = False
        elif (uso_CPU1 > 50  or uso_CPU2>50 or uso_CPU3>50 or uso_CPU4>50 and enviadoSetCPU):
            send_alert_attached("Sobrepasa Umbral set del uso del CPU", "CPU",cpu_utilizado)
            enviadoSetCPU = False
        elif (uso_CPU1 > 60 or uso_CPU2>60 or uso_CPU3>60 or uso_CPU4>60 and enviadoGoCPU):
            send_alert_attached("Sobrepasa Umbral go del uso del CPU", "CPU",cpu_utilizado)
            enviadoGoCPU = False

        if (porcentaje > 45 and porcentaje < 50 and enviadoReadyRAM):
            send_alert_attached("Sobrepasa Umbral ready del uso de la RAM", "RAM",cpu_utilizado)
            enviadoReadyRAM = False
        elif (porcentaje > 50 and porcentaje < 60 and enviadoSetRAM):
            enviadoSetRAM = False
            send_alert_attached("Sobrepasa Umbral set del uso de la RAM", "RAM",cpu_utilizado)
        elif (porcentaje > 60 and enviadoGoRAM):
            enviadoGoRAM = False
            send_alert_attached("Sobrepasa Umbral go del uso de la RAM", "RAM",cpu_utilizado)

        time.sleep(1)

def obtenerValor(OID):
    session = Session(hostname='localhost', community='comunidadASR', version=2)
    description = str(session.get(OID))
    inicio = description.index("=")
    sub = description[inicio + 2:]
    fin = sub.index("'")

    return sub[:fin]

def graficar(pes4):
    ultima_lectura = int(rrdtool.last("bdrrdtool/g1.rrd"))
    tiempo_final = ultima_lectura
    tiempo_inicial = tiempo_final - 1300

    ultima_lectura_cpu_ram = int(rrdtool.last("bdrrdtool/gCPU1.rrd"))
    tiempo_final_cpu_ram = ultima_lectura_cpu_ram
    tiempo_inicial_cpu_ram = tiempo_final_cpu_ram - 1800

    fila=0
    columna=0
    Label(pes4, text="Graficas agente").grid(row=fila, column=columna)
    fila += 1
    while 1:
        fila=1

        ret1 = rrdtool.graph("graficas/g1.png",
                             "--start", str(tiempo_inicial),
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
                             "--start", str(tiempo_inicial),
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
                             "--start", str(tiempo_inicial),
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
                             "--start", str(tiempo_inicial),
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
                             "--start", str(tiempo_inicial),
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

        ret6 = rrdtool.graphv("graficas/gCPU1.png",
                             "--start", str(tiempo_inicial_cpu_ram),
                             "--vertical-label=Carga CPU",
                             "--title=Uso de CPU 1",
                             "--color", "ARROW#009900",
                             '--vertical-label', "Uso de CPU (%)",
                             '--lower-limit', '0',
                             '--upper-limit', '100',
                             "DEF:carga=bdrrdtool/gCPU1.rrd:CPUload:AVERAGE",
                             "AREA:carga#00FF00:CPU load",
                             "LINE1:30",
                             "AREA:5#ff000022:stack",
                             "HRULE:45#0000ff:ready",
                             "HRULE:50#FFFF00:set",
                             "HRULE:60#FF0000:go")

        ret7 = rrdtool.graphv("graficas/gCPU2.png",
                              "--start", str(tiempo_inicial_cpu_ram),
                              "--vertical-label=Carga CPU",
                              "--title=Uso de CPU 2",
                              "--color", "ARROW#009900",
                              '--vertical-label', "Uso de CPU (%)",
                              '--lower-limit', '0',
                              '--upper-limit', '100',
                              "DEF:carga=bdrrdtool/gCPU2.rrd:CPUload:AVERAGE",
                              "AREA:carga#00FF00:CPU load",
                              "LINE1:30",
                              "AREA:5#ff000022:stack",
                              "HRULE:45#0000ff:ready",
                              "HRULE:50#FFFF00:set",
                              "HRULE:60#FF0000:go")

        ret8 = rrdtool.graphv("graficas/gCPU3.png",
                              "--start", str(tiempo_inicial_cpu_ram),
                              "--vertical-label=Carga CPU",
                              "--title=Uso de CPU 3",
                              "--color", "ARROW#009900",
                              '--vertical-label', "Uso de CPU (%)",
                              '--lower-limit', '0',
                              '--upper-limit', '100',
                              "DEF:carga=bdrrdtool/gCPU3.rrd:CPUload:AVERAGE",
                              "AREA:carga#00FF00:CPU load",
                              "LINE1:30",
                              "AREA:5#ff000022:stack",
                              "HRULE:45#0000ff:ready",
                              "HRULE:50#FFFF00:set",
                              "HRULE:60#FF0000:go")


        ret9 = rrdtool.graphv("graficas/gCPU4.png",
                              "--start", str(tiempo_inicial_cpu_ram),
                              "--vertical-label=Carga CPU",
                              "--title=Uso de CPU 3",
                              "--color", "ARROW#009900",
                              '--vertical-label', "Uso de CPU (%)",
                              '--lower-limit', '0',
                              '--upper-limit', '100',
                              "DEF:carga=bdrrdtool/gCPU4.rrd:CPUload:AVERAGE",
                              "AREA:carga#00FF00:CPU load",
                              "LINE1:30",
                              "AREA:5#ff000022:stack",
                              "HRULE:45#0000ff:ready",
                              "HRULE:50#FFFF00:set",
                              "HRULE:60#FF0000:go")
        fila+=1
        Label(pes4, text="Gráficas del uso de CPU: ").grid(row=fila, column=0)
        fila+=1
        columna= 0
        img6a = PhotoImage(file="graficas/gCPU1.png")
        a6a = Label(pes4, image=img6a)
        a6a.image = img6a
        a6a.grid(row=fila, column=columna)
        columna = 1
        img6b = PhotoImage(file="graficas/gCPU2.png")
        a6b = Label(pes4, image=img6b)
        a6b.image = img6b
        a6b.grid(row=fila, column=columna)
        fila += 1

        columna = 0
        img6c = PhotoImage(file="graficas/gCPU3.png")
        a6c = Label(pes4, image=img6c)
        a6c.image = img6c
        a6c.grid(row=fila, column=columna)
        columna = 1
        img6d = PhotoImage(file="graficas/gCPU4.png")
        a6d = Label(pes4, image=img6d)
        a6d.image = img6d
        a6d.grid(row=fila, column=columna)
        fila += 1
        Label(pes4, text="Gráfica del uso de la RAM: ").grid(row=fila, column=0)
        fila += 1

        ret10 = rrdtool.graphv("graficas/gRAM.png",
                             "--start", str(tiempo_inicial_cpu_ram),
                             "--vertical-label=Carga RAM",
                             "--title=Uso de RAM",
                             "--color", "ARROW#009900",
                             '--vertical-label', "Uso de RAM (%)",
                             '--lower-limit', '0',
                             '--upper-limit', '100',
                             "DEF:carga=bdrrdtool/gRAM.rrd:RAMload:AVERAGE",
                             "AREA:carga#00FF00:RAM load",
                             "LINE1:30",
                             "AREA:5#ff000022:stack",
                             "HRULE:45#0000ff:ready",
                             "HRULE:50#FFFF00:set",
                             "HRULE:60#FF0000:go")

        columna=0
        img7 = PhotoImage(file="graficas/gRAM.png")
        a7 = Label(pes4, image=img7)
        a7.image = img7
        a7.grid(row=fila, column=columna)
        time.sleep(3)
