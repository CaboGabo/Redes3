from Conexion import *
from Consultadispositivo import *
from threading import Thread
import time


def getinfo(hostname,version,comunidad,indice):

    while(1):
        archivo = open("informacion"+str(indice)+".txt", "w")
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
        time.sleep(1)

class Agente(Conexion):
    def insertar(self, hostname, versionSNMP, puertoSNMP, comunidad, usuario):
        con = self.conectar()
        cursor = con.cursor()
        cursor.execute("select idUsuario from Usuario where usuario='" + usuario + "';")
        result = cursor.fetchone()
        idUsuario = str(result[0])
        cursor.execute("insert into Agente values(null,'" + hostname + "','" + str(versionSNMP) + "'," + str(puertoSNMP) + ",'" + comunidad + "',"+ idUsuario+");")
        con.commit()
        self.cerrar(con)

    def eliminar(self,comunidad,usuario):
        con = self.conectar()
        cursor = con.cursor()
        cursor.execute("delete from Agente where comunidadSNMP = '" +comunidad +"';")
        con.commit()
        self.cerrar(con)

    def mostrarDispositivos(self, usuario):
        con = self.conectar()
        cursor = con.cursor()
        cursor.execute("select idUsuario from Usuario where usuario='" + usuario + "';")
        result = cursor.fetchone()
        idUsuario = str(result[0])
        cursor.execute("select count(*) from Agente where idUsuario='"+idUsuario+"';")
        result = cursor.fetchone()
        dispositivosMonitorizados = result[0]

        cursor.execute("select * from Agente where idUsuario='" + idUsuario + "';")
        rows = cursor.fetchall()
        hostname = []
        version = []
        comunidad = []
        estados = []
        interfaces = []
        i=0
        for row in rows:
            hostname.append(row[1])
            version.append(row[2])
            comunidad.append(row[4])
            host = hostname.__getitem__(i)
            v = int(version.__getitem__(i))
            com = comunidad.__getitem__(i)
            respuesta = direccionip(host,com,v)

            if(respuesta!=""):
                estados.append('Up')
            else:
                estados.append('Down')
            respuesta = noInterfacesRed(host,com,v)
            interfaces.append(respuesta)
        resultadoGrup = []
        j=0
        for interface in interfaces:
            resultadoInd=[]
            for i in range(0,int(interface)-1):
                resultado = int(estatusInterfaces(hostname.__getitem__(j),comunidad.__getitem__(j),version.__getitem__(j),i+1))
                if(resultado==1):
                    resultadoInd.append("Up")
                elif(resultado==2):
                    resultadoInd.append("Down")
                elif(resultado==3):
                    resultadoInd.append("Testing")
            j=j+1
            resultadoGrup.append(resultadoInd)

        return [dispositivosMonitorizados, estados, interfaces, resultadoGrup]

    def mostrarEstados(self,usuario):
        con=self.conectar()
        cursor = con.cursor()
        cursor.execute("select idUsuario from Usuario where usuario='" + usuario + "';")
        result = cursor.fetchone()
        idUsuario = str(result[0])
        cursor.execute("select * from Agente where idUsuario='" + idUsuario + "';")
        rows = cursor.fetchall()

        i=0
        for row in rows:
            t = Thread(target=getinfo, args=(row[1],int(row[2]),row[4],i,))
            t.start()
            i=i+1

        return i