# TCPServer.py

from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('The server is ready to receive')

user2 = input('Username: ')

while True:
    print("Waiting for connection...")
    connectionSocket, addr = serverSocket.accept()

    user1 = connectionSocket.recv(1024).decode()
    connectionSocket.send(user2.encode())

    print('\nYou are now chatting with', '\033[1m' + user1 + '\033[0m' + '!')
    print('Type \033[1m"bye"\033[0m to end the chat.')
    print("Waiting for response...")

    while True:
        message = connectionSocket.recv(1024).decode()
        print('\033[1m' + user1 + '\033[0m: ' + message)

        if message == 'bye':
            print(user1 + ' left the chat.')
            break

        reply_message = input('\033[1m' + user2 + '\033[0m: ')
        connectionSocket.send(reply_message.encode())
        print("Waiting for response...")
        if reply_message == 'bye':
            print('You left the chat.')
            break

    connectionSocket.close()
    break

serverSocket.close()