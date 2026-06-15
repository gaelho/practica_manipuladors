import socket
import time
import os
import tkinter as tk
from tkinter import simpledialog

# Directori on està el script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

HOST = "10.10.73.237"
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
            [0.801543547295243, 2.402889494999508, -6.283185307179586, -2.276534995467506, 0.727291233728021, 9.332902521177749],
            [0.513718155212967, 2.347190882252864, -6.283185307179586, -2.166103243370312, 0.447747756356090, 9.263487453899575],
            [0.457691016705029,2.419400659624597, -6.283185307179587, -2.173254033639796, 0.383067809491607, 9.199145331382191],
            [0.727236100191636, 2.464730230546249, -6.283185307179586, -2.305839915383183, 0.642960977349559, 9.300983935986070]
        ]
    #fariem així la lògica per cada número de costats
    send_joint_path(pathfi, sock)

def trajectoria_cercle(sock):
    pathce = [
        [0.539453774113416, 2.735042281471561, 2.346408705890656, 3.113547756672048, 0.926208358602099, 1.763438655663339],
        [0.499614799720631, 2.866382320599393, 2.260838341727565, 3.095628252932583, 0.940097893782770, 1.716828902834266],
        [0.404104072572027, 2.925377317988377, 2.202236822430637, -3.126286183613610, 0.977255384974400, 1.609425764853362],
        [0.278358439119530, 2.882763032985934, 2.186809670893457, -2.996921529359294, 1.033902019181807, 1.476411187266148],
        [0.177874169715628, 2.763219480519446, 2.214676670955793, -2.856444654078596, 1.084369885982451, 1.376788499034408],
        [0.138416266003810, 2.601093367465173, 2.270602946121863, -2.733033560767174, 1.105372002383873, 1.339165273873148],
        [0.176012832216108, 2.449658884978788, 2.340558992819163, -2.668019003205098, 1.085481773345858, 1.375015844161997],
        [0.273539673305732, 2.363415502180573, 2.401486508927059, -2.689721436430377, 1.036462470970346, 1.471443840768689],
        [0.398054995096227, 2.399355147014992, 2.434978382186484, -2.829225909971137, 0.980026642833711, 1.602713543632931],
        [0.496594193980558, 2.547131325460457, 2.413558388531871, -3.019079140492286, 0.941375661953349, 1.713378855704393]
    ]


    send_joint_path(pathce, sock)

# Conexión via socket a la controladora del robot
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

#del punt inicial a peça 1:
path1 = [
    [-0.039712931799921, 1.891347754883363, 1.212969060686791, -1.123340636201485, 1.570980735006774, -0.038821334557614]
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
    [-0.109006060650880, -0.139159698085471, -1.902691127132571, -1.398040611782887, 0.166741902885645, 0.295306936710737]
]
send_joint_path(path2, sock)
time.sleep(3)
#demanar el num
numero1 = demanar_numero_peça(1)
executar_trajectoria_segons_numero(numero1, sock)
time.sleep(3)
#cami per deixar la peça
path3 = [
    [1.813192579465399, 1.070305522327075, -6.283185307179589, -3.091355857864719, -0.432041317739394, 11.532336295633016]
]
send_joint_path(path3, sock)
time.sleep(3)
with open(Abrir_pinza, 'rb') as f: sock.sendall(f.read())
#deixar peça1

#PEÇA 2!!
#cami per la peça 2:
path4 = [
    [2.304272181394191, 1.467717672392168, -7.327142959703847, -2.507390016142736, -1.113305199443041, 11.777583651324958]
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
   [-0.109794366955809, 4.474781079484104, -11.538457105003333, 0.483934074169329, -0.167427476297211, 9.718335609979469]
]
send_joint_path(path5, sock)
time.sleep(3)
numero2 = demanar_numero_peça(2)
executar_trajectoria_segons_numero(numero2, sock)
time.sleep(3)

# Mensaje que se imprime cuando se finaliza la ejecución
# de la trayectoria
print("Trayectoria finalizada")


data = sock.recv(1024)

# Se cierra la conexión
sock.close()

