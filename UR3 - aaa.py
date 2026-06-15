import socket
import time
import os
import tkinter as tk
from tkinter import simpledialog

# Directori on està el script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

HOST = "10.10.73.235"
PORT = 30002

# Ruta absoluta als fitxers de la pinza
Abrir_pinza = os.path.join(BASE_DIR, 'pinza40UR3.py')
Cerrar_pinza = os.path.join(BASE_DIR, 'pinza10UR3.py')

# Función para enviar una trayectoria en espacio de configuraciones a la controladora del robot
def send_joint_path(path, sock):
    for joint_config in path:
        print(joint_config)
        sock.send(f"movej({joint_config}, a=0.5, v=0.5)".encode() + "\n".encode())
        time.sleep(5)

def demanar_numero_peça(num_peça):
    """
    Mostra un popup a l'ordinador demanant a l'usuari
    que introdueixi el número que hi ha a la peça.
    """
    root = tk.Tk()
    root.withdraw()  # Amaga la finestra principal
    root.attributes('-topmost', True)  # El popup apareix al davant

    while True:
        numero = simpledialog.askinteger(
            title=f"Peça {num_peça}",
            prompt=f"Introdueix el número que apareix a la peça {num_peça} (1-10):",
            minvalue=1,
            maxvalue=10,
            parent=root
        )
        if numero is not None:
            break
        # Si l'usuari tanca sense introduir res, torna a preguntar

    root.destroy()
    return numero

def executar_trajectoria_segons_numero(numero, sock):
    """
    Decideix si fer figura geomètrica (parell) o cercle (imparell).
    """
    if numero % 2 == 0:
        print(f"Número {numero} és PARELL → traçar figura de {numero} costats")
        trajectoria_figura(numero, sock)
    else:
        print(f"Número {numero} és IMPARELL → traçar cercle de radi 5cm")
        trajectoria_cercle(sock)

def trajectoria_figura(numero, sock):
    if numero == 4:
        pathfi = [
            [-1.447159069008518, -1.644827512423482, -1.029983530194813, -0.422696837116301, 1.497014895096205, -0.003751004440434],
            [-0.750209626968530, -1.559133993122124, -1.114111288401728, -0.407425412001099, 0.801139545964185, -0.042927069636849],
            [-0.749864037289718, -1.492170235509374, -1.900465869774991, 0.311923057288943, 0.800766117832470, -0.042911034670523],
            [-1.531840882582348, -1.833199330538566, -1.526216522656946, 0.261696440246406, 1.581601575967733, -0.000024425011782]
        ]
    #fariem així la lògica per cada número de costats
    send_joint_path(pathfi, sock)

def trajectoria_cercle(sock):
    pathce = [
        [-1.3439, -1.7639, -1.6111, 0.2778, 1.3942, -0.0083],
        [-1.376978697180495, -1.750324877800567, -1.491278336083367, 0.144396081301672, 1.426890386974375, -0.006868354239356],
        [-1.473840497442741, -1.588156253720471, -1.676813504219662, -1.712106948976187, -1.680059834440030, -1.591847597637490],
        [-1.476590488238460, -1.380993842707228, -1.784432808982249, -1.841792225666028, -1.900989727917503, -1.943390078961099],
        [-1.951058551970837, -1.926919510392384, -1.874128981070844, -1.810552918387921, -1.363490521706814, -1.291325993306792],
        [-1.295336629794801, -1.371290190812044, -1.503808959768055, -1.630196029712716, -1.705203169258265, -1.699197142481426],
        [0.050260300391290,	0.035547655242173,	0.099053063463610,	0.217488374660494,	0.357528780591051,	0.459350468250539],
        [0.481543185962293,	0.412484197983743, 1.523686113736687,	1.637800214449172,	1.726361743462532, 1.761941715482429],	
        [1.729973385066500,	1.641854511444696,	1.526670955298846,	1.431237754761403, -0.002570053034741,	0.002453082790021],
        [0.006372783672006,	0.007930590033175,	0.006508669348003,	0.002603549936901,	-0.002442098076153,	-0.006682887455199],
        [-1.3439, -1.7639, -1.6111, 0.2778, 1.3942, -0.0083],
    ]


    send_joint_path(pathce, sock)

# Conexión via socket a la controladora del robot
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

#del punt inicial a peça 1:
path1 = [
    [-1.549903784776632, -2.402424196525162, -0.692281316038875, -1.168784829907094, 1.506710483293595, -1.588144527056243]
]
#obrir pinça
with open(Abrir_pinza, 'rb') as f: sock.sendall(f.read())
time.sleep(0.5)
send_joint_path(path1, sock)
#tancar pinça per agafar la peça
with open(Cerrar_pinza, 'rb') as f: sock.sendall(f.read())
time.sleep(0.5)
#portar la pinça a pose de veure
path2 = [
    [-1.536190666208854, -1.838383707321720, -1.516713187670425, 0.257253453726341, 1.586366795230875, 0.000167832330602]
]
send_joint_path(path2, sock)
time.sleep(3)
#demanar el num
numero1 = demanar_numero_peça(1)
executar_trajectoria_segons_numero(numero1, sock)
time.sleep(3)
#cami per deixar la peça
path3 = [
    [0.977050757309872, 0.019384889979691, -1.393239027887752, -0.200063498178355, -1.566743309728070, -2.199230332767112]
]
send_joint_path(path3, sock)
time.sleep(3)
with open(Abrir_pinza, 'rb') as f: sock.sendall(f.read())
#deixar peça1

#PEÇA 2!!
#cami per la peça 2:
path4 = [
    [0.948887098850669, 0.649039416818432, -1.652845787589351, -1.353878144853722, -1.198980805940714, -1.995537859419820]
]
#potser aquest open s'ha de treure
with open(Abrir_pinza, 'rb') as f: sock.sendall(f.read())
send_joint_path(path4, sock)
time.sleep(3)
#tancar pinça per agafar la peça
with open(Cerrar_pinza, 'rb') as f: sock.sendall(f.read())
time.sleep(0.5)
#portar la pinça a pose de veure
path5 = [
   [0.698302799420510, -0.720760929805960, -0.473945419259977, 1.121819731848477, 0.649761953908455, -3.084020301024214]
]
send_joint_path(path5, sock)
time.sleep(3)
numero2 = demanar_numero_peça(2)
executar_trajectoria_segons_numero(numero2, sock)
time.sleep(3)

#deixar peça 2:
path6 = [
    [0.114421201764704, 0.220380013972548, -1.921140832133033, 0.760980144024705, -0.768913199707674, 2.426836956989657]
]
send_joint_path(path6, sock)
with open(Abrir_pinza, 'rb') as f: sock.sendall(f.read())
time.sleep(3)
# Mensaje que se imprime cuando se finaliza la ejecución
# de la trayectoria
print("Trayectoria finalizada")


data = sock.recv(1024)

# Se cierra la conexión
sock.close()
