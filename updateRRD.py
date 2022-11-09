import time
import rrdtool
import threading
from getSNMP import consultaSNMP

def actualizarRRD(comunidad, ip, documento):
    while 1:
        paquetesUnicast = int(
            consultaSNMP(comunidad,ip,
                        '1.3.6.1.2.1.2.2.1.11.2'))
        paquetesIPV4 = int(
            consultaSNMP(comunidad,ip,
                        '1.3.6.1.2.1.4.3.0'))
        mensajesECHO = int(
            consultaSNMP(comunidad,ip,
                        '1.3.6.1.2.1.5.21.0'))
        segmentosRec = int(
            consultaSNMP(comunidad,ip,
                        '1.3.6.1.2.1.6.10.0'))
        datagramasEnt = int(
            consultaSNMP(comunidad,ip,
                        '1.3.6.1.2.1.7.1.0'))
        valor = "N:" + str(paquetesUnicast) + ':' + str(paquetesIPV4) + ':' + str(mensajesECHO) + ':' + str(segmentosRec) + ':' + str(datagramasEnt)
        rrdtool.update(documento, valor)
        rrdtool.dump(documento,documento+'.xml')
        time.sleep(1)

    if ret:
        print (rrdtool.error())
        time.sleep(300)