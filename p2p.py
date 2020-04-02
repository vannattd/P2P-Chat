import os
import socket
import emojis
import sys
from threading import Thread
import time


def GetChatMessage():
    global name
    global broadSock
    global current
    while True:
        recv_message = broadSock.recv(1024)
        recv_string_message = str(recv_message.decode('utf-8'))
        if recv_string_message.find(':') != -1:
            print(emojis.encode('\r %s \n' % recv_string_message), end='')
        elif not (recv_string_message in current) and recv_string_message.find(':') == -1:
            current.append(recv_string_message)
            print('>> Now online:' + str(len(current)))


def SendMessageForChat():
    global name
    global sendSock
    sendSock.setblocking(False)
    while True:
        data = input()
        if data == 'Exit ()':
            close_message = '! @ #' + name
            sendSock.sendto(close_message.encode('utf-8'), ('255.255.255.255', 8080))
            os._exit(1)
        elif data != '' and data != 'Exit ()':
            send_message = name + ':' + data
            sendSock.sendto(send_message.encode('utf-8'), ('255.255.255.255', 8080))
        else:
            print('Write the message first!')


def SendOnlineStatus():
    global name
    global sendSock
    sendSock.setblocking(False)
    while True:
        time.sleep(1)
        sendSock.sendto(name.encode('utf-8'), ('255.255.255.255', 8080))


def main():
    global broadSock
    broadSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    broadSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadSock.bind(('0.0.0.0', 8080))
    global sendSock
    sendSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sendSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    print(emojis.encode(':star::star::star::star::star::star::star::star::star::star::star::star::star::star::star:'
                        ':star::star::star::star:'':star::star::star::star::star::star::star::star::star::star::star:'
                        ':star::star::star::star::star::star::star::star::star::star::star::star::star::star::star:'))
    print(emojis.encode(':sparkles: Welcome to the P2P chat! :sparkles:'))
    print(emojis.encode(':sparkles: To exit, send the message: Exit () :sparkles:'))
    print(emojis.encode(':sparkles: Enter your name and you can immediately write to the chat. :sparkles:'))
    print(emojis.encode(':star::star::star::star::star::star::star::star::star::star::star::star::star::star::star:'
                        ':star::star::star::star:'':star::star::star::star::star::star::star::star::star::star::star:'
                        ':star::star::star::star::star::star::star::star::star::star::star::star::star::star::star:'))

    global name
    name = ''
    while True:
        if not name:
            name = input('Your name:')
            if not name:
                print('Enter a non-empty name!')
            else:
                break
    print(emojis.encode(':star::star::star::star::star::star::star::star::star::star::star::star::star::star::star:'
                        ':star::star::star::star:'':star::star::star::star::star::star::star::star::star::star::star:'
                        ':star::star::star::star::star::star::star::star::star::star::star::star::star::star::star:'))

    global recvThread
    recvThread = Thread(target=GetChatMessage)
    global sendThread
    sendThread = Thread(target=SendMessageForChat)

    global current
    current = []

    global onlineThread
    onlineThread = Thread(target=SendOnlineStatus)

    recvThread.start()
    sendThread.start()
    onlineThread.start()

    recvThread.join()
    sendThread.join()
    onlineThread.join()


if __name__ == '__main__':
    main()
