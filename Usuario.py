from Conexion import *

class Usuario(Conexion):
    def insertar(self, usr, passw):
        con = self.conectar()
        cursor = con.cursor()
        cursor.execute("insert into Usuario values(null,'"+usr+"','"+passw+"');")
        con.commit()
        self.cerrar(con)

    def login(self, usr, passw):
        con = self.conectar()
        cursor = con.cursor()
        cursor.execute("select pass from Usuario where usuario='"+usr+"';")
        result = cursor.fetchone()
        if(result is not None):
            if(passw == result[0]):
                self.cerrar(con)
                return True
            else:
                self.cerrar(con)
                return False
        else:
            self.cerrar(con)
            return False