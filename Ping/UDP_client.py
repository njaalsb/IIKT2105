# Kode for å pinge UDP server:
# Ikke ferdig: https://github.com/selbyk/python-udp-ping/blob/master/UDPPingClient.py
import time 
from socket import *

serverName = '10.24.37.66'
serverPort = 12000

sequence_number = 1
num_pings = 10
min_rtt = 0
max_rtt = 0
avg_rtt = 0
packets_dropped = 0.0
total_packets = 0.0

clientSocket = socket(AF_INET, SOCK_DGRAM)

clientSocket.settimeout(1.0)

clientSocket.bind(serverName, serverPort)

def get_time():
    return int(round(time.time()*1000))

def wait_for_response():
    global packets_dropped
    while True:
        try:
            message, serverAddress = clientSocket.recvfrom(serverPort)
            return message
        except Exception:
            packets_dropped = packets_dropped + 1
            return 'ERROR 522' + str(get_time()) + 'TIMEOUT'

def send_message(message, wait=False):
    clientSocket.sendto(message, (serverName, serverPort))
    if wait ==  False:
        return
    else:
        return wait_for_response

print("UDP socket is listening for incoming packets on port", clientSocket.getsockname()[1])

while sequence_number <= num_pings:
    message = 'PING ' + str(sequence_number) + ' ' + str(get_time())
    
    recieved = send_message(message, True)
    recieved_size = len(recieved)
    recieved_array = recieved.split(' ')
    recieved_type = recieved_array[0].upper()
    
    recieved_seq = int(recieved_array[1])
    recieved_time = int(recieved_array[2])

    rtt = get_time() - recieved_time
    if rtt > 1000:
        continue
    if recieved_type == 'PING':
        print (str(recieved_size) + " bytes recieved from " + serverName + ':' + str(serverPort) + ': seq=' + str(recieved_seq) + ' rtt=' + str(rtt))
        avg_rtt = avg_rtt + rtt
    if rtt < min_rtt or min_rtt == 0:
        min_rtt = rtt
    if rtt > max_rtt or max_rtt == 0:
        max_rtt = rtt
        sequence_number = sequence_number + 1
    elif recieved_type == 'ERROR':
        recieved_message = recieved_array[3]
        print(recieved)
    else:
        print('Something went wrong, but I have no idea what it is.')
    last = recieved

    total_packets = total_packets + 1
    

# Out of the loop, report running statistics
print ("RTT: min=" + str(min_rtt) + " max=" + str(max_rtt) + " avg=" + str(avg_rtt/10))
print ("Packet Loss: " + str(packets_dropped/total_packets*100) + "%")
'''
    clientSocket.sendto(message.encode(), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
print(modifiedMessage.decode())
clientSocket.close()
'''