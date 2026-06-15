import socket
import time
import os
import tkinter as tk
from tkinter import simpledialog

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

HOST = "10.10.73.235"
PORT = 30002

def abrir_pinza(sock):
    sock.send(b"def abrir():\n  RG2(40,40,0.0,True,False,False)\nend\nabrir()\n")
    time.sleep(3)

def cerrar_pinza(sock):
    sock.send(b"def cerrar():\n  RG2(10,40,0.0,True,False,False)\nend\ncerrar()\n")
    time.sleep(3)

def send_joint_path(path, sock, sleep=5):
    for joint_config in path:
        print(joint_config)
        sock.send(f"movej({joint_config}, a=0.5, v=0.5)".encode() + "\n".encode())
        time.sleep(sleep)

def demanar_numero_peça(num_peça):
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

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

    root.destroy()
    return numero

def executar_trajectoria_segons_numero(numero, sock):
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
    send_joint_path(pathfi, sock)

def trajectoria_cercle(sock):
    pathce = [
        [-1.531430107559169, -1.810901134352920, -1.319902215954799, 0.033158476075029, 1.581158240648813, -0.000041827617792],
        [-1.531778822951940, -1.840832644068301, -1.044303530630978, -0.212493439820732, 1.581541424493357, -0.000026015093811],
        [-1.638490671114252, -1.896889226623446, -1.015024894313484, -0.185418191173208, 1.688120744526584, 0.004686849070219],
        [-1.704181914265098, -1.931421649640293, -1.080080041369062, -0.085713440285176, 1.754062406780974, 0.007582010271134],
        [-1.704289606025138, -1.923656531063257, -1.236761303273844, 0.063233670781097, 1.754182937819261, 0.007592631471314],
        [-1.641547657826000, -1.889738975762411, -1.401697621463651, 0.193849068095608, 1.691495902928991, 0.004791523920664],
        [-1.535183093921125, -1.838141149634386, -1.516186875963057, 0.256426002785472, 1.585246520690867, 0.000121220880062],
        [-1.424209724053465, -1.782802161973231, -1.541581228977733, 0.226718552411671, 1.474420815912012, -0.004741247292902],
        [-1.351336482316479, -1.740765304625891, -1.480242814494501, 0.124138689571193, 1.401478663321045, -0.008047933034657],
        [-1.349297319182367, -1.738792608100417, -1.336077863369068, -0.022123043860270, 1.399241967459963, -0.008118116829843],
        [-1.419928316981547, -1.777896003626084, -1.170531609283958, -0.148981383605429, 1.469802817187430, -0.004956734066689],
        [-1.531778822951940, -1.840832644068301, -1.044303530630978, -0.212493439820732, 1.581541424493357, -0.000026015093811]
    ]
    send_joint_path(pathce, sock, sleep=0.5)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# PEÇA 1
path1 = [
    [-1.549903784776632, -2.402424196525162, -0.692281316038875, -1.168784829907094, 1.506710483293595, -1.588144527056243]
]
abrir_pinza(sock)
send_joint_path(path1, sock)
cerrar_pinza(sock)

path2 = [
    [-1.536190666208854, -1.838383707321720, -1.516713187670425, 0.257253453726341, 1.586366795230875, 0.000167832330602]
]
send_joint_path(path2, sock)
time.sleep(3)

numero1 = demanar_numero_peça(1)
executar_trajectoria_segons_numero(numero1, sock)
time.sleep(3)

path3 = [
    [0.977050757309872, 0.019384889979691, -1.393239027887752, -0.200063498178355, -1.566743309728070, -2.199230332767112]
]
send_joint_path(path3, sock)
abrir_pinza(sock)

# PEÇA 2
path4 = [
    [0.948887098850669, 0.649039416818432, -1.652845787589351, -1.353878144853722, -1.198980805940714, -1.995537859419820]
]
send_joint_path(path4, sock)
cerrar_pinza(sock)

path5 = [
    [0.698302799420510, -0.720760929805960, -0.473945419259977, 1.121819731848477, 0.649761953908455, -3.084020301024214]
]
send_joint_path(path5, sock)
time.sleep(3)

numero2 = demanar_numero_peça(2)
executar_trajectoria_segons_numero(numero2, sock)
time.sleep(3)

path6 = [
    [-2.146053541389191, -1.858554830129618, -2.173926284372349, -0.198078353693901, 2.455453599893539, -2.468390117922107]
]
send_joint_path(path6, sock)
abrir_pinza(sock)

print("Trayectoria finalizada")

data = sock.recv(1024)
sock.close()
