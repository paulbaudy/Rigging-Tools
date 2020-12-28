import maya.cmds as cmds
import IKHandles
import view
import settings
import json
import locators

locators = reload(locators)
IKHandles = reload(IKHandles)
view = reload(view)
settings = reload(settings)

#UI = view.RTKView()
UI2 = view.View()
settings.init()

ikHandler = IKHandles.IkHandler()
       
 
def ImportRig():
    basicFilter = "*.json"
    file = cmds.fileDialog2(fileFilter=basicFilter, dialogStyle=1)
   
    with open(file[0], 'r') as json_file:
        data = json.load(json_file)
        
        if cmds.objExists('Loc_Master'):
           print '[Error] base locator already exists'
        else:
           cmds.group(em = True, name = 'RT_Master')
        
        root = cmds.spaceLocator(n = 'RT_Root')
        cmds.move(0, 1.5, 0, root)
        cmds.scale(0.1, 0.1, 0.1, root)
        cmds.parent(root, 'RT_Master')
    
        CreateLocators(data['Locators'])
    
def CreateLocators(LocatorsData):
    for LocatorData in LocatorsData:
        CreateLocator(LocatorData)
    
def CreateLocator(LocatorData, parent = False):
    Locator = cmds.spaceLocator(n = LocatorData['name'])
    cmds.scale(0.1, 0.1, 0.1, Locator)
    if parent:
        cmds.parent(Locator, parent)
    elif 'parent' in LocatorData:
        cmds.parent(Locator, LocatorData['parent'])
    else:
        print 'no parent'
        cmds.parent(Locator, 'RT_Root')
 
    if 'x' in LocatorData and 'y' in LocatorData and 'z' in LocatorData:
        cmds.move(LocatorData['x'], LocatorData['y'], LocatorData['z'], Locator)
        
    if 'child' in LocatorData:
        print 'create child'
        CreateLocator(LocatorData['child'], Locator)
    

    
        