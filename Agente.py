from Conexion import *
from threading import Thread
from hilos import *


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
        print(interfaces)
        resultadoGrup = []
        j=0
        for interface in interfaces:
            resultadoInd=[]
            for i in range(0,int(interface)-1):
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