import socket as s
import threading
import time
import os
import tkinter as tk

read = s.socket(s.AF_INET, s.SOCK_DGRAM)
read.bind(('', 2222))

write = s.socket(s.AF_INET, s.SOCK_DGRAM)
write.setsockopt(s.SOL_SOCKET, s.SO_BROADCAST, 1)

IP = s.gethostbyname(os.environ['COMPUTERNAME'])

people = []

def listenThread():
    global text
    while True:
        msg, add = read.recvfrom(1024)
        msg = msg.decode('utf-8')
        ip, port = add

        if msg.startswith('\r'):
            #Handle as a request
            if msg.startswith('\rGET PEOPLE;'):
                p = msg[msg.find(';') + 1:]
                people.append(p)
                print(p + " has connected.\n")
                write.sendto(b'\rSEND NAME;' + bytes(name, 'utf-8'), (ip, 2222))
            if msg.startswith('\rSEND NAME;'):
                if not ip == IP:
                    people.append(msg[msg.find(';') + 1:])
                    print(ip)
            if msg.startswith('\rDEL NAME;'):
                try:
                    people.remove(msg[msg.find(';') + 1:])
                except ValueError:
                    print('Bad Name Value')
        else: 
            text.configure(state="normal")
            text.insert(tk.END, msg + '\n')
            text.configure(state="disabled")
            text.see("end")

def sendMessage(text):
    global writer, root
    writer.delete(0, tk.END)
    if text == '/EXIT':

        try:
            read.close()
        except OSError:
            print('Failed to close read port')
        
        write.sendto(bytes(name + " disconnected", 'utf-8'), ('255.255.255.255', 2222))
        write.sendto(bytes('\rDEL NAME;' + name, 'utf-8'), ('255.255.255.255', 2222))
        write.close()
        
        root.destroy()
        exit(2)
        
    write.sendto(bytes(name + ": " + text, 'utf-8'), ('255.255.255.255', 2222))





rThread = threading.Thread(target=listenThread)

name = ""
while name == "":
    name = input('Please specify your name: ').strip()
    
print('To exit the chat type:/EXIT')

root = tk.Tk()
root.resizable(False, False)
root.title('NBHS Chat')
text = tk.Text(root)
text.configure(state="disabled")
text.grid(column=0, row=0)
writer = tk.Entry(root, width=100)
writer.bind('<Return>', lambda e: sendMessage(writer.get()))
writer.grid(column=0, row=1)

write.sendto(b'\rGET PEOPLE;' + bytes(name, 'utf-8'), ('255.255.255.255', 2222))
rThread.start()

root.mainloop()
    

