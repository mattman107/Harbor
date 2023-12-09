import requests

class sohReleaseHandler:
    def __init__(self):
        self.__sohGithubVersionsName = "GitHub Versions"

        self.__sohGithubVersions = {}

        self.setSohGithubVersions()

    def setSohGithubVersions(self):

        url = 'https://api.github.com/repos/HarbourMasters/Shipwright/releases'
        
        #github json variableNames
        sohGithubVersionName = "name"
        sohGithubAssetsName = "assets"
        sohGithubDownloadName = "browser_download_url"
        sohGithubCreateDateName = "created_at"

        #my json variableNames
        sohDownloadLinkName = "downloadLink"
        sohDateName = "date"

        # sending an HTTP request using request module
        r = requests.get(url)

        data = r.json()

        d = {}
        #stupid nested loops to fix the requests.json() data
        for jsonData in data:
            for key in jsonData:
                    if(key == sohGithubVersionName):
                        d.update({jsonData[key]: {}})
                        for assets in jsonData[sohGithubAssetsName]:
                            for key1 in assets:
                                if (key1 == sohGithubVersionName):
                                    d[jsonData[key]].update({ assets[key1] : {
                                            sohDownloadLinkName : assets[sohGithubDownloadName],
                                            sohDateName : assets[sohGithubCreateDateName]
                                    }})

        self.__sohGithubVersions = d

    #returning both if it needs to be saved to the JSON file
    #for now I don't think this specific data needs to be saved to metadata file but change my mind :)
    #I think it would be best to keep this in RAM and refresh it on startup or if the user requests
    def getSohGithubVersionsJson(self):
        return [self.__sohGithubVersionsName, self.__sohGithubVersions]