import time
from socket import *

# define o endereço do servidor
serverName = 'localhost'

# Porta do servidor
serverPort = 12000

# cria o socket do cliente
# AF_INET = IPv4
# SOCK_DGRAM = UDP (datagramas)
clientSocket = socket(AF_INET, SOCK_DGRAM)

# se o server nao comunicar dentro de 1 segundo, uma exception vai estourar.
clientSocket.settimeout(1)

rtts = []  # lista para guardar os tempos de cada ping que deu certo
sent_packets = 10  # numero de pings que vamos tentar enviar
received_packets = 0  # contador de quantos voltaram

for sequence_number in range(1, sent_packets + 1):

    # hora de envio
    send_time = time.time()

    message = f"Ping {sequence_number} {send_time}"

    try:
        # encode = transforma a string em bytes para trafegar pela rede
        # sendto = envia o pacote para o endereco e porta definidos
        clientSocket.sendto(message.encode(), (serverName, serverPort))

        # recvfrom = o script aguarda a resposta
        # 1024 = tamanho do buffer (tamanho máximo em bytes do pacote que aceitamos receber)
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)

        # hora de chegada.
        recv_time = time.time()

        # RTT = hora da chegada - hora do envio
        rtt = recv_time - send_time
        rtts.append(rtt)
        received_packets += 1

        print(f"Resposta do servidor: {modifiedMessage.decode()}")
        print(f"RTT = {rtt:.6f} segundos")

    except timeout:
        print("Request timed out")

    # espera um pouquinho antes do próximo ping
    time.sleep(0.3)

# fecha o socket liberando a porta efemera
clientSocket.close()

if rtts:
    min_rtt = min(rtts)
    max_rtt = max(rtts)
    avg_rtt = sum(rtts) / len(rtts)
else:
    min_rtt = max_rtt = avg_rtt = 0

packet_loss = ((sent_packets - received_packets) / sent_packets) * 100

print(f"Pacotes enviados: {sent_packets}")
print(f"Pacotes recebidos: {received_packets}")
print(f"Pacotes perdidos: {sent_packets - received_packets} ({packet_loss:.1f}%)")
print(f"RTT mínimo = {min_rtt:.6f} segundos")
print(f"RTT máximo = {max_rtt:.6f} segundos")
print(f"RTT médio  = {avg_rtt:.6f} segundos")