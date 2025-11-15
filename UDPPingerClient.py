import time
from socket import *

# Endereço do servidor
serverName = 'localhost'

# Porta do servidor
serverPort = 12000

# Cria um socket UDP (AF_INET = IPV4, SOCKGRAM = Protocolo UDP)
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Timeout de 1 segundo, se nao responder lança exception
clientSocket.settimeout(1)

# Armazena os tempos de resposta bem sucedidos
rtts = []

# Pacotes enviados
sent_packets = 10

# Pacotes perdidos
received_packets = 0

# Loop de Pings
for sequence_number in range(1, sent_packets+1):

    # Captura o momento exato do envio
    send_time = time.time()

    # Formata a mensagem para o padrão especificado
    message = f"Ping {sequence_number} {send_time}"

    try:

        # Envia o pacote (sem conexão estabelecida previamente)
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
        recv_time = time.time()
        rtt = recv_time - send_time
        rtts.append(rtt)
        received_packets += 1
        print(f"Resposta do servidor: {modifiedMessage.decode()}")
        print(f"RTT = {rtt:.6f} segundos")
    except timeout:
        print("Request timed out")
    time.sleep(0.3)

clientSocket.close()

if rtts:
    min_rtt = min(rtts)
    max_rtt = max(rtts)
    avg_rtt = sum(rtts) / len(rtts)
else:
    min_rtt = max_rtt = avg_rtt = 0

packet_loss = ((sent_packets - received_packets) / sent_packets) * 100

print("\n--- Estatísticas do Ping ---")
print(f"Pacotes enviados: {sent_packets}")
print(f"Pacotes recebidos: {received_packets}")
print(f"Pacotes perdidos: {sent_packets - received_packets} ({packet_loss:.1f}%)")
print(f"RTT mínimo = {min_rtt:.6f} segundos")
print(f"RTT máximo = {max_rtt:.6f} segundos")
print(f"RTT médio  = {avg_rtt:.6f} segundos")
