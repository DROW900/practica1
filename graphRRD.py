import rrdtool
import time
def generarGrafica(documento, nombreGrafica, datos, titulo, fechaInicial, fechaFinal):
    print("Generando grafica")
    time.sleep(2);
    tiempo_actual = int(time.time())
    #Grafica desde el tiempo actual menos diez minutos
    tiempo_inicial = tiempo_actual - 1800

    ret = rrdtool.graphv( nombreGrafica,
                        "--start",str(fechaInicial),
                        "--end",str(fechaFinal),
                        "--vertical-label=Segmentos",
                        "--title="+titulo+"",
                        "DEF:sEntrada="+ documento +":"+ datos +":AVERAGE",
                        "AREA:sEntrada#FF0000:"+titulo+"")
    print(ret)