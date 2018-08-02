import socket as s
import threading
import time
import os

send = False

read = s.socket(s.AF_INET, s.SOCK_DGRAM)
read.bind(('', 2222))

write = s.socket(s.AF_INET, s.SOCK_DGRAM)
write.setsockopt(s.SOL_SOCKET, s.SO_BROADCAST, 1)

IP = s.gethostbyname(os.environ['COMPUTERNAME'])

def listenThread():
    while True:
        msg, add = read.recvfrom(1024)
        ip, port = add
        if not ip == IP:
            print(msg.decode('utf-8'))

rThread = threading.Thread(target=listenThread)

name = input('Please specify your name: ').strip()
print('To exit the chat type:(EXIT)')
time.sleep(1)
os.system('cls')

rThread.start()
while True:
    text = input('>')
    if text == '(EXIT)':
        break
    write.sendto(bytes(name + ": " + text, 'utf-8'), ('255.255.255.255', 2222))

read.close()
write.close()
    
