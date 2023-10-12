# TCPClient.py

from socket import *
serverName = "localhost"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)

print("Connecting to server...")
clientSocket.connect((serverName,serverPort))
print("Connected to server!")

user1 = input('Username: ')
clientSocket.send(user1.encode())

user2 = clientSocket.recv(1024).decode()
print('\nYou are now chatting with', '\033[1m' + user2 + '!\033[0m')
print('Type \033[1m"bye"\033[0m to end the chat.')

while True:
    message = input('\033[1m' + user1 + '\033[0m: ')
    clientSocket.send(message.encode())

    if message == 'bye':
        print('You ended the chat')
        break

    print("Waiting for response...")
    recieved_message = clientSocket.recv(1024).decode()
    print('\033[1m' + user2 + '\033[0m: ' + recieved_message)

    if recieved_message == 'bye':
        print(user2 + ' left the chat')
        break

clientSocket.close()