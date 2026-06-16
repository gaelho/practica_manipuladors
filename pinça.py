import socket
import time

# Dirección IP del robot UR
HOST = "10.10.73.23X"

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
        time.sleep(10)

# Conexión via socket a la controladora del robot
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Trayectoria -- configuraciones (variables articulares, en radianes)
path = [
     [-1.447159069008518, -1.644827512423482, -1.029983530194813, -0.422696837116301, 1.497014895096205 -0.003751004440434],
    # Añadir más si hiciera falta
]
path2 = [
      [-0.750209626968530, -1.559133993122124, -1.114111288401728, -0.407425412001099, 0.801139545964185, -0.042927069636849],
    # Añadir más si hiciera falta
]
# Se envia la trayectoria a la controladora del robot
send_joint_path(path, sock)
# Enviar archivo script abrir pinza
with open(Cerrar_pinza, 'rb') as f: sock.sendall(f.read())
time.sleep(3)
# Se envia la trayectoria a la controladora del robot
send_joint_path(path2, sock)
# Enviar archivo script cerrar pinza
with open(Abrir_pinza, 'rb') as f: sock.sendall(f.read())
time.sleep(3)

# Mensaje que se imprime cuando se finaliza la ejecución
# de la trayectoria
print("Trayectoria finalizada")

data = sock.recv(1024)

# Se cierra la conexión
sock.close()
