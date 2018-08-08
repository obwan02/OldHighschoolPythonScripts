import socket as s
import threading
import time
import ctypes
import os
import tkinter as tk

write, read = (None, None)

try:
    read = s.socket(s.AF_INET, s.SOCK_DGRAM)
    read.bind(('', 2222))

    write = s.socket(s.AF_INET, s.SOCK_DGRAM)
    write.setsockopt(s.SOL_SOCKET, s.SO_BROADCAST, 1)
except OSError as e:
    ctypes.windll.user32.MessageBoxW(0, 'The NBHS Chat is already open.', 'Already Open', 0)
    exit(2)

IP = s.gethostbyname(os.environ['COMPUTERNAME'])

people = []


privMessages = {}
texts = []

def sendPrivateMessage(peep:tuple, msg):
    global write
    write.sendto(bytes('\rPRIV;') + bytes(peep[0]) + b': ' + bytes(msg), (peep[1], 2222))

def addText(txt, ip, isGlobal):
    global text

    if isGlobal:
        if selected != 'GLOBAL':
            return
    else:
        if selected == 'GLOBAL':
            return
        elif selected[1] != ip:
            return
        
    
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
                addText(p + " has connected.", None, True)
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
            if msg.startswith('\rPRIV;'):
                txt = msg[msg.find(';') + 1:]
                try:
                    privMessages[ip].append(txt)
                except KeyError:
                    privMessages[ip] = [txt]
        else:
            addText(msg, None, True)
            texts.append(msg)


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
        
    if selected == 'GLOBAL':      
        write.sendto(bytes(name + ": " + text, 'utf-8'), ('255.255.255.255', 2222))
    else:
        write.sendto(bytes('\rPRIV' + ";" + text, 'utf-8'), ('255.255.255.255', 2222))
        

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
        peopleList.insert(tk.END, i[0] + ": " + i[1])

def openPrivMsg(e):
    global selected
    index = peopleList.curselection()[0]
    item = people[int(index)]

    if selected == item:
        return

    if selected == 'GLOBAL' and item[1] == IP:
        return
    
    if item[1] == IP:
        selected = 'GLOBAL'
    text.delete(0, tk.END)

    if selected == 'GLOBAL':
        for i in texts:
            text.insert(tk.END, i)
    else:
        t = privMessages[item[1]]
        for i in t:
            test.insert(tk.END, i)
        
    

selected = 'GLOBAL'

rThread = threading.Thread(target=listenThread)

name = os.environ['USERNAME']
    
print('To exit the chat type:/EXIT')

root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", disconnect)
root.resizable(False, False)
root.title('NBHS Chat')

text = tk.Text(root)
text.configure(state="disabled")
text.grid(column=0, row=0)

peopleList = tk.Listbox(root)
peopleList.bind("<Double-Button-1>", openPrivMsg)
peopleList.grid(column=1, row=0)

writer = tk.Entry(root, width=100)
writer.bind('<Return>', lambda e: sendMessage(writer.get()))
writer.grid(column=0, row=1, rowspan=1)

write.sendto(b'\rGET PEOPLE;' + bytes(name, 'utf-8'), ('255.255.255.255', 2222))
rThread.start()

root.mainloop()
    

