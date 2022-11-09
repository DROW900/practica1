import rrdtool
import time
def generarGrafica(documento, nombreGrafica, datos):
    tiempo_actual = int(time.time())
    #Grafica desde el tiempo actual menos diez minutos
    tiempo_inicial = tiempo_actual - 1800

    ret = rrdtool.graphv( nombreGrafica,
                        "--start",str(tiempo_inicial),
                        "--end","N",
                        "--vertical-label=Segmentos",
                        "--title=Segmentos TCP de un agente \n Usando SNMP y RRDtools",
                        "DEF:sEntrada="+ documento +":"+ datos +":AVERAGE",
                        "LINE3:sEntrada#FF0000:Segmentros recibidos")
    print(ret)