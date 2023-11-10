from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_pi"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
tcpSerSock.bind((sys.argv[1], 8888))
tcpSerSock.listen(100)
# Fill in end.

while 1:
    # Start recieving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)

    # Fill in start. 
    message = tcpCliSock.recv(1024).decode()
    # Fill in end.
    print(message)

    # Extract the filename from the given message
    print(message.split()[1])
    request_line = message.split('\n')[0]
    http_method, url, http_version = request_line.split()
    filename = url
    print(filename)
    fileExists = "false"
    filetouse = "/" + filename.replace("/", "")
    print(filetouse)

    try:
        # check whether the file exists in the cache
        f = open(filetouse[1:], "rb")
        outputdata = f.read()
        f.close()
        fileExists = "true"
        #Proxy server finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n")
        tcpCliSock.send("Content-Type: text/html\r\n")
        tcpCliSock.send("\r\n")
        
        # Fill in start.
        for i in outputdata:
            tcpCliSock.send(i.encode())
        # Fill in end.
            print('Read from cache')

    # Error handling for file not found in cache
    except IOError:
        if fileExists == "false":
            # Create a socket on the proxyserver
            # Fill in start.
            c =  socket(AF_INET, SOCK_STREAM)
            # Fill in end.
            hostn = filename.replace("www.", "", 1)
            print(hostn)
            try:
                # Connect to the socket on port 80
                # Fill in start.
                c.connect((hostn, 80))
                # Fill in end.
                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = c.makefile('r', 0)
                fileobj.write(f"GET /{filename} HTTP/1.0\r\nHost: {hostn}\r\n\r\n")                # Read the response into buffer
                # Fill in start.
                buffer = fileobj.readlines()
                # Fill in end.
                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket and the corresponding file in the cache
                tmpFile = open("./" + filename,"wb")
                tmpFile.write(buffer)
                tmpFile.close()
                # Fill in start.
                for i in buffer:
                    tmpFile.write(i.encode())
                    tcpCliSock.send(i.encode())
                # Fill in end.
            except:
                print("Illegal request")

        else:
            # HTTP response message for file not found
            # Fill in start.
            tcpCliSock.send("HTTP/1.0 404 Not Found\r\n")
            tcpCliSock.send("Content-Type:text/html\r\n")
            tcpCliSock.send("\r\n")
            tcpCliSock.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")
            # Fill in end.
    # Close the client and the server sockets
    tcpCliSock.close()
# Fill in start.
tcpSerSock.close()
# Fill in end.
