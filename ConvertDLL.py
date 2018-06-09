#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from ctypes import WinDLL
import sys

def LoadDLL(path, makeModule=False):

    try:
        testFile = open(path, "r")
        testFile.close()
    except FileNotFoundError:
        try:
            testFile = open("C:\\windows\\system32\\" + path)
            testFile.close()
        except FileNotFoundError as e:
            e.filename = path
            raise e
    
    try:
        os.system(r'("C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.13.26128\bin\Hostx86\x86\dumpbin.exe" /exports ' + path + ') >> TEMP')
        file = open('TEMP', 'r')
        string =''.join(file.readlines())
        #print(string)
        file.close()
        os.system('del TEMP')
        return ParseDLLExportOutput(string, path, makeModule)
    except PermissionError as e:
        raise e
    except FileNotFoundError as e:
        raise e


def ParseDLLExportOutput(dllExportOuput, path, makeModule):
    title, ext = os.path.splitext(os.path.basename(path))
    title += "_dll"
    d = dllExportOuput
    c = "ordinal hint RVA      name"
    index1 = d.find(c) + len(c)
    index2 = d.find("Summary")
    strList = d[index1:index2]
    fList = strList.split("\n")
    nameList = []
    for i in fList:
        j = i[26:].split(" ")[0]
        if j != "[NONAME]":
            nameList.append(j)

    #Try to read the ddll to check for errors such as FileNotFoundError
    testerDLL = WinDLL(path)

    file = open(title + ".py", "w")
    file.write("from ctypes import WinDLL\nfrom time import sleep\n")
    file.write("_dllHandle = WinDLL(r\"" + path + "\")\n\n")

    for i in nameList:
        func = None
        try:
            func = testerDLL.__getattr__(i)
            file.write("def " + i + "(*args):\n")
            file.write("\treturn _dllHandle." + i + "(*args)")
        except AttributeError as e:
            file.write("#function \"" + i + "\" could not be implemented")
        finally:
            file.write("\n\n")
            
    file.close()
    module = __import__(title)
    if not makeModule:
        p = os.path.dirname(os.path.realpath(__file__))
        os.system("del " + p + "\\" + title + ".py")
    return module
    

if __name__ == '__main__':

    args = sys.argv
    if len(args) > 1:
        LoadDLL(args[1], makeModule=True)
    else:
        while True:

            file = input('DLL: ')

            if os.path.isfile(file):
                LoadDLL(file, makeModule=True)
            else:
                if os.path.isfile('C:\\windows\\system32\\' + file):
                    LoadDLL('C:\\windows\\system32\\' + file, makeModule=True)
                else:
                    print('Invalid DLL')



