from socket import *

serverName = '10.24.37.66'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
message = 'Ping'

clientSocket.sendto(message.encode(), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()