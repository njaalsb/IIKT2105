from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

print('The server is ready to receive')

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    print("Got message %s from client %s, returning %s." % (message, clientAddress, modifiedMessage))
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)