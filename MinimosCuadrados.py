import rrdtool
import time
from tkinter import *
from easysnmp import Session
from datetime import datetime

"""def mincuad(archivo,inicio,final, umbral):
    #No se como hacer que salga el inicio ni el final asi que solo lo pongo asi yolo
    startStop, names, values = rrdtool.fetch(archivo,"average", '-s',inicio, '-e', final)
    for v in values:
        print(v)
"""
def minCuadBD():
    ret = rrdtool.create("bdrrdtool/trend.rrd",
                         "--start", 'N',
                         "--step", '60',
                         "DS:CPUload:GAUGE:600:U:U",
                         "RRA:AVERAGE:0.5:1:24")

def getStartRRD(fecha_ingresada,hora_ingresada):# la fecha de la maestra es 9/10/2017  13:50 hrs
    #la fecha del rrdtool 1/1/1970
    formato = "%d/%m/%Y"
    fecha_ult = datetime.strptime(fecha_ingresada, formato)
    fecha_prim = datetime.strptime("1/1/1970", formato)
    diferencia = fecha_ult - fecha_prim
    segundos_obt = diferencia.days * 86400

    horas = hora_ingresada[:2]
    minutos = hora_ingresada[3:]
    segundos_obt2 = int(horas) * 3600 + int(minutos) * 60
    segundos_tot = segundos_obt + segundos_obt2
    return segundos_tot



def obtenerValorCPU(OID):
    session = Session(hostname='localhost', community='comunidadASR', version=2)
    description = str(session.get(OID))
    inicio = description.index("=")
    sub = description[inicio + 2:]
    fin = sub.index("'")

    return sub[:fin]

def actualizarMinCuad(archivo):
    carga_CPU = 0

    while 1:
        carga_CPU = int(obtenerValorCPU('1.3.6.1.2.1.25.3.3.1.2.196608'))

        valor = "N:" + str(carga_CPU)
        # print(valor)
        rrdtool.update(archivo, valor)
        #rrdtool.dump(archivo, 'bdrrdtool/trend.xml')
        time.sleep(1)

def graficarMinCuad(pes5,archivo,tiempo_dado):
    ultima_lectura = int(rrdtool.last(archivo))
    tiempo_final = ultima_lectura
    tiempo_incial = tiempo_final - 1300
    while 1:
        ret = rrdtool.graph("graficas/trend.png",
                            "--start", str(tiempo_dado),
                            "--vertical-label=Carga CPU",
                            "--title=Uso de CPU",
                            "--color", "ARROW#009900",
                            '--vertical-label', "Uso de CPU (%)",
                            '--lower-limit', '0',
                            '--upper-limit', '100',
                            "DEF:carga="+archivo+":CPUload:AVERAGE",
                            "AREA:carga#00FF00:CPU load",

                            "LINE1:30",
                            "AREA:5#ff000022:stack",
                            "VDEF:CPUlast=carga,LAST",
                            "VDEF:CPUmin=carga,MINIMUM",
                            "VDEF:CPUavg=carga,AVERAGE",
                            "VDEF:CPUmax=carga,MAXIMUM",

                            "COMMENT:                         Now          Min             Avg             Max//n",
                            "GPRINT:CPUlast:%12.0lf%s",
                            "GPRINT:CPUmin:%10.0lf%s",
                            "GPRINT:CPUavg:%13.0lf%s",
                            "GPRINT:CPUmax:%13.0lf%s",
                            "VDEF:a=carga,LSLSLOPE",
                            "VDEF:b=carga,LSLINT",
                            'CDEF:avg2=carga,POP,a,COUNT,*,b,+',
                            "LINE2:avg2#FFBB00")
        img1 = PhotoImage(file="graficas/trend.png")
        a1 = Label(pes5, image=img1)
        a1.image = img1
        a1.grid(row=6, column=0)

        time.sleep(2)

