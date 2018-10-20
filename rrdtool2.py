#Actualizar los valores en el archivo de rrdtool
import time
import rrdtool
from easysnmp import Session
from estadoDispositivo import *

def actualizarDatos():
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
    session = Session(hostname='localhost', community='MacCommunity', version=2)

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

        rrdtool.update('g1.rrd', valor1)
        rrdtool.dump('g1.rrd','g1.xml')

        rrdtool.update('g2.rrd', valor2)
        rrdtool.dump('g2.rrd', 'g2.xml')

        rrdtool.update('g3.rrd', valor3)
        rrdtool.dump('g3.rrd', 'g3.xml')

        rrdtool.update('g4.rrd', valor4)
        rrdtool.dump('g4.rrd', 'g4.xml')

        rrdtool.update('g5.rrd', valor5)
        rrdtool.dump('g5.rrd', 'g5.xml')

        time.sleep(1)

    if ret:
        print(rrdtool.error())
        time.sleep(300)

def obtenerValor(OID):
    session = Session(hostname='localhost', community='MacCommunity', version=2)
    description = str(session.get(OID))
    inicio = description.index("=")
    sub = description[inicio + 2:]
    fin = sub.index("'")

    return sub[:fin]

