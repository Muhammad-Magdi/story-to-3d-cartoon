import os
import json
import sys

def readFile(path):
    with open(path, 'r') as file:
        return file.readline()

def writeFile(path, data):
    with open(path, 'w') as file:
        file.write(data)

def addAction(action):
    dataPath = os.path.join(os.getcwd(), 'data')
    dataPath = os.path.normpath(dataPath) + '/actions.json'
    data = json.loads(readFile(dataPath))
    data.append(action)
    data = json.dumps(data)
    writeFile(dataPath, data)

def log(message):
        sys.stderr.write(message + '\n')
        sys.stderr.flush()