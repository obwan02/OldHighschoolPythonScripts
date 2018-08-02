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

def listenThread():
    global text
    while True:
        msg, add = read.recvfrom(1024)
        ip, port = add
        if not ip == IP:
            t = msg.decode('utf-8')
            text.configure(state="normal")
            text.insert(tk.END, t + '\n')
            text.configure(state="disabled")

def sendMessage(text):
    global writer, root
    writer.delete(0, tk.END)
    if text == '/EXIT':
        write.close()
        try:
            read.close()
        except OSError:
            pass
        root.destroy()
        exit(2)
        
    write.sendto(bytes(name + ": " + text, 'utf-8'), ('255.255.255.255', 2222))

rThread = threading.Thread(target=listenThread)
name = input('Please specify your name: ').strip()
print('To exit the chat type:/EXIT')
rThread.start()

root = tk.Tk()
text = tk.Text(root)
text.configure(state="disabled")
text.grid(column=0, row=0)
writer = tk.Entry(root, width=100)
writer.bind('<Return>', lambda e: sendMessage(writer.get()))
writer.grid(column=0, row=1)
root.mainloop()
    
