import os

def fail(s):
    input(s + " (Press Enter to Exit)")
    exit(0)

while True:    
    path = input("Folder Path: ")

    if not os.path.isdir(path):
        fail("Invalid Path")
        
    files = [os.path.join(path, x) for x in os.listdir(path)]

    ext = input("Extension To be Applied to All Files: ")
    if len(ext) < 2 or ext[0] != '.':
        fail("Invalid Extension")



    for i in files:
        name, e = os.path.splitext(i)
        os.rename(i, name + ext)


