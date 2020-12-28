import maya.cmds as cmds
import IKHandles
import locators
import joints
import json
import settings

locators = reload(locators)
joints = reload(joints)
IKHandles = reload(IKHandles)
ikHandler = IKHandles.IkHandler()


class View():      
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
        
    def ApplySettings(self):
        settings.RootHeight = float(cmds.textField('rootHeightLineEdit', query=True, text=True))
        settings.SpineCount = int(cmds.textField('spineCountLineEdit', query = True, text = True))
        settings.SpineOffset = float(cmds.textField('spineOffsetLineEdit', query = True, text = True))
        settings.SpineBaseHeight = float(cmds.textField('spineBaseHeightLineEdit', query = True, text = True))
        settings.FingersCount = int(cmds.textField('fingersCountLineEdit', query = True, text = True))
        settings.PhalanxCount = int(cmds.textField('phalanxCountLineEdit', query = True, text = True))
        settings.PhalanxOffset = float(cmds.textField('phalanxOffsetLineEdit', query = True, text = True))
        settings.LegsOffset = float(cmds.textField('legsOffsetLineEdit', query = True, text = True))
        settings.Scale = float(cmds.textField('scaleLineEdit', query = True, text = True))
        
        ## GLOBAL SETTINGS
        settings.LocatorsGrp = cmds.textField('locatorsGroupNameLineEdit', query = True, text = True)
       
    def G_ImportConfig(self, Button):
        jsonFilter = "*.json"
        file = cmds.fileDialog2(fileFilter=jsonFilter, dialogStyle=1)
        
        with open(file[0], 'r') as json_file:
            data = json.load(json_file)
            ikHandler.importConfig(data)
            
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
        
        
    def __init__(self):
        dialog = cmds.loadUI(uiFile='C:/Users/paulb/Documents/maya/2020/scripts/main.ui')
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
        self.ApplySettings()

class RTKView():
    
    def BuildJoints(self, void):
       self.applySettings()
       joints.AutoBuildJoints()
        
    def OrientJoints(self, void):
        joints.OrientJoints()
        
    def applySettings(self):
        settings.RootHeight = cmds.floatField(self.RootHeightField, query = True, value = True)
        settings.SpineCount = cmds.intField(self.SpineCountField, query = True, value = True)
       
        settings.Legs = cmds.intField(self.LegsField, query = True, value = True)
        settings.SpineBaseHeight = cmds.floatField(self.SpineBaseHeight, query = True, value = True)
        settings.SpineOffset = cmds.floatField(self.SpineOffset, query = True, value = True)
        settings.Arms = cmds.intField(self.ArmsField, query = True, value = True)

        settings.FingersCount = cmds.intField(self.FingersField, query = True, value = True)
        settings.PhalanxCount = cmds.intField(self.PhalanxCountField, query = True, value = True)
        settings.PhalanxOffset = cmds.floatField(self.PhalanxOffsetField, query = True, value = True)
    
    def BuildLocators(self, void):
       self.applySettings()
       locators.BuildLocators()
       
    def MirrorLocators(self, void):
        locators.MirrorLocators()
        
    
    def __init__(self):
        cmds.window('Rigging tools')
        cmds.rowColumnLayout(nc = 2)
        
        # Show actions
        cmds.button(l = 'Build locators', w = 100, c = self.BuildLocators)
        cmds.button(l = 'Mirror Locators', w = 100, c = self.MirrorLocators)
        cmds.button(l = 'Import Rig', w = 100, c = 'ImportRig()')
        cmds.button(l = 'Export Rig', w = 100, c = 'ExportRig()')
        cmds.button(l = 'Delete All', w = 100, c = 'Clear()')
        cmds.button(l = 'Build Rig Joints', w = 100, c = 'BuildJoints()')
        cmds.button(l = 'Generate Joints', w = 100, c = self.BuildJoints)
        cmds.button(l = 'Orient Joints', w = 100, c = self.OrientJoints)
        

        cmds.separator(st = 'none')
        cmds.separator(st = 'none')
        
        # Show settings
        cmds.text(l = 'Root Height')
        self.RootHeightField = cmds.floatField(value = 1.5)
        cmds.text(l = 'Spine Count')
        self.SpineCountField = cmds.intField(minValue = 1, maxValue = 4, value = 4)
        cmds.text(l = 'Legs Count')
        self.LegsField = cmds.intField(minValue = 1, maxValue = 5, value = 2)
        cmds.text(l = 'Spine Base Height')
        self.SpineBaseHeight = cmds.floatField(value = 1.75)
        cmds.text(l = 'Spine Offset')
        self.SpineOffset = cmds.floatField(value = 0.25)
        cmds.text(l = 'Arms per Side')
        self.ArmsField = cmds.intField(minValue = 1, maxValue = 5, value = 1)

        cmds.text(l = 'Fingers Count')
        self.FingersField = cmds.intField(minValue = 1, maxValue = 5, value = 5)
        cmds.text(l = 'Phalanx Count')
        self.PhalanxCountField = cmds.intField(minValue = 1, maxValue = 5, value = 5)
        cmds.text(l = 'Phalanx Offset')
        self.PhalanxOffsetField = cmds.floatField(value = 5)
        
        
        cmds.showWindow()
        