import sys
import rrdtool
import time

def graficacion():
    tiempo_actual = int(time.time())
    tiempo_final = tiempo_actual - 86400
    tiempo_inicial = tiempo_final -25920000

    while 1:
        ret1 = rrdtool.graph( "g1.png",
                         "--start",'1537494660',
     #                    "--end","N",
                         "--vertical-label=Bytes/s",
                         "DEF:inoctets=g1.rrd:inoctets:AVERAGE",
                         "DEF:outoctets=g1.rrd:outoctets:AVERAGE",
                         "AREA:inoctets#00FF00:In traffic",
                         "LINE1:outoctets#0000FF:Out traffic\r")

        ret2 = rrdtool.graph("g2.png",
                            "--start", '1537494660',
                            #                    "--end","N",
                            "--vertical-label=Bytes/s",
                            "DEF:inoctets=g2.rrd:inoctets:AVERAGE",
                            "DEF:outoctets=g2.rrd:outoctets:AVERAGE",
                            "AREA:inoctets#00FF00:In TCP segments",
                            "LINE1:outoctets#0000FF:Out TCP segments\r")
        ret3 = rrdtool.graph("g3.png",
                            "--start", '1537494660',
                            #                    "--end","N",
                            "--vertical-label=Bytes/s",
                            "DEF:inoctets=g3.rrd:inoctets:AVERAGE",
                            "DEF:outoctets=g3.rrd:outoctets:AVERAGE",
                            "AREA:inoctets#00FF00:In UDP datagram",
                            "LINE1:outoctets#0000FF:Out UDP datagram\r")
        ret4 = rrdtool.graph("g4.png",
                             "--start", '1537494660',
                             #                    "--end","N",
                             "--vertical-label=Bytes/s",
                             "DEF:inoctets=g4.rrd:inoctets:AVERAGE",
                             "DEF:outoctets=g4.rrd:outoctets:AVERAGE",
                             "AREA:inoctets#00FF00:In SNMP packages",
                             "LINE1:outoctets#0000FF:Out SNMP packages\r")
        ret5 = rrdtool.graph("g5.png",
                             "--start", '1537494660',
                             #                    "--end","N",
                             "--vertical-label=Bytes/s",
                             "DEF:inoctets=g5.rrd:inoctets:AVERAGE",
                             "DEF:outoctets=g5.rrd:outoctets:AVERAGE",
                             "AREA:inoctets#00FF00:In ICP entries",
                             "LINE1:outoctets#0000FF:Out ICP entries\r")


        time.sleep(5)
