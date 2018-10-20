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
        #print(hostname)
        #print(comunidad)
        #print(version)
        #print(ip)
        #print(nombre)
        #print(sistemaop)
        #print(interfaces)
        #print(tiempo)
        #print(ubicacion)
        #print(contacto)
        #print(porCPU)
        #print(porRAM)
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
            host = hostname[i]
            v = int(version[i])
            com = comunidad[i]
            respuesta = nombreDis(host,com,v)
            if(respuesta=='Timeout Error'):
                estados.append("Down")
                interfaces.append("0")
            else:
                estados.append("Up")
                respuesta = noInterfacesRed(host,com,v)
                interfaces.append(respuesta)
            i+=1
        resultadoGrup = []
        j=0
        for interface in interfaces:
            resultadoInd=[]
            for i in range(0,int(interface)):
                resultado = int(estatusInterfaces(hostname[j],comunidad[j],version[j],i+1))
                if(resultado==1):
                    resultadoInd.append("Up")
                elif(resultado==2):
                    resultadoInd.append("Down")
                elif(resultado==3):
                    resultadoInd.append("Testing")
                else:
                    resultadoInd.append("Unknown")
            j+=1
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