import os
import json
import platform
import subprocess
import shutil

class sohFileHandler:
    #constructors
    def __init__(self):

        self.__metadataFile = "metadata.json"

        #jsonNames
        self.__sohDirName = "SOH Path"
        self.__romDirName = "ROM Path"
        self.__sohVersionsName = "SOH Versions"
        self.__sohVersionNumberName = "Number"
        self.__sohVersionName = "Name"
        self.__sohVersionPathName = "Path"
        self.__sohVersionDefaultName = "Default"

        #json indentation
        self.__ind = 4

        self.__sohDir = None
        self.__romDir = None
        self.__default = None
        self.__sohVersions = []

        if (not os.path.exists(self.__metadataFile) or os.stat(self.__metadataFile).st_size == 0):
            self.createMetadataFile()

        #read data from json file
        a = self.getJson()
        self.__sohDir = a[self.__sohDirName]
        self.__romDir = a[self.__romDirName]
        self.__default = a[self.__sohVersionDefaultName]
        self.__sohVersions = a[self.__sohVersionsName]    

    #add more here
    #@classmethod

    ########################################################################################
    #set class variables
    #afterwards should set the json equivalent
    def setSohDir(self, path):
        
        lpath = os.path.normcase(path)

        if (os.path.isdir(lpath)):
            self.__sohDir = lpath
            self.updateJson(self.__sohDirName, lpath)

    def setRomDir(self, path):
        
        lpath = os.path.normcase(path)

        if (os.path.isdir(lpath)):
            self.__romDir = lpath 
            self.updateJson(self.__romDirName, lpath)

    def setSohVersions(self):
        
        mVersions = self.getVersionsSOHPath(self.__sohDir)
         #loop for adding SOH Version metadata
        for version in mVersions:

                #check if version is already in the dictionary before adding it again
                if (version not in self.__sohVersions):
                    #could use this when SOH supports arguments
                    #p = subprocess.Popen(["python", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                    #when adding custom/older versions of SOH that don't support arguments
                    self.__sohVersions.update({version : {
                        self.__sohVersionNumberName : "unknown",
                        self.__sohVersionName : version,
                        self.__sohVersionPathName : os.path.join(self.__sohDir, version)
                    }})
        
        removeVersions = []
        #remove Versions that are not or no longer in the SOH folder
        for version in self.__sohVersions:

            if (version not in mVersions):
                removeVersions.append(version)

        for version in removeVersions:
            self.__sohVersions.pop(version)

        self.updateJson(self.__sohVersionsName, self.__sohVersions)

    def setDefaultVersion(self, version):
            
        #check if version to update is in dictionary
        if (version in self.__sohVersions):
            self.__default = version
            self.updateJson(self.__sohVersionDefaultName, self.__default)
            return
        else:
            raise TypeError("Version not found")
    
    #get local variables
    def getSohDir(self):
        return self.__sohDir

    def getRomDir(self):
        return self.__romDir

    def getSohVersions(self):
        return self.__sohVersions
    
    def getDefault(self):
        return self.__default
    
    def getDefaultSohVersion(self):

        return self.__sohVersions[self.__default]
            
    def getPathofSohVersion(self, version):
        
        if version in self.__sohVersions:
            return self.__sohVersions[version][self.__sohVersionPathName]

        return None
    
    #get jsonNames
    def getJsonSOHDirName(self):
        return self.__sohDirName
    
    def getJsonRomDirName(self):
        return self.__romDirName
        
    def getJsonSOHVersionsName(self):
        return self.__sohVersionsName
        
    def getJsonSOHVersionNumberName(self):
        self.__sohVersionNumberName
        
    def getJsonSOHVersionName(self):
        self.__sohVersionName
        
    def getJsonSohVersionPathName(self):
        return self.__sohVersionPathName
    
    def getJsonSohVersionDefaultName(self):
        return self.__sohVersionDefaultName

    ########################################################################################
    #json Manipulation
    def createMetadataFile(self):

        #load data for json
        data = {
            self.__sohDirName : self.__sohDir,
            self.__romDirName : self.__romDir,
            self.__sohVersionDefaultName : self.__default,
            self.__sohVersionsName : {}
        }

        with open(self.__metadataFile, "w+") as jsonFile:
            json.dump(data, jsonFile, indent = self.__ind)

    #this can be called from outside the class to allow for external data to be saved to the file
    #careful with this, it overwrites the data in the metadata file for the given field
    def updateJson(self, name, data):

        jsonData = self.getJson()

        jsonData[name] = data 
        
        with open(self.__metadataFile, "w+") as jsonFile:

            json.dump(jsonData, jsonFile, indent = self.__ind)

    #Get JSON data
    def getJson(self):
        
        with open(self.__metadataFile, "r") as jsonFile:
            jsonData = json.load(jsonFile)

        return jsonData
    
    #if you need specific json data instead of the whole file
    def getSpecificJsonData(self, name):
        
        with open(self.__metadataFile, "r") as jsonFile:
            jsonData = json.load(jsonFile[name])

        return jsonData
    
    ########################################################################################
    #file system access
    def runSOH(self, path, localDir):

        os.chdir(path)

        #need help testing on other platforms 
        match platform.system():
            case "Darwin":
                subprocess.Popen(
                    os.path.join(path, 'soh.exe'),
                    stdout = subprocess.DEVNULL,
                    stderr = subprocess.DEVNULL
                )
            case "Linux":
                subprocess.Popen(
                    os.path.join(path,'soh.appimage'), 
                    stdout = subprocess.DEVNULL,
                    stderr = subprocess.DEVNULL
                )
            case "Windows":
                subprocess.Popen(
                    os.path.join(path, 'soh.exe'),
                    stdout = subprocess.DEVNULL,
                    stderr = subprocess.DEVNULL
                )
        os.chdir(localDir)

    def getVersionsSOHPath(self, path):
        files_dir = [
            f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))
        ]
        return files_dir
    
    def listVersions(self, versions: list):

        default = self.getDefaultSohVersion()[self.__sohVersionName]

        print('\nDefault\n' + default + '\n---------------------------\n')
        for version in versions:
            if (versions[version][self.__sohVersionDefaultName] == 0):
                print(version)
        print()

    def copyData(self, fr, to, data):
        
        fromPath = os.path.join(self.getPathofSohVersion(fr), data)
        toPath = os.path.join(self.getPathofSohVersion(to), data)

        if(os.path.isfile(fromPath)):
            shutil.copy2(fromPath, toPath)

        if(os.path.isdir(fromPath)):
            shutil.copytree(fromPath, toPath, dirs_exist_ok=True)

    ########################################################################################
    #symlink rom files
    def symlinkRom(self, path):

        for rom in os.listdir(self.__romDir):
            if(os.path.isfile(os.path.join(self.__romDir,rom))):
                os.symlink(rom, os.path.join(path, rom))