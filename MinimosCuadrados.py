import rrdtool
import time
from tkinter import *
from easysnmp import Session
from datetime import datetime

def getxvalues(muestras,inicio):
    xvalues = []
    sig = 0
    for i in range(0,muestras):
        sig = inicio + (i * 60)
        xvalues.append(sig)

    return [xvalues, sig+60]

def getvaluemedia(values,media):
    valuemedia = []
    for value in values:
        valuemedia.append(value-media)
    return valuemedia

def producto(valores1,valores2):
    prod = []
    for i in range(0,len(valores1)):
        prod.append(valores1[i]*valores2[i])
    return prod


def mincuad(archivo,inicio,final, umbral):
    struct_fecha_inicio = time.strptime(inicio,"%Y-%m-%dT%H:%M:%S")
    iniciosegundos = int(time.mktime(struct_fecha_inicio))
    if(final==""):
        finalsegundos = int(time.time())
    else:
        struct_fecha_final = time.strptime(final, "%Y-%m-%dT%H:%M:%S")
        finalsegundos = int(time.mktime(struct_fecha_final))

    [startStop, names, values] = rrdtool.fetch(archivo, 'AVERAGE', '-s', str(iniciosegundos), '-e',
                                           str(finalsegundos))

    #print('Final segundos: ',finalsegundos)
    values = [v[0] for v in values if v[0] is not None]
    muestras = len(values)
    [xvalues, ini] = getxvalues(muestras,iniciosegundos)
    yvalues = values

    sumax = sum(xvalues)
    sumay = sum(yvalues)

    xmedia = sumax/muestras
    ymedia = sumay/muestras

    xxmedia = getvaluemedia(xvalues,xmedia)
    yymedia = getvaluemedia(yvalues,ymedia)

    prod = producto(xxmedia,yymedia)
    xxmediacuadrado = producto(xxmedia,xxmedia)

    m = sum(prod)/sum(xxmediacuadrado)
    b = ymedia-(m*xmedia)

    resultado = int((umbral-b)/m)

    fechaumbral= time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(resultado))

    predecidos= getpredict(m,b,ini,finalsegundos)
    actualizarMinCuad(archivo, predecidos)
    graficarMinCuad(archivo, iniciosegundos)
    #print(predecidos)
    #print(fechaumbral)
    # Predecidos contiene los valores de x y y a graficar. Falta poner el umbral
    return fechaumbral

def getpredict(m,b,inicio,final):
    predecidos  = []
    i=1
    y = (m*inicio)+b
    predecidos.append([inicio,y])
    suma = inicio
    while(y<=100 and suma<=final):
        suma= inicio+(i*60)
        y = (m*suma)+b
        predecidos.append([suma,y])
        i+=1

    return predecidos

def actualizarMinCuad(archivo, predecidos):
    carga_CPU = 0
    for valor in predecidos:
        valores = "N:"+ str(valor[1])
        print(valores)
        rrdtool.update(archivo, valores)


def graficarMinCuad(archivo,inicio_segundos):

    ret = rrdtool.graph("graficas/prediction.png",
                        "--start", str(inicio_segundos),
                        "--end",str(rrdtool.last(archivo)),
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

"""
def minCuadBD():
    ret = rrdtool.create("bdrrdtool/trend.rrd",
                         "--start", 'N', 1540088040
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
    session = Session(hostname='localhost', community='nuevaSDLG', version=2)
    description = str(session.get(OID))
    inicio = description.index("=")
    sub = description[inicio + 2:]
    fin = sub.index("'")
    return sub[:fin]
def actualizarMinCuad():
    carga_CPU = 0
    while 1:
        carga_CPU = int(obtenerValorCPU('1.3.6.1.2.1.25.3.3.1.2.196608'))
        valor = "N:" + str(carga_CPU)
        # print(valor)
        rrdtool.update("bdrrdtool/trend.rrd", valor)
        #rrdtool.dump(archivo, 'bdrrdtool/trend.xml')
        time.sleep(1)
def graficarMinCuad(pes5):
    ultima_lectura = int(rrdtool.last("bdrrdtool/trend.rrd"))
    tiempo_final = ultima_lectura
    tiempo_incial = tiempo_final - 1300
    while 1:
        ret = rrdtool.graph("graficas/trend.png",
                            "--start", str(tiempo_incial),
                            "--vertical-label=Carga CPU",
                            "--title=Uso de CPU",
                            "--color", "ARROW#009900",
                            '--vertical-label', "Uso de CPU (%)",
                            '--lower-limit', '0',
                            '--upper-limit', '100',
                            "DEF:carga=bdrrdtool/trend.rrd:CPUload:AVERAGE",
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
time.sleep(2)"""