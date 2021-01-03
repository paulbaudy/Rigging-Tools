import maya.cmds as cmds
import settings

def AutoBuildJoints():
    if cmds.objExists(settings.inst.RigName):
        cmds.delete(settings.inst.RigName)
        
    root = cmds.ls(settings.inst.RootName)
    if root:
        RigGrp = cmds.group(em = True, name = settings.inst.RigName)
        rootLoc = cmds.xform(root, q = True, t = True, ws = True)
        rootJoint = cmds.joint(radius = 0.1, p = rootLoc, name = settings.inst.RigRootName)
        buildJointHierarchy(root, rootJoint)
    else:
        cmds.confirmDialog(title='No locators', message='You need to build locators first')
        
def OrientJoints():
    if not cmds.ls(settings.inst.RootName):
        cmds.confirmDialog(title='No locators', message='You need to build locators first')
        return
        
    cmds.select(settings.inst.RigRootName)
    cmds.joint(e = True, ch = True, oj = 'xyz')
        
def buildJointHierarchy(rootLocator, rootJoint):
    childs = cmds.listRelatives(rootLocator)
    locators = cmds.ls(type=('locator'), l=True) or []
    for child in childs:
       
       if 'Shape' not in child and 'Grp' not in child:
          BuildJoint(child, rootLocator, rootJoint)
          
       if 'Grp' in child:
          buildJointHierarchy(child, rootJoint)
        
        
def BuildJoint(locator, parentLocator, parentJoint):
    cmds.select(deselect = True)
    cmds.select(parentJoint)
    JointLocation = cmds.xform(locator, q = True, t = True, ws = True)
    Joint = cmds.joint(radius = 0.1, p = JointLocation, name = locator + 'J')
    buildJointHierarchy(locator, Joint)
    
     