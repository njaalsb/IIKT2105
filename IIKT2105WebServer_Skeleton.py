from socket import *
# Additional imports for graceful shutdown.
import signal
import sys

# Prepare sever socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 6789
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

print('The server is ready to receive')

# Handle Ctrl+C (SIGINT) to close the socket gracefully.
def signal_handler(sig, frame):
    print("\nShutting down the server")
    serverSocket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Actual server logic
while True:
    # Establish the connection
    print('Ready to serve')
    connectionSocket, addr = serverSocket.accept()
    try:
        # Receive and decode request message from client.
        request = connectionSocket.recv(1024).decode()
        # Extract file path from request and attempt to open it.
        # Note: the path is relative to the location of the server program, i.e., a request for 
        #       /index.html would attempt access the file index.html in the same folder as IIKT2105WebServer.py.
        filename = request.split()[1]
        f = open(filename[1:])
        # Read the contents of the requested file into outputdata.
        outputdata = f ## TODO fill in.
        ## TODO fill in start.
        header = "HTTP/1.1 200 \r\n\r\n"
        connectionSocket.send(header)
        # Send the appropriate HTTP header line into the socket
        # The basic format is "HTTP/1.1 CORRECTHTTPCODE\r\n\r\n", replacing CORRECTHTTPCODE with the actual code.
        ## TODO fill in end.
        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
    # Handle IOError when the file is not available.
    except IOError:
        ## TODO fill in start.
        error = "404 page not found"
        connectionSocket.send(error.encode())
        ## TODO fill in end.
    
    ## TODO fill in start.
    connectionSocket.close()
    ## TODO fill in end.