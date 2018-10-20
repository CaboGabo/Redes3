from easysnmp import Session
from estadoDispositivo import *
from Consultadispositivo import tiempoUltimoReinicio
import time

# Estado de interfaces de red 1 up 2 down 3 testing
session = Session(hostname='localhost', community='MacCommunity', version=2)
description = str(session.get('1.3.6.1.2.1.6.10.0'))
inicio = description.index("=")
sub = description[inicio+2:]
fin = sub.index("'")

print(sub[:fin])


print(monitoreosSNMP[0][1])


"""""

from easysnmp import Session

# Nombre de la pc

description = str(session.get('.1.3.6.1.2.1.1.5.0'))
inicio = description.index("=")
sub = description[inicio+2:]
fin = sub.index("'")

print(sub[:fin])


#Direccion ip

session = Session(hostname='localhost', community='MacCommunity', version=2)
description = str(session.walk('1.3.6.1.2.1.4.20.1.1'))
inicio = description.index("=")
sub = description[inicio+2:]
fin = sub.index("'")

print(sub[:fin])



# Estado de interfaces de red 1 up 2 down 3 testing
session = Session(hostname='localhost', community='MacCommunity', version=2)
description = str(session.walk('1.3.6.1.2.1.2.2.1.8'))


print(description)



# No interfaces de red
session = Session(hostname='localhost', community='MacCommunity', version=2)
description = str(session.get('1.3.6.1.2.1.2.1.0'))


print(description)

"""