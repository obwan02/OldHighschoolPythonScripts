import socket as s
import threading
import time
import ctypes
import os
import tkinter as tk
#lol xD 
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

def addText(txt, ip, isGlobal):
    global text

    if isGlobal:
        if selected != 'GLOBAL':
            return
    else:
        if selected == 'GLOBAL':
            return
        if selected[1] != ip:
            return
        
    
    text.configure(state="normal")
    text.insert(tk.END, txt + '\n')
    text.configure(state="disabled")
    text.see("end")

    if isGlobal:
        texts.append(txt)
    else:
        privMessages[ip].append(txt)

def listenThread():
    global text, people, root, writer

    write.sendto(b'\rGET PEOPLE;' + bytes(name, 'utf-8'), ('255.255.255.255', 2222))
    
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
                privMessages[ip] = []
                updatePeople()
                
                print(p + " has connected.\n")
                addText(p + " has connected.", None, True)
                write.sendto(b'\rSEND NAME;' + bytes(name, 'utf-8'), (ip, 2222))
            if msg.startswith('\rSEND NAME;'):
                if not ip == IP:
                    n = msg[msg.find(';') + 1:]
                    people.append((n, ip))
                    privMessages[ip] = []
                    updatePeople()
            if msg.startswith('\rDEL NAME;'):
                try:
                    people.remove((msg[msg.find(';') + 1:], ip))
                    updatePeople()
                except ValueError:
                    print('Bad Name Value')
            if msg.startswith('\rPRIV;'):
                txt = msg[msg.find(';') + 1:]
                addText(txt, ip, False)
        else:
            addText(msg, None, True)


lastSendTime = 0
lastMessage = ""
def sendMessage(txt):
    global writer, root, people, lastSendTime, text

    if txt.strip() == "":
        print("Spam message detected")
        return

    if lastMessage == txt:
        print("Spam detected")
    
    if time.time() - lastSendTime < 2:
        print('Sending messages too quickly')
        lastSendTime = time.time()
        return
    
    writer.delete(0, tk.END)
    if txt == '/EXIT':
        
        root.destroy()
        exit(0)
        
    if selected == 'GLOBAL':      
        write.sendto(bytes(name + ": " + txt, 'utf-8'), ('255.255.255.255', 2222))
    else:
        n, ip = selected

        write.sendto(bytes('\rPRIV' + ';' + name + ": " + txt, 'utf-8'), (ip, 2222))

        text.configure(state="normal")
        text.insert(tk.END, "You: " + txt + "\n")
        text.configure(state="disabled")
        privMessages[ip].append("You: " + txt)
    lastMessage = txt

def disconnect():
    try:
        read.close()
    except OSError:
        print('Failed to close read port')
        
    write.sendto(bytes(name + " disconnected", 'utf-8'), ('255.255.255.255', 2222))
    write.sendto(bytes('\rDEL NAME;' + name, 'utf-8'), ('255.255.255.255', 2222))
    write.close()
    
    exit(0)

def updatePeople():
    global people, peopleList

    peopleList.delete(0, tk.END)

    for i in people:
        peopleList.insert(tk.END, i[0] + ": " + i[1])

def openPrivMsg(e):
    global selected, text
    index = peopleList.curselection()[0]
    item = people[int(index)]
    
    text.configure(state="normal")
    text.delete("1.0", tk.END)

    selected = item
    if item[1] == IP:
        selected = 'GLOBAL'

    if selected == 'GLOBAL':
        for i in texts:
            text.insert(tk.END, i + "\n")
    else:
        t = privMessages[item[1]]
        for i in t:
            text.insert(tk.END, i + "\n")
    text.configure(state="disabled")
        
    

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

rThread.start()
root.mainloop()
    

