import configparser
class ConfigLoader:
    def __init__(self):
        self.configParser = configparser.RawConfigParser()   
        configFilePath = r'config.ini'
        self.configParser.read(configFilePath)
        
    def getUrl(self):
        return self.configParser.get("wordquiz","url")
    def getChromeDriverPath(self):
        return self.configParser.get("selenium","chromedriverpath")
