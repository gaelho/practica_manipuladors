import socket
import time
import os
import tkinter as tk
from tkinter import simpledialog

# Dirección IP del robot UR
HOST = "10.10.73.236"

# Puerto del servidor en el robot
PORT = 30002

# Scripts para abrir y cerrar la pinza
Abrir_pinza = 'pinza40UR3.py'
Cerrar_pinza = 'pinza10UR3.py'

# Función para enviar una trayectoria en espacio de configuraciones a la controladora del robot
def send_joint_path(path, sock):
    for joint_config in path:
        print(joint_config)
        sock.send(f"movej({joint_config}, a=0.5, v=0.5)".encode() + "\n".encode())
        time.sleep(3)

# Conexión via socket a la controladora del robot
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

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
    if numero % 2 == 0:
        print(f"Número {numero} parell: figura de {numero} costats")
        trajectoria_figura(numero, sock)
    else:
        print(f"Número {numero} imparell: cercle de radi 5cm")
        trajectoria_cercle(sock)

def trajectoria_figura(numero, sock):
    if numero == 4:
        pathfi = [
            [-2.311630985878277, -1.815265800052897, -1.405138624188302, 0.010095904538356, 2.360697087552706, -0.047957468022975],
            [-2.314044362932033, -2.064882474173553, -1.818856555289150, 0.672866814189677, 2.363440015298567, -0.048483008194692],
            [-1.591008510574735, -1.535165507654675, -2.558072869161473, 0.903093490858411, 1.641672945535685, -0.002533977215791],
            [-1.589179651086175, -1.154735749110471, -2.001775433558062, -0.033547375790686, 1.639775607968391, -0.002439577784648],
        ]
    #fariem així la lògica per cada número de costats
    send_joint_path(pathfi, sock)

def trajectoria_cercle(sock):
    pathce = [
        [-1.042927564461636, -0.873964692305305, -2.111329324253208, -0.210865405016873, 1.094306771676160, 0.025955703376278],
        [-1.145400738570315, -0.942068855648443, -1.951218249210320, -0.300444748258736, 1.196082444775712, 0.019982371850360],
        [-1.433534414297655, -1.092947795208598, -1.806022721998286, -0.291320254129975, 1.483817309952061, 0.005116363047184],
        [-1.701534072252841, -1.237933065594867, -1.727948748344112, -0.225013986840275, 1.751598172972550, -0.007985233640846],
        [-1.866348251930575, -1.339985585460217, -1.744453281099052, -0.108696526777919, 1.916182824651321, -0.016577226980270],
        [-1.921985911058832, -1.385569646275058, -1.845849305811181, 0.036999511379490, 1.971824970567786, -0.019749545207282],
        [-1.875796721164735, -1.368390795154075, -1.998215205385559, 0.173130677931312, 1.926162544933151, -0.017156648798982],
        [-1.711612696971345, -1.268227349335796, -2.159135852478318, 0.236393388997111, 1.762130088295108, -0.008490528423499],
        [-1.451452947105093, -1.097949460190047, -2.253837337618060, 0.161615948926915, 1.502287161868615, 0.004235511541632],	
        [-1.172918512598000, -0.928453013020922, -2.234117443662226, -0.030564825373506, 1.224110140126982, 0.018435189592280],
        [-1.042927564461636, -0.873964692305305, -2.111329324253208, -0.210865405016873, 1.094306771676160, 0.025955703376278],
    ]


    send_joint_path(pathce, sock)


#del punt inicial a peça 1:
path1 = [
    [-1.969447219150332, -1.843566091636810, -1.391924761531454, -1.388944567259390, 1.602815619552640, -0.440657074568116],
]
send_joint_path(path1, sock)
time.sleep(3) #no fa falta ja que ja n'hi ha un a la funcio pero per si de cas encara a depurar
#tancar pinça per agafar la peça
with open(Cerrar_pinza, 'rb') as f: sock.sendall(f.read())
time.sleep(0.5)
#portar la pinça a pose de veure
path2 = [
    [-1.590901544553329, -1.155897401140183, -1.999424256268729, -0.034878027414740, 1.641562768416003, -0.002532688713940],
]
send_joint_path(path2, sock)
time.sleep(3) #no fa falta ja que ja n'hi ha un a la funcio pero per si de cas encara a depurar
#demanar el num
numero1 = demanar_numero_peça(1)
executar_trajectoria_segons_numero(numero1, sock)
time.sleep(3)
#cami per deixar la peça
path3 = [
    [-1.628273618395326, -1.606280113421929, -2.097509272358570, -0.609014954430093, 1.616160590659280, 0.006271943607753],
]
send_joint_path(path3, sock)
time.sleep(3) #no fa falta ja que ja n'hi ha un a la funcio pero per si de cas encara a depurar
with open(Abrir_pinza, 'rb') as f: sock.sendall(f.read())
time.sleep(3)
#deixar peça1

#PEÇA 2!!
#cami per la peça 2:
path4 = [
    [-1.659240440780025, -1.587049583665279, -1.292328159294717, -1.775914870559414, 1.511609984778052, -0.110286149815122],
    [-1.965444799574059, -1.927825101466137, -1.271403092609259, -1.478571213891143, 1.602537640816021, -0.441625689058345],
    [-1.966637856440213, -1.951677834346193, -1.395027083217823, -1.331589089778734, 1.602707079007652, -0.442845459026799],
]
#potser aquest open s'ha de treure
with open(Abrir_pinza, 'rb') as f: sock.sendall(f.read())
time.sleep(2)
send_joint_path(path4, sock)
time.sleep(3)#no fa falta ja que ja n'hi ha un a la funcio pero per si de cas encara a depurar
#tancar pinça per agafar la peça
with open(Cerrar_pinza, 'rb') as f: sock.sendall(f.read())
time.sleep(2)
#portar la pinça a pose de veure
path5 = [
   [-1.590720974646908, -1.155773024628555, -1.999494393934870, -0.034931901486521, 1.641375277741080, -0.002523869229181],
]
send_joint_path(path5, sock)
time.sleep(2)#no fa falta ja que ja n'hi ha un a la funcio pero per si de cas encara a depurar
numero2 = demanar_numero_peça(2)
executar_trajectoria_segons_numero(numero2, sock)
time.sleep(2)

#deixar peça 2:
path6 = [
    [-1.628540711633691, -1.478693500621700, -1.789310584202126, -1.044797432139317, 1.616289471052616, 0.006020620373456],
]
send_joint_path(path6, sock)
time.sleep(2) #no fa falta ja que ja n'hi ha un a la funcio pero per si de cas encara a depurar
with open(Abrir_pinza, 'rb') as f: sock.sendall(f.read())
time.sleep(3) 
# Mensaje que se imprime cuando se finaliza la ejecución
# de la trayectoria
print("Trayectoria finalizada")


data = sock.recv(1024)

# Se cierra la conexión
sock.close()
