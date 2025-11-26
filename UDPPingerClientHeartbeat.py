import random
import time
from socket import *

serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

sequence_number = 0

while True:
    sequence_number += 1

    rand = random.randint(0, 9)

    if rand > 3:
        send_time = time.time()
        message = f"Heartbeat {sequence_number} {send_time}"

        clientSocket.sendto(message.encode(), (serverName, serverPort))
        print(f"heartbeat: seq={sequence_number}")

    else:
        print(f"falha simulada: seq={sequence_number}")

    time.sleep(1)