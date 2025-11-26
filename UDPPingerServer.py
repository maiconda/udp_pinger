import random
from socket import *

# cria o socket do server
# AF_INET = IPv4
# SOCK_DGRAM = UDP (datagramas)
serverSocket = socket(AF_INET, SOCK_DGRAM)

# bind = associa o socket a um endereço e porta específicos
# '' = escutar todas as interfaces de rede desta máquina
# 12000 = porta
serverSocket.bind(('', 12000))

print("O servidor está pronto para receber...")

while True:
    rand = random.randint(1, 10)

    # recvfrom = o script aguarda a resposta
    # 1024 = tamanho do buffer (tamanho máximo em bytes do pacote que aceitamos receber)
    message, address = serverSocket.recvfrom(1024)

    message = message.upper()

    if rand < 4:
        print(f"pacote de {address} ignorado")
        continue

    # sendto usa o endereço que capturamos no recvfrom para saber para onde devolver
    serverSocket.sendto(message, address)
    print(f"Respondido para {address}")