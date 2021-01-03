import maya.cmds as cmds

class Settings():
    def __init__(self, Data = dict()):
         for key in Data:
            setattr(self, key, Data[key])
            print str(key) + ' ' + str(Data[key])
            
         
inst = Settings()