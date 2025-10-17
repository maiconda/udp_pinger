import time
from socket import *

serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
num_heartbeats = 10

for sequence_number in range(1, num_heartbeats + 1):
    send_time = time.time()
    message = f"Heartbeat {sequence_number} {send_time}"
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    print(f"Heartbeat enviado: seq={sequence_number}")
    time.sleep(1)

clientSocket.close()
