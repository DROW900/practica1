#!/usr/bin/env python
import rrdtool
def generarRRD(nombre):
    ret = rrdtool.create(str(nombre),
                        "--start",'N',
                        "--step",'300',
                        "DS:paquetesUnicast:COUNTER:120:U:U",
                        "DS:paquetesIPV4:COUNTER:120:U:U",
                        "DS:mensajesECHO:COUNTER:120:U:U",
                        "DS:segmentosRecibidos:COUNTER:120:U:U",
                        "DS:datagramasUDP:COUNTER:120:U:U",
                        "RRA:AVERAGE:0.5:1:100",
                        "RRA:AVERAGE:0.5:1:100",
                        "RRA:AVERAGE:0.5:1:100",
                        "RRA:AVERAGE:0.5:1:100",
                        "RRA:AVERAGE:0.5:1:100")

    if ret:
        print (rrdtool.error())