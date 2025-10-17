import time
from socket import *

serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

rtts = []
sent_packets = 10
received_packets = 0

for sequence_number in range(1, 11):
    send_time = time.time()
    message = f"Ping {sequence_number} {send_time}"
    try:
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
