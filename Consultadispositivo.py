from estadoDispositivo import *
from easysnmp import Session, EasySNMPTimeoutError


def obtenerSesion(hostname,community, version, tipo, elementoLista):
    session = Session(hostname=hostname, community=community, version=version)
    if(tipo=="walk"):
        try:
            description = str(session.walk(elementoLista))
        except EasySNMPTimeoutError:
            description = 'Timeout Error'
    elif(tipo=="get"):
        try:
            description = str(session.get(elementoLista))
        except EasySNMPTimeoutError:
            description = 'Timeout Error'
    else:
        description = 'No fue seleccionada una opción correcta'
    return description

def obtenerSubcadena(cadena):
    if(cadena=='Timeout Error'):
        return cadena
    inicio = cadena.index("=")
    sub = cadena[inicio+2:]
    fin = sub.index("'")
    return sub[:fin]

def nombreHost(hostname_var):
    return hostname_var

def direccionip(hostname,community,version):
    return obtenerSubcadena(obtenerSesion(hostname,community,version,"walk",lista_oid[0]))

def nombreDis(hostname,community,version):
    return obtenerSubcadena(obtenerSesion(hostname,community,version,"get",lista_oid[1]))

def version(versionsnmp):
    return versionsnmp

def so(hostname,community,version):
    cadena = obtenerSesion(hostname,community,version,"get",lista_oid[2])
    if(cadena=='Timeout Error'):
        return cadena
    inicio = cadena.index("=")
    sub = cadena[inicio + 2:]
    fin = sub.index(" ")

    return sub[:fin]

def noInterfacesRed(hostname,community,version):
    return obtenerSubcadena(obtenerSesion(hostname,community,version,"get",lista_oid[3]))

def tiempoUltimoReinicio(hostname,community,version):
    subcadena = obtenerSubcadena(obtenerSesion(hostname,community,version,"get",lista_oid[4]))
    if(subcadena=='Timeout Error'):
        return subcadena
    milisegundos= int(subcadena)
    num= milisegundos/100
    hor = (int(num / 3600))
    minu = int((num - (hor * 3600)) / 60)
    seg = num - ((hor * 3600) + (minu * 60))
    tiempo=str(hor) + "h " + str(minu) + "m " + str(seg) + "s"
    return tiempo

def ubicacionFisica(hostname,community,version):
    return obtenerSubcadena(obtenerSesion(hostname,community,version,"get",lista_oid[5]))

def infContacto(hostname,community,version):
    return obtenerSubcadena(obtenerSesion(hostname,community,version,"get",lista_oid[6]))

def estatusInterfaces(hostname, community, version, num):
    session = Session(hostname=hostname, community=community, version=version)
    try:
        description = str(session.get('1.3.6.1.2.1.2.2.1.8.' + str(num)))
    except EasySNMPTimeoutError:
        description = 'Timeout Error'
    return obtenerSubcadena(description)

def ifInDiscards(hostname,community, version):
    return obtenerSubcadena(obtenerSesion(hostname,community,version,"get",'1.3.6.1.2.1.2.2.1.13.1'))

def porcentajeCPU(hostname,community,version):
    return obtenerSubcadena(obtenerSesion(hostname,community, version, "get",rendimientoSNMP[0]))

def porcentajeRAM(hostname,community,version):
    ramusada = int(obtenerSubcadena(obtenerSesion(hostname,community, version, "get",rendimientoSNMP[1])))
    ramtotal = int(obtenerSubcadena(obtenerSesion(hostname,community, version, "get",rendimientoSNMP[2])))
    porcentaje = int((ramusada*100)/ramtotal)
    return str(porcentaje)