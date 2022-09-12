import json
import os
import random
import time
from reportlab.pdfgen import canvas
datos = []

def consultaSNMP(comunidad,host,puerto,oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad),
               UdpTransportTarget((host, int(puerto))),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            varB=(' = '.join([x.prettyPrint() for x in varBind]))
            resultado= varB.split()[2]
    return resultado

## Se obtienen los datos, se almacena en el arreglo de JSON y se agregan al archivo
def agregarDispositivo():
    direccionIP = input("Dirección IP: ")
    versionSNMP = input("Versión SNMP: ")
    nombreComunidad = input("Nombre de la comunidad: ")
    puerto = input("Puerto: ")
    dispositivo = {
        'direccionIP': direccionIP,
        'versionSNMP': versionSNMP,
        'nombreComunidad': nombreComunidad,
        'puerto': puerto
    }
    datos.append(dispositivo);
    guardarEnArchivo("Se ha realizado el registro correctamente :D")

def guardarEnArchivo(mensaje):
    f = open("dispositivos.json", 'w')
    json.dump(datos, f)
    f.close()
    print(mensaje)
    time.sleep(2)

def leerDispositivos():
    try:
        f = open("dispositivos.json", 'r')
        datos = json.load(f)
        f.close()
        return datos
    except:
        print("Aún no existen registros")
        time.sleep(2);
        os.system("clear")
        return [];

def listarDispositivos():
    os.system("clear")
    contador = 1;
    print("Dispositivos registrados: ")
    for dispositivo in datos:
        print(str(contador)+".", dispositivo)
        contador += 1;
    print("0. Cancelar")

## Se hace la eliminación del elemento en el arreglo y se lleva al archivo
def eliminarDispositivo():
    listarDispositivos()
    opt = int(input("Ingresa el dispositivo a eliminar: "));
    if opt == 0:
        return
    else:
        opt = opt - 1;
        datos.pop(opt)
        guardarEnArchivo("Se ha eliminado el elemento :D")
        time.sleep(2)
        return

def generarReporte():
    listarDispositivos();
    opt = int(input("Ingresa el dispositivo al que se realizará el reporte: "));
    if opt == 0:
        return
    print("Generando reporte para", datos[opt-1]['direccionIP'])
    numero = random.randint(1,100);
    nombre = "reporte"+str(numero)+".pdf"
    c = canvas.Canvas(nombre);
    c.drawCentredString(0,0,"Reporte")
    c.save()

## Generación del menú interactivo
while True:
    os.system("clear")
    datos = leerDispositivos();
    print("Sistema de Administración de Red")
    print("Practica 1 - Adquisición de Información")
    print("Carlos Eduardo Muñoz Carbajal    4CM13   201963070\n")
    print("1. Agregar dispositivo")
    print("2. Eliminar dispositivo")
    print("3. Generar Reporte")
    print("0. Salir")

    opt = int(input("Ingresa la opción que desea realizar "))
    match opt:
        case 1:
            agregarDispositivo();
        case 2:
            eliminarDispositivo();
        case 3:
            generarReporte();
        case 0:
            exit()