import os
import json
import platform
import subprocess
import sys
# import tkinter as tk
# from tkinter import filedialog

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    _localDir = sys._MEIPASS
else:
    _localDir = os.path.dirname(os.path.abspath(__file__))

_metadataFile = "metadata.json"

#read data from json file
_sohDir = None
_romDir = None
_sohVersions = []

#jsonNames
_sohDirName = "SOH Path"
_romDirName = "ROM Path"
_sohVersionsName = "SOH Versions"
_sohVersionNumberName = "Number"
_sohVersionName = "Name"
_sohVersionPathName = "Path"
_sohVersionDefaultName = "Default"

#json indentation
ind = 4

def main():
    # root = tk.Tk()
    # root.withdraw()
    
    #if(not os.path.isfile(_metadataFile)):
    # setSohDir("/home/matt/Downloads/SOH")
    # setRomDir("/home/matt/Downloads/SOH/soh-linux-compatibility/ZELOOTD.z64")
    data = getJson()
    setSohDir(data[_sohDirName])
    setRomDir(data[_romDirName])
    setSohVersions(data[_sohVersionsName])

    #createMetadataFile()   
    #setJsonSohVersions()

    #setJsonDefaultVersion("soh-linux-compatibility")

    #runSOH(os.path.join(_sohDir, "soh-linux-compatibility"))
    #print(_sohDir)
    #print(_romDir)

    
    #print(json.dumps(data, indent = 4))
    
    listVersions(_sohVersions)
    print(data)

    #symRom('/home/matt/Downloads/SOH/SoH-MacReady-Charlie-Linux-Performance')
#.split('_')
#os.symlink()

########################################################################################
#set local variables
def setSohDir(path):
    global _sohDir 
    
    lpath = os.path.normcase(path)

    if (os.path.isdir(lpath)):
        _sohDir = lpath

def setRomDir(path):
    global _romDir
    
    lpath = os.path.normcase(path)
    ext = lpath.rpartition('.')[-1]

    if (os.path.isfile(lpath) and ext == "z64"):
        _romDir = lpath 

def setSohVersions(sohDict):
    global _sohVersions

    _sohVersions = sohDict

#get local variables
def getSohDir():
    return _sohDir

def getRomDir():
    return _romDir

def getSohVersions():
    return _sohVersions

########################################################################################
#symlink rom file
def symlinkRom(path):
    global _romDir

    romName = os.path.basename(_romDir)
    os.symlink(_romDir, os.path.join(path, romName))

########################################################################################
#json Manipulation
def createMetadataFile():
    global _metadataFile
    
    #load data for json
    data = {
        _sohDirName : _sohDir,
        _romDirName : _romDir,
        _sohVersionsName : {}
    }

    with open(_metadataFile, "w+") as jsonFile:
        json.dump(data, jsonFile, indent = ind)

def setJsonSohVersions():
#could use this when SOH supports arguments
#p = subprocess.Popen(["python", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    with open(_metadataFile, "r+") as jsonFile:
        jsonData = json.load(jsonFile)

        #loop for adding SOH Version metadata
        for version in getVersionsSOHPath(_sohDir):
            
            #check if version is already in the file before adding it again
            if (version not in jsonData[_sohVersionsName]):

                jsonData[_sohVersionsName].update({version : {
                    _sohVersionNumberName : "unknown",
                    _sohVersionName : version,
                    _sohVersionPathName : os.path.join(_sohDir, version),
                    _sohVersionDefaultName : 0
                }})
            
        jsonFile.seek(0)
        
        json.dump(jsonData, jsonFile, indent = ind)

def setJsonDefaultVersion(version):

    with open(_metadataFile, "r+") as jsonFile:
        jsonData = json.load(jsonFile)

        #check if version is already in the file before adding it again
        if (version in jsonData[_sohVersionsName]):
            
            #set all default values to 0
            for versions in jsonData[_sohVersionsName]:
                jsonData[_sohVersionsName][versions][_sohVersionDefaultName] = 0

            #set new default to 1
            jsonData[_sohVersionsName][version][_sohVersionDefaultName] = 1

            jsonFile.seek(0)
        
            json.dump(jsonData, jsonFile, indent = ind)

#Get JSON data
def getJson():
    
    with open(_metadataFile, "r") as jsonFile:
        jsonData = json.load(jsonFile)

    return jsonData

########################################################################################
#file system access
def runSOH(path):

    os.chdir(path)

    #need help testing on other platforms 
    match platform.system():
        case "Darwin":
            subprocess.run(
                os.path.join(path, 'soh.exe'),
                stdout = subprocess.DEVNULL,
                stderr = subprocess.DEVNULL
            )
        case "Linux":
            subprocess.run(
                os.path.join(path,'soh.appimage'), 
                stdout = subprocess.DEVNULL,
                stderr = subprocess.DEVNULL
            )
        case "Windows":
            subprocess.run(
                os.path.join(path, 'soh.exe'),
                stdout = subprocess.DEVNULL,
                stderr = subprocess.DEVNULL
            )
    os.chdir(_localDir)
    print(_localDir)

def getVersionsSOHPath(path):
    files_dir = [
        f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))
    ]
    return files_dir

# def setSohDir():
#     global _sohDir 

#     _sohDir = filedialog.askdirectory(initialdir=_sohDir, title="Select SOH folder")
#     #update json file

# def setRomDir():
#     global _romDir
    
#     _romDir = filedialog.askopenfilename(initialdir = _romDir, title = "Select Rom File", filetypes = (("z64 files","*.z64"),("all files","*.*")))
#     #update json file

def listVersions(versions):
    for version in versions:
        print(version)

if __name__ == '__main__':
    main()