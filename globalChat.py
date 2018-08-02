import socket as s
import threading
import time
import os

send = False

read = s.socket(s.AF_INET, s.SOCK_DGRAM)
read.bind(('', 2222))

write = s.socket(s.AF_INET, s.SOCK_DGRAM)
write.setsockopt(s.SOL_SOCKET, s.SO_BROADCAST, 1)

def listenThread():
    while True:
        msg = read.recvfrom(1024)
        print(msg)

rThread = threading.Thread(target=listenThread)

name = input('Please specify your name: ')
print('To exit the chat type:(EXIT)')
time.sleep(5)
os.system('cls')

rThread.start()
while True:
    text = input('>')
    if text == '(EXIT)':
        break
    write.sendto(bytes(name + ": " + text), ('255.255.255.255', 2222))

read.close()
write.close()
    
