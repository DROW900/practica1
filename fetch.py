import sys
import rrdtool
import time

def consultarInfo(documento):
    last_update = rrdtool.lastupdate(documento)
    # Grafica desde la última lectura menos cinco minutos
    tiempo_inicial = int(last_update['date'].timestamp())- 300
    result = rrdtool.fetch(documento, "-s,"+str(tiempo_inicial),"LAST")
    start, end, step = result[0]
    ds = result[1]
    rows = result[2]
    print(ds)
    return rows[0]
