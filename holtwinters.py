import rrdtool
from tkinter import *
#from NotifyHW import *
from getSNMP import *
from easysnmp import Session, EasySNMPTimeoutError
import time
def crearBDRRDHW(alpha,beta,gamma):
    ret = rrdtool.create("bdrrdtool/netPred.rrd",
                         "--start", 'N',
                         "--step", '100',
                         "DS:inoctets:COUNTER:600:U:U",
                         "DS:outoctets:COUNTER:600:U:U",
                         "RRA:AVERAGE:0.5:1:20",
                         # RRA:HWPREDICT:rows:alpha:beta:seasonal period[:rra - num]
                         "RRA:HWPREDICT:50:"+str(alpha)+":"+str(beta)+":10:3",  # -----------1
                         # RRA:SEASONAL:seasonal period:gamma:rra-num
                         "RRA:SEASONAL:10:"+str(gamma)+":2",  # --------------2 con esos dos funcionan las predicciones
                         # RRA:DEVSEASONAL:seasonal period:gamma:rra-num
                         "RRA:DEVSEASONAL:10:"+str(gamma)+":2",  # *** el valor de gamma debe ser igual al de seasonal
                         # RRA:DEVPREDICT:rows:rra-num
                         "RRA:DEVPREDICT:50:4",  # *** usamos estos dos para almacenar fallas en failures
                         # RRA:FAILURES:rows:threshold:window length:rra-num
                         "RRA:FAILURES:50:7:9:4")

    # Entre más filas, mejor es la predicción, el 50 se cambia por 1000 y el 10 por 288

    # Valor de alpha muy grande significa que va a tomar los último valores en los serie de tiempo
    # Valor de alpha pequeño significa que va a tomar los primeros valores en la serie de tiempo
    # Valor de beta diferencia de periodo anterior y periodo actual
    # Valor de beta muy grande significa que se va a trabajar con la propia estimación, es decir, las prediction
    # Valor de beta pequeña, va a trabajar con los puntos observados

    # Seasonal
    # Valor de gamma bajo quiere decir que va a trabajar con los valores observados, no le va a dar tanta importancia
    # a las temporadas anteriores

    if ret:
        print
        rrdtool.error()

def actualizarHW():

    while 1:
        # total_input_traffic = int(consultaSNMP('comunidadASR', 'localhost', '1.3.6.1.2.1.2.2.1.10.1'))
        # total_output_traffic = int(consultaSNMP('comunidadASR', 'localhost', '1.3.6.1.2.1.2.2.1.16.1'))

        total_input_traffic = int(obtenerValor('1.3.6.1.2.1.2.2.1.10.1'))
        total_output_traffic = int(obtenerValor('1.3.6.1.2.1.2.2.1.16.1'))

        valor = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
        ret = rrdtool.update("bdrrdtool/netPred.rrd", valor)
        #rrdtool.dump(fname, 'netP.xml')
        time.sleep(1)
        #print(check_aberration(rrdpath, fname))

    if ret:
        print(rrdtool.error())
        time.sleep(300)

def graficarHW(alpha,pestana):
    fname = "bdrrdtool/netPred.rrd"
    title = "Deteccion de comportamiento anomalo, valor de Alpha "+str(alpha)
    endDate = rrdtool.last(fname)
    begDate = endDate - 1800
    while 1:
        rrdtool.tune(fname, '--alpha', '0.1')
        ret = rrdtool.graph("graficas/predHW.png",
                            '--start', str(begDate), '--title=' + title,
                            "--vertical-label=Bytes/s",
                            '--slope-mode',
                            "DEF:obs=" + fname + ":inoctets:AVERAGE",
                            "DEF:outoctets=" + fname + ":outoctets:AVERAGE",
                            "DEF:pred=" + fname + ":inoctets:HWPREDICT",
                            "DEF:dev=" + fname + ":inoctets:DEVPREDICT",
                            "DEF:fail=" + fname + ":inoctets:FAILURES",

                            # "RRA:DEVSEASONAL:1d:0.1:2",
                            # "RRA:DEVPREDICT:5d:5",
                            # "RRA:FAILURES:1d:7:9:5""
                            "CDEF:scaledobs=obs,8,*",
                            "CDEF:upper=pred,dev,2,*,+",
                            "CDEF:lower=pred,dev,2,*,-",
                            "CDEF:scaledupper=upper,8,*",
                            "CDEF:scaledlower=lower,8,*",
                            "CDEF:scaledpred=pred,8,*",
                            "TICK:fail#FDD017:1.0:Fallas",
                            "LINE3:scaledobs#00FF00:In traffic",
                            "LINE1:scaledpred#FF00FF:Prediccion\\n",
                            # "LINE1:outoctets#0000FF:Out traffic",
                            "LINE1:scaledupper#ff0000:Upper Bound Average bits in\\n",
                            "LINE1:scaledlower#0000FF:Lower Bound Average bits in")

        img1 = PhotoImage(file="graficas/predHW.png")
        a1 = Label(pestana, image=img1)
        a1.image = img1
        a1.grid(row=4, column=0)
        time.sleep(1)

def obtenerValor(OID):
    session = Session(hostname='localhost', community='comunidadASR', version=2)
    description = str(session.get(OID))
    inicio = description.index("=")
    sub = description[inicio + 2:]
    fin = sub.index("'")

    return sub[:fin]