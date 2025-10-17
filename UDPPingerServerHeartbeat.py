import random
import time
from socket import *

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', 12000))

expected_heartbeats = 10
received_heartbeats = 0
delays = []
last_seq = 0
lost_heartbeats = 0

print("Servidor Heartbeat aguardando pacotes...")

while received_heartbeats < expected_heartbeats:
    rand = random.randint(0, 9)
    message, address = serverSocket.recvfrom(1024)
    if rand < 3:
        continue
    recv_time = time.time()
    decoded = message.decode()
    parts = decoded.split()
    seq = int(parts[1])
    sent_time = float(parts[2])
    delay = recv_time - sent_time

    if last_seq != 0 and seq > last_seq + 1:
        lost = seq - last_seq - 1
        lost_heartbeats += lost
        print(f"Heartbeats perdidos: {lost} (entre {last_seq} e {seq})")

    print(f"Heartbeat recebido: seq={seq}, atraso={delay:.6f} segundos")
    delays.append(delay)
    last_seq = seq
    received_heartbeats += 1

if delays:
    min_delay = min(delays)
    max_delay = max(delays)
    avg_delay = sum(delays) / len(delays)
else:
    min_delay = max_delay = avg_delay = 0

packet_loss = ((expected_heartbeats - received_heartbeats + lost_heartbeats) / expected_heartbeats) * 100

print("\n--- Estatísticas do Heartbeat ---")
print(f"Heartbeats esperados: {expected_heartbeats}")
print(f"Heartbeats recebidos: {received_heartbeats}")
print(f"Heartbeats perdidos: {expected_heartbeats - received_heartbeats + lost_heartbeats} ({packet_loss:.1f}%)")
print(f"Atraso mínimo = {min_delay:.6f} segundos")
print(f"Atraso máximo = {max_delay:.6f} segundos")
print(f"Atraso médio  = {avg_delay:.6f} segundos")
