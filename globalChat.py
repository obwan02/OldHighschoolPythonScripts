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

def addText(txt):
    global text
    text.configure(state="normal")
    text.insert(tk.END, txt + '\n')
    text.configure(state="disabled")
    text.see("end")

def listenThread():
    global text, people, root
    while True:

        msg, add = (None, None)
        try:    
            msg, add = read.recvfrom(1024)
        except OSError:
            root.destroy()
            exit(0)
            return

        if msg == None or add == None:
            continue
        msg = msg.decode('utf-8')
        ip, port = add
        
        if msg.startswith('\r'):
            #Handle as a request
            if msg.startswith('\rGET PEOPLE;'):
                p = msg[msg.find(';') + 1:]


                #Check for duplicates
                duplicate = False
                dupToRemove = None
                for i in people:
                    if i[1] == ip:
                        duplicate = True
                        dupToRemove = i

                if duplicate:
                    people.remove(dupToRemove)
                people.append((p, ip))
                updatePeople()
                
                print(p + " has connected.\n")
                addText(p + " has connected.")
                write.sendto(b'\rSEND NAME;' + bytes(name, 'utf-8'), (ip, 2222))
            if msg.startswith('\rSEND NAME;'):
                if not ip == IP:
                    n = msg[msg.find(';') + 1:]
                    people.append((n, ip))
                    updatePeople()
            if msg.startswith('\rDEL NAME;'):
                try:
                    people.remove((msg[msg.find(';') + 1:], ip))
                    updatePeople()
                except ValueError:
                    print('Bad Name Value')
        else: 
            addText(msg)


lastSendTime = 0

def sendMessage(text):
    global writer, root, people, lastSendTime

    if text.strip() == "":
        print("Spam message detected")
        return
    if time.time() - lastSendTime < 2:
        print('Sending messages too quickly')
        lastSendTime = time.time()
        return
    
    writer.delete(0, tk.END)
    if text == '/EXIT':
        
        root.destroy()
        exit(0)
        
    write.sendto(bytes(name + ": " + text, 'utf-8'), ('255.255.255.255', 2222))

def disconnect():
    try:
        read.close()
    except OSError:
        print('Failed to close read port')
        
    write.sendto(bytes(name + " disconnected", 'utf-8'), ('255.255.255.255', 2222))
    write.sendto(bytes('\rDEL NAME;' + name, 'utf-8'), ('255.255.255.255', 2222))
    write.close()

def updatePeople():
    global people, peopleList

    peopleList.delete(0, tk.END)

    for i in people:
        peopleList.insert(tk.END, i[0] + " - " + i[1])


rThread = threading.Thread(target=listenThread)

name = ""
while name == "":
    name = input('Please specify your name: ').strip()
    
print('To exit the chat type:/EXIT')

root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", disconnect)
root.resizable(False, False)
root.title('NBHS Chat')

text = tk.Text(root)
text.configure(state="disabled")
text.grid(column=0, row=0)

peopleList = tk.Listbox(root)
peopleList.grid(column=1, row=0)

writer = tk.Entry(root, width=100)
writer.bind('<Return>', lambda e: sendMessage(writer.get()))
writer.grid(column=0, row=1, rowspan=2)

write.sendto(b'\rGET PEOPLE;' + bytes(name, 'utf-8'), ('255.255.255.255', 2222))
rThread.start()

root.mainloop()
    

