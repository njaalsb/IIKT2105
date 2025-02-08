import socket
from time import time, ctime
prev_millis = time.time()
intervall = 1
socketcreat = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for i in range(9):
    curr_millis = 0
    if (prev_millis )
    

    start_time = time()
    message = "ping" + ctime(start_time)
    socketcreat.sendto(message.encode(), ("10.24.37.66", 12000))

    data, address = socketcreat.recvfrom(1024)
    end_time = time()
    rttime = str(end_time - start_time)

    data = data.decode()
    print(f"Server: {data}")
    print("Round trip time: " + rttime)

socketcreat.close()