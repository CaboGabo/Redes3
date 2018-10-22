import rrdtool
import time
from builtins import int, str, len, sum, range
from math import floor


def mincuad(archivo,inicio,final,umbral):
    struct_fecha_inicio = time.strptime(inicio, '%Y-%m-%dT%H:%M:%S')
    iniciosegundos = int(time.mktime(struct_fecha_inicio))
    if(final==""):
        finalsegundos=int(time.time())
    else:
        struct_fecha_final = time.strptime(final, '%Y-%m-%dT%H:%M:%S')
        finalsegundos = int(time.mktime(struct_fecha_final))

    # Obtencion de los datos de fetch
    [startStop, names, values] = rrdtool.fetch(archivo, 'AVERAGE', '-s', str(iniciosegundos), 'e', str(finalsegundos))

    inicioMuestras = rrdtool.first(archivo)
    steps = startStop[2] #Da los steps
    div = obtenerDiv(iniciosegundos,inicioMuestras,steps)
    values = [v[0] for v in values if v[0] is not None]
    muestras = len(values)
    #Asignacion tipo funcion
    [x, y] = asignacion(values,div,inicioMuestras,steps)
    sumax = sum(x)
    sumay = sum(y)

    mediax = sumax/muestras
    mediay = sumay/muestras

    xmediax = obtenerValorMedia(x,mediax)
    ymediay = obtenerValorMedia(y,mediay)

    xmediaxymediay = producto(xmediax,ymediay)
    xmediaxcuadrado = producto(xmediax,xmediax)

    m = sum(xmediaxymediay)/sum(xmediaxcuadrado)
    b = mediay - (m*mediax)

    resultado = int((umbral-b)/m)

    fechaumbral = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(resultado))


    tiempoInicialPredicciones = x[0]
    [predecidosx, predecidosy] = obtenerPredecidos(m,b,tiempoInicialPredicciones, finalsegundos, steps)

    #archivorrdpredecido = crearGrafica(predecidosy,tiempoInicialPredicciones, steps, names,archivo)
    #actualizarGrafica(archivorrdpredecido,predecidosx,predecidosy)
    #graficar(archivo,tiempoInicialPredicciones)

    return fechaumbral

def crearGrafica(valoresy, tiempoInicial, steps, names,archivo):
    print(rrdtool.info(archivo))
    muestras = len(valoresy)
    ret = rrdtool.create('predicciones/trend.rrd',
                        "--start", str(tiempoInicial),
                        "--step", str(steps),
                        "DS:"+names[0]+":GAUGE:600:U:U",
                        "RRA:AVERAGE:0.5:1:"+str(muestras))
    return 'predicciones/'+archivo

def actualizarGrafica(archivo, predecidosx,predecidosy):
    i=0
    for predecido in predecidosy:
        valor = str(predecidosx[i])+':'+str(predecido)
        print(valor)
        rrdtool.update(archivo, valor)
        i+=1

def graficar(archivo,inicio):
    ret = rrdtool.graph("graficas/prediction.png",
                        "--start", str(inicio),
                        "--end", str(rrdtool.last(archivo)),
                        "--vertical-label=Carga CPU",
                        "--title=Uso de CPU",
                        "--color", "ARROW#009900",
                        '--vertical-label', "Uso de CPU (%)",
                        '--lower-limit', '0',
                        '--upper-limit', '100',
                        "DEF:carga=" + archivo + ":CPUload:AVERAGE",
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


def obtenerPredecidos(m,b,tiempoInicial, tiempoFinal, steps):
    x = []
    y = []

    contador = tiempoInicial
    yvalor = (m * contador) + b

    x.append(contador)
    y.append(yvalor)
    i=1
    while(yvalor<=100 and contador<=tiempoFinal):
        contador = tiempoInicial+(i*steps)
        yvalor = (m*contador) + b

        x.append(contador)
        y.append(yvalor)
        i+=1

    return [x,y]



def obtenerValorMedia(valores,media):
    valormedia = []
    for valor in valores:
        valormedia.append(valor-media)
    return valormedia

def producto(valores1, valores2):
    #Deben ser iguales en tamaño
    prod = []
    for i in range(0,len(valores1)):
        prod.append(valores1[i]*valores2[i])
    return prod

def obtenerDiv(iniciosegundos,inicioMuestras,steps):
    div = floor((iniciosegundos - inicioMuestras) / steps) + 1
    if (div <= 0):
        div = 0

    return div

def asignacion(values,div,inicioMuestras, steps):
    i=div
    x=[]
    y=[]
    for value in values:
        x.append(inicioMuestras + (i * steps))
        y.append(value)
        i += 1
    return [x,y]
