#! /usr/bin/env python3
#
# mytar.py.
#

import os
import sys

progName = sys.argv[0]

#error message then stop running
def err(msg):
    os.write(2,f"{progName}: {msg}\n".encode());
    sys.exit(1)

#print something
def msg(msg):
    os.write(2,f"{progName}: {msg}\n".encode());

def compress(files,cFile):
    with open(cFile,'wb') as x:
        for file in files:
            if not os.path.exists(file):
                err(f"{file}: was not found")
            fileName = file.encode('utf-8')
            msg(f"{fileName} being compress")
            x.write(len(fileName).to_bytes(4,'big'))
            x.write(fileName)
            x.write(os.path.getsize(file).to_bytes(8,'big'))
            with open(file,'rb')as y:
                x.write(y.read())
            
def extract(cFile,location):
    with open(cFile,'rb') as x:
        while True:
            nameLength = int.from_bytes(x.read(4),'big')
            if nameLength == 0:
                break
            fileName = x.read(nameLength).decode('utf-8')
            fileSize = int.from_bytes(x.read(8),'big')

            path = os.path.join(location,fileName)
            with open(path,'wb') as destination:
                destination.write(x.read(fileSize))
        
#Start of main
msg(f"Welcome usage: mytar.py c|x compress_file_name file1 file2 file3...")
if len(sys.argv)<4:
    err(f"Missing arguments.")

option = sys.argv[1]
cFile = sys.argv[2]
files = sys.argv[3:]

if option == 'c':
    compress(files,cFile)
elif option == 'x':
    extract(cFile,'.')
else:
    err(f"option not valid: only c or x are valid \nc for compressing and x for extracting")