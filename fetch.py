import sys
import rrdtool
import time

last_update = rrdtool.lastupdate("192.168.0.17.rrd")
# Grafica desde la última lectura menos cinco minutos
print(last_update)
tiempo_inicial = int(last_update['date'].timestamp())- 300
print(tiempo_inicial)
result = rrdtool.fetch("192.168.0.17.rrd", "-s,"+str(tiempo_inicial),"LAST")
start, end, step = result[0]
ds = result[1]
rows = result[2]
print(result)
print (ds)
print (rows)
