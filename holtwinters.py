import rrdtool
from NotifyHW import *

def crearBDRRDHW(alpha,beta,gamma):
    ret = rrdtool.create("bdrrtool/predicthw.rrd",
                         "--start", 'N',
                         "--step", '60',
                         "DS:inoctets:COUNTER:600:U:U",
                         "RRA:AVERAGE:0.5:1:2016",
                         # RRA:HWPREDICT:rows:alpha:beta:seasonal period[:rra - num]
                         "RRA:HWPREDICT:1000:"+str(alpha)+":"+str(beta)+":288:3",
                         # RRA:SEASONAL:seasonal period:gamma:rra-num
                         "RRA:SEASONAL:288:"+str(gamma)+":2",
                         # RRA:DEVSEASONAL:seasonal period:gamma:rra-num
                         "RRA:DEVSEASONAL:288:"+str(gamma)+":2",
                         # RRA:DEVPREDICT:rows:rra-num
                         "RRA:DEVPREDICT:1000:4",
                         # RRA:FAILURES:rows:threshold:window length:rra-num
                         "RRA:FAILURES:288:7:9:4")

    # HWPREDICT rra-num is the index of the SEASONAL RRA.
    # SEASONAL rra-num is the index of the HWPREDICT RRA.
    # DEVPREDICT rra-num is the index of the DEVSEASONAL RRA.
    # DEVSEASONAL rra-num is the index of the HWPREDICT RRA.
    # FAILURES rra-num is the index of the DEVSEASONAL RRA.

    if ret:
        print
        rrdtool.error()

def actualizarHW():

    while 1: #Necesitamos aplicar el hack del puerto que da tanibet(foto que el bb8 me envio)
        #Tambien nuestra propia version del hack con easysnmp
        total_input_traffic = int(consultaSNMP('comunidadASR', 'localhost', '1.3.6.1.2.1.2.2.1.10.1'))
        total_output_traffic = int(consultaSNMP('comunidadASR', 'localhost', '1.3.6.1.2.1.2.2.1.16.1'))

        valor = str(rrdtool.last(fname) + 100) + ":" + str(total_input_traffic) + ':' + str(total_output_traffic)
        print(valor)
        ret = rrdtool.update(fname, valor)
        rrdtool.dump(fname, 'netP.xml')
        time.sleep(1)
        print(check_aberration(rrdpath, fname))

    if ret:
        print(rrdtool.error())
        time.sleep(300)