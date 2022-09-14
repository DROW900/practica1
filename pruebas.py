from ast import Str
from pysnmp.hlapi import *
import json
import os
import random
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
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
    time.sleep(1)

def leerDispositivos():
    try:
        f = open("dispositivos.json", 'r')
        datos = json.load(f)
        f.close()
        return datos
    except:
        print("Aún no existen registros")
        time.sleep(1);
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
        time.sleep(1)
        return

def generarReporte():
    listarDispositivos();
    opt = int(input("Ingresa el dispositivo al que se realizará el reporte: "));
    if opt == 0:
        return
    print("Generando reporte para", datos[opt-1]['direccionIP'])
    informacionRequerida = obtenerInformacion(opt);
    infoSistema = informacionRequerida[0]
    infoInterfaces = informacionRequerida[1]
    manipularCanva(infoSistema,infoInterfaces)
    # Se genera el reporte del agente marcado
    print("Se ha generado el reporte correctamente C:")
    time.sleep(1)

def manipularCanva(infoSistema,infoInterfaces):
    w, h = A4
    rutaImagen = ""
    c = canvas.Canvas("Reporte.pdf", pagesize=A4)
    #Se empieza a generar el reporte
    if infoSistema[0] == "Linux":
        rutaImagen = "./Logos/Linux.jpg"
    else:
        rutaImagen = "./Logos/Windows.jpg"
    i = 50
    c.drawInlineImage(rutaImagen,300,h-200,150,150)
    c.drawString(50, h - i, "Sistema Operativo: "+infoSistema[0])
    i = i+20
    c.drawString(50, h - i, "Nombre Dispositivo: "+infoSistema[1])
    i = i+20
    c.drawString(50, h - i, "Contacto: "+infoSistema[2])
    i = i+20
    c.drawString(50, h - i, "Ubicación: "+infoSistema[3])
    i = i+40
    #Se empieza a imprimir la tabla de interfaces
    c.drawString(50, h - i, "Número de interfaces: "+infoSistema[4])
    i = i+20; 
    for interfaz,status in infoInterfaces.items():
        c.drawString(50, h - i, interfaz+": "+status)
        i = i+20
    c.showPage()
    c.save()

def obtenerInformacion(opt):
    comunidad = datos[opt-1]['nombreComunidad']
    direccionIP = datos[opt-1]['direccionIP']
    puerto = datos[opt-1]['puerto']
    arrayInfo = [];
    # Sistema Operativo
    arrayInfo.append(consultaSNMP(comunidad,direccionIP,puerto,'1.3.6.1.2.1.1.1.0'))
    # Nombre dispositivo
    arrayInfo.append(consultaSNMP(comunidad,direccionIP,puerto,'1.3.6.1.2.1.1.5.0'))
    # Contacto
    arrayInfo.append(consultaSNMP(comunidad,direccionIP,puerto,'1.3.6.1.2.1.1.4.0'))
    # Ubicación
    arrayInfo.append(consultaSNMP(comunidad,direccionIP,puerto,'1.3.6.1.2.1.1.6.0'))
    # Numero de interfaces
    arrayInfo.append(consultaSNMP(comunidad,direccionIP,puerto,'1.3.6.1.2.1.2.1.0'))
    numeroInterfaces = int(arrayInfo[4]);
    # Se genera un diccionario de las interfaces
    dictInterfaces = {}
    i = 1
    while i != numeroInterfaces+1:
        oid = '1.3.6.1.2.1.2.2.1.2.'+ str(i)
        nombreInterfaz = consultaSNMP(comunidad,direccionIP,puerto, oid)
        oid = '1.3.6.1.2.1.2.2.1.7.'+ str(i)
        estadoAministrativo = consultaSNMP(comunidad,direccionIP,puerto, oid)
        if estadoAministrativo == '1':
            dictInterfaces[nombreInterfaz] = "up"
        elif estadoAministrativo == '2':
            dictInterfaces[nombreInterfaz] = "down"
        else:
            dictInterfaces[nombreInterfaz] = "testing"
        i = i+1;
    return [arrayInfo,dictInterfaces]


## Generación del menú interactivo
while True:
    os.system("clear")
    datos = leerDispositivos();
    print("Sistema de Administración de Red")
    print("Practica 1 - Adquisición de Información")
    print("Carlos Eduardo Muñoz Carbajal    4CM13   2019630370\n")
    print("1. Agregar dispositivo")
    print("2. Eliminar dispositivo")
    print("3. Generar Reporte")
    print("0. Salir")

    opt = int(input("Ingresa la opción que desea realizar: "))
    match opt:
        case 1:
            agregarDispositivo();
        case 2:
            eliminarDispositivo();
        case 3:
            generarReporte();
        case 0:
            exit()