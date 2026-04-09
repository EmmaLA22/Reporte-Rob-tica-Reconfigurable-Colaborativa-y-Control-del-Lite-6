#!/usr/bin/env python3

import os
import sys
import time
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from xarm.wrapper import XArmAPI

#######################################################
# Obtener IP
if len(sys.argv) >= 2:
    ip = sys.argv[1]
else:
    try:
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read('../robot.conf')
        ip = parser.get('xArm', 'ip')
    except:
        ip = input('Please input the xArm ip address:')
        if not ip:
            print('input error, exit')
            sys.exit(1)
########################################################

# Inicializar robot
arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

# ------------------ RUTA BASE ------------------
base_path = r"C:\Users\Emmanuel LechArr\xArm-Python-SDK\example\wrapper\common"

# ------------------ ARCHIVOS ------------------
dibujos = [
    os.path.join(base_path, "dibujo_negro_0001.ngc"),
    os.path.join(base_path, "dibujo_gris_0001.ngc"),
    os.path.join(base_path, "dibujo_rojo_0001.ngc")
]

# POSICIÓN INICIAL
def posicion_inicial():
    arm.set_position(x=74, y=311, z=180, roll=-180, pitch=0, yaw=130, speed=100, wait=True)
    print(arm.get_position(), arm.get_position(is_radian=True))

# Espera inicial
print("Presiona 'a' para comenzar el primer dibujo...")
x = ''
while x != 'a':
    x = input()

# Ejecutar dibujos
for idx, archivo in enumerate(dibujos):

    print(f"\n--- Iniciando dibujo {idx+1} ---")
    print(f"Archivo: {archivo}")

    # Validar archivo
    if not os.path.exists(archivo):
        print(f"ERROR: No se encontró el archivo {archivo}")
        continue

    # Ir a posición inicial
    posicion_inicial()

    # Contar líneas
    with open(archivo, 'r') as fp:
        lines = sum(1 for line in fp)
    print('Total Number of lines:', lines)

    start_time = time.time()

    cont = 0

    # -------------------------------
    # 🔧 CALIBRACIÓN DE ALTURA
    # -------------------------------
    print("Ajusta altura con 'a'. Presiona 'q' para guardar y continuar...")
    x = ''
    while x != "q":
        if x == "a":
            # Baja poco a poco desde la posición inicial
            pos_actual = arm.get_position()[1]
            arm.set_position(
                x=pos_actual[0],
                y=pos_actual[1],
                z=pos_actual[2] - 1,
                roll=-180,
                pitch=0,
                yaw=130,
                speed=100,
                wait=True
            )
        x = input()

    # GUARDAR BASE REAL DESPUÉS DE CALIBRAR
    pos_actual = arm.get_position()[1]

    base_x = pos_actual[0]
    base_y = pos_actual[1]
    base_z = pos_actual[2]

    print(f"Base calibrada: X={base_x}, Y={base_y}, Z={base_z}")

    # -------------------------------
    #  LEER G-CODE Y DIBUJAR
    # -------------------------------
    with open(archivo) as gcode:
        for line in gcode:
            line = line.strip()
            coord = re.findall(r'[XY].?\d+.\d+', line)

            if coord:
                xx = float(coord[0].split('X')[1])
                yy = float(coord[1].split('Y')[1])

                # Ajuste de altura dinámico
                if yy > 150:
                    z_offset = 0
                elif yy > 50:
                    z_offset = -1
                else:
                    z_offset = -2

                arm.set_position(
                    x=base_x - xx,
                    y=base_y - yy,
                    z=base_z + z_offset,  
                    roll=-180,
                    pitch=0,
                    yaw=130,
                    speed=100,
                    wait=True
                )

                cont += 1

                if cont % 100 == 0:
                    print(f"{cont} lines. Lines to finish {lines - cont}\r")

    print(f"--- {time.time() - start_time} seconds ---")

    # Regresar a posición inicial
    posicion_inicial()

    # Esperar siguiente dibujo
    if idx < len(dibujos) - 1:
        print("\nPresiona 'a' para continuar al siguiente dibujo...")
        x = ''
        while x != 'a':
            x = input()

# Final
print("Todos los dibujos completados")
arm.move_gohome(wait=True)
arm.disconnect()