from socket import *
import requests

from signal import signal, SIGFPE, SIG_DFL
signal(SIGFPE,SIG_DFL)


serverName = '10.24.37.66'
serverPort = 6789

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

url = "10.24.37.66:6789/HelloWorld.html"
# r = requests.get(url)

GET_request = 'HTTP/1.1 GET 10.24.37.66:6789/HelloWorld.html\r\n\r\n'
clientSocket.send(GET_request.encode())
response = clientSocket.recv(1024)

print ('From Server:', response.decode())  
clientSocket.close()