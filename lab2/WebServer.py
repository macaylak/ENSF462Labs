#import socket module
from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a server socket
# Fill in start
serverPort = 6789 
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(1)
# Fill in end

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()  # Accept a connection
    try:
        message = connectionSocket.recv(1024).decode()  # Receive the HTTP request from the client
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        # Send one HTTP header line into socket
        # Fill in start
        response_header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        connectionSocket.send(response_header.encode())
        # Fill in end

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:
        # Send response message for file not found
        # Fill in start
        response_header = "HTTP/1.1 404 Not Found\r\n\r\n"
        response_message = "<html><body><h1>404 Not Found</h1></body></html>"
        connectionSocket.send(response_header.encode())
        connectionSocket.send(response_message.encode())
        # Fill in end

        # Close client socket
        # Fill in start
        connectionSocket.close()
        # Fill in end

serverSocket.close()
