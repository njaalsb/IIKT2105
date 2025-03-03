from socket import *
import time 

serverName =  "127.0.0.1"  #"10.24.37.66"  # IP address to the UDP-serveren
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)  # 1 second timeout 

num_pings = 10
lost_packets = 0
rtt_list = []

for i in range(1, num_pings + 1):
    send_time = time.time()
    message = f"ping {i} {send_time}"
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    
    try:
        response, serverAddress = clientSocket.recvfrom(1024)
        recv_time = time.time()
        rtt = (recv_time - send_time) * 1000  # Converting to milliseconds 
        rtt_list.append(rtt)
        
        print(f"Ping {i}: Reply from {serverName}, RTT = {rtt:.3f} ms")
    except timeout:
        print(f"Ping {i}: Request timed out")
        lost_packets += 1

clientSocket.close()

# Calculating statistics
if rtt_list:
    min_rtt = min(rtt_list)
    max_rtt = max(rtt_list)
    avg_rtt = sum(rtt_list) / len(rtt_list)
else:
    min_rtt = max_rtt = avg_rtt = 0.0

packet_loss = (lost_packets / num_pings) * 100

# Ping statistics 
print(f"Packets: Sent = {num_pings}, Received = {num_pings - lost_packets}, Lost = {lost_packets} ({packet_loss:.1f}% loss)")
print(f"RTT: Min = {min_rtt:.3f} ms, Max = {max_rtt:.3f} ms, Avg = {avg_rtt:.3f} ms")
