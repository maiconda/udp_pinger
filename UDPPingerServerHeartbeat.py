import time
from socket import *

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', 12000))

# se ficar mais de 1.5 sem receber nada, gera uma exception (faz sentido no localhost)
serverSocket.settimeout(1.5)

strikes = 0  # falhas consecutivas
MAX_STRIKES = 3  # numero de falhas para acusar um erro critico

while True:
    try:
        # mensagem recebida
        message, address = serverSocket.recvfrom(1024)

        # ao receber zera strikes
        if strikes > 0:
            print(f"[{time.strftime('%H:%M:%S')}] cliente recuperado")
        strikes = 0

        recv_time = time.time()
        decoded = message.decode()

        print(f"[{time.strftime('%H:%M:%S')}] Mensagem: {decoded}")

    except timeout:
        strikes += 1

        print(f"[{time.strftime('%H:%M:%S')}] timeout ({strikes}/{MAX_STRIKES})")

        if strikes >= MAX_STRIKES:
            print(f"[{time.strftime('%H:%M:%S')}] erro critico")