import sys
import rrdtool
import time
tiempo_actual = int(time.time())
#Grafica desde el tiempo actual menos diez minutos
tiempo_inicial = tiempo_actual - 1800

ret = rrdtool.graphv( "segmentosTCP.png",
                     "--start",str(tiempo_inicial),
                     "--end","N",
                     "--vertical-label=Segmentos",
                     "--title=Segmentos TCP de un agente \n Usando SNMP y RRDtools",
                     "DEF:sEntrada=192.168.0.17.rrd:paquetesUnicast:AVERAGE",
                     "LINE3:sEntrada#FF0000:Segmentros recibidos")
print(ret)