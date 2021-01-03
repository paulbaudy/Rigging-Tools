import maya.cmds as cmds
import controller
import IKHandles
import locators
import joints
import json
import settings
import skin
import os
import os.path

controller = reload(controller)
locators = reload(locators)
joints = reload(joints)
IKHandles = reload(IKHandles)
skin = reload(skin)
settings = reload(settings)
ikHandler = IKHandles.IkHandler()

class View():
    def __init__(self):
        dialog = cmds.loadUI(uiFile=self.searchInEnv('main.ui'))
        cmds.showWindow(dialog)
        
        # Bind buttons
        cmds.button('G_ImportButton', edit=True, command=self.G_ImportConfig)
        cmds.button('G_ExportButton', edit=True, command=self.G_ExportConfig)
        cmds.button('L_BuildLocators', edit=True, command=self.L_BuildLocatorss)
        cmds.button('L_MirrorLocators', edit=True, command=self.L_MirrorLocators)
        cmds.button('J_GenerateJoints', edit=True, command=self.J_BuildJoints)
        cmds.button('J_OrientJoints', edit=True, command=self.J_OrientJoints)
        cmds.button('IK_FromJoint', edit=True, command=self.IK_SelectFromJoint)
        cmds.button('IK_ToJoint', edit=True, command=self.IK_ToJoint)
        cmds.button('IK_BuildHandles', edit=True, command=self.IK_BuildHandles)
        cmds.button('S_BinSkinButton', edit=True, command=self.S_BinSkin)
        cmds.button('C_BuildControllers', edit=True, command=self.C_BuildControllers)
        
        # Import default settings
        self.importConfigFile(self.searchInEnv('config.json'))
        self.ApplySettings()
        
    def J_BuildJoints(self, void):
        self.ApplySettings()
        joints.AutoBuildJoints()
        
    def J_OrientJoints(self, void):
        joints.OrientJoints()
        
    def L_MirrorLocators(self, Button):
        locators.MirrorLocators()
    
    def L_BuildLocatorss(self, Button):
        self.ApplySettings()
        locators.BuildLocators()
        
    def SetTextFieldValue(self, field, value):
        cmds.textField(field, edit=True, text = str(value))
        
        
    def ApplySettings(self):
        # Locators settings
        settings.inst.RootHeight = float(cmds.textField('rootHeightLineEdit', query=True, text=True))
        settings.inst.SpineCount = int(cmds.textField('spineCountLineEdit', query = True, text = True))
        settings.inst.SpineOffset = float(cmds.textField('spineOffsetLineEdit', query = True, text = True))
        settings.inst.SpineBaseHeight = float(cmds.textField('spineBaseHeightLineEdit', query = True, text = True))
        settings.inst.FingersCount = int(cmds.textField('fingersCountLineEdit', query = True, text = True))
        settings.inst.PhalanxCount = int(cmds.textField('phalanxCountLineEdit', query = True, text = True))
        settings.inst.PhalanxOffset = float(cmds.textField('phalanxOffsetLineEdit', query = True, text = True))
        settings.inst.LegsOffset = float(cmds.textField('legsOffsetLineEdit', query = True, text = True))
        settings.inst.Scale = float(cmds.textField('scaleLineEdit', query = True, text = True))
        
        # Joints settings
        settings.inst.RigRootName = cmds.textField('rigRootNameLineEdit', query = True, text = True)
        
        ## GLOBAL SETTINGS
        settings.inst.LocatorsGrp = cmds.textField('locatorsGroupNameLineEdit', query = True, text = True)
        
    def refreshUISettings(self):
        # Locators settings
        self.SetTextFieldValue('rootHeightLineEdit', settings.inst.RootHeight)
        self.SetTextFieldValue('spineCountLineEdit', settings.inst.SpineCount)
        self.SetTextFieldValue('spineOffsetLineEdit', settings.inst.SpineOffset)
        self.SetTextFieldValue('spineBaseHeightLineEdit', settings.inst.SpineBaseHeight)
        self.SetTextFieldValue('fingersCountLineEdit', settings.inst.FingersCount)
        self.SetTextFieldValue('phalanxCountLineEdit', settings.inst.PhalanxCount)
        self.SetTextFieldValue('phalanxOffsetLineEdit', settings.inst.PhalanxSideOffset)
        self.SetTextFieldValue('legsOffsetLineEdit', settings.inst.LegsSideOffset)
        self.SetTextFieldValue('scaleLineEdit', settings.inst.Scale)
                
        # Joints settings
        self.SetTextFieldValue('rigRootNameLineEdit', settings.inst.RigRootName)     
        
    def importConfigFile(self, filePath):
        if os.path.isfile(filePath):
            with open(filePath, 'r') as json_file:
                data = json.load(json_file)
                settings.inst = settings.Settings(data)
                self.refreshUISettings()
                ikHandler.importConfig(data)
                 
    def G_ImportConfig(self, Button):
        jsonFilter = "*.json"
        file = cmds.fileDialog2(fileFilter=jsonFilter, dialogStyle=1)
        if file:
            self.importConfigFile(file[0])
            
    def G_ExportConfig(self, Button):
        jsonFilter = "*.json"
        file = cmds.fileDialog2(fileFilter=jsonFilter, dialogStyle=1)
        
        with open(file[0], 'r') as json_file:
            data = json.load(json_file)
            ikHandler.importConfig(data)
            
    def IK_SelectFromJoint(self, Button):
        selected = cmds.ls(sl=True,long=False, type = 'joint') or []
        cmds.textField('FromJointlineEdit', edit=True, tx = str(selected))
        
    def IK_ToJoint(self, Button):
        selected = cmds.ls(sl=True,long=False, type = 'joint') or []
        cmds.textField('ToJointlineEdit', edit=True, tx = str(selected))
        
    def IK_BuildHandles(self, Button):
        ikHandler.buildHandlers()
        
    def S_BinSkin(self, Button):
        skin.BindSkin()
        
    def C_BuildControllers(self, Button):
        controller.BuildControllers(settings.inst.Ctrl)
         
    def searchInEnv(self, fileName):
        script_paths = os.getenv('MAYA_SCRIPT_PATH')
        if script_paths:
            paths = script_paths.split(';')
            for path in paths:
                file_path = path + '/' + fileName
                if os.path.isfile(file_path):
                    return file_path
                    
        return ''
                