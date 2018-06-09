import os

DIR_PATH = os.path.dirname(os.path.abspath(__file__)) + "/Dell"

def LoadModule(absPath):
    title, ext = os.path.splitext(os.path.basename(absPath))
    file = open(absPath, "r")
    data = file.read()
    file.close()

    file = open(title + "__TEMP.py", "w")
    file.write(data)
    file.close()

    module = __import__(title + "__TEMP")
    os.remove(DIR_PATH + title + "__TEMP.py")
    return module


    
def search(value, string):
    result = []
    curr = ""
    index = 0
    for i in range(0, len(string)):
        curr += string[i]

        if value == curr:
            result.append(i - len(value) + 1)
            index = 0
            curr = ""
        elif value[index] == string[i]:
            index += 1
        else:
            index = 0
            curr = ""

    return result
        
        
