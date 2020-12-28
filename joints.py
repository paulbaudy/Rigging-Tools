import maya.cmds as cmds
import settings

def AutoBuildJoints():
    if cmds.objExists('BaseJointRig'):
        cmds.delete('BaseJointRig')
        
    RigGrp = cmds.group(em = True, name = 'BaseJointRig')
        
    root = cmds.ls('RT_Root')
    rootLoc = cmds.xform(root, q = True, t = True, ws = True)
    rootJoint = cmds.joint(radius = 0.1, p = rootLoc, name = 'RT_Rig_Root')
        
    BuildJointRename(root, rootJoint)
        
def OrientJoints():
    cmds.select('RT_Rig_Root')
    cmds.joint(e = True, ch = True, oj = 'xyz')
        
def BuildJointRename(rootLocator, rootJoint):
    childs = cmds.listRelatives(rootLocator)
    locators = cmds.ls(type=('locator'), l=True) or []
    for child in childs:
       print cmds.objectType(child)
       if 'Shape' not in child and 'Grp' not in child:
          BuildJoint(child, rootLocator, rootJoint)
          print child
          
       if 'Grp' in child:
           BuildJointRename(child, rootJoint)
        
        
def BuildJoint(locator, parentLocator, parentJoint):
    cmds.select(deselect = True)
    cmds.select(parentJoint)
    JointLocation = cmds.xform(locator, q = True, t = True, ws = True)
    Joint = cmds.joint(radius = 0.1, p = JointLocation, name = locator + 'J')
    BuildJointRename(locator, Joint)
    
     
def BuildJoints():
    print 'Enter Build Joints function'
    
    if not cmds.objExists('BaseJointRig'):
        RigGrp = cmds.group(em = True, name = 'BaseJointRig')
        
        root = cmds.ls('RT_Root')
        
        Spines = cmds.ls('RT_Spine_*', type='locator')
        spine = cmds.listRelatives(*Spines, p = True, f = True)
        
        rootLoc = cmds.xform(root, q = True, t = True, ws = True)
        rootJoint = cmds.joint(radius = 0.1, p = rootLoc, name = 'RT_Rig_Root')
        
        cmds.parent(rootJoint, w = True, a = True)
        cmds.parent(rootJoint, 'BaseJointRig', a = True)
    
        for Index, Spine in enumerate(spine):
            Loc = cmds.xform(Spine, q = True, t = True, ws = True)
            SpineJoint = cmds.joint(radius = 0.08, p = Loc, name = 'RT_Rig_Spine_' + str(Index))
            
        Sides = ['L', 'R']
        SpineValue = cmds.intField(SpineField, query = True, value = True) - 1
        SpineJoint = 'RT_Rig_Spine_' + str(SpineValue)
    
        for Side in Sides:
            cmds.select(deselect = True)
            cmds.select(SpineJoint)
            
            UpperArm = cmds.ls('RT_' + Side + '_UpperArm')
            UpperArmPos = cmds.xform(UpperArm, q = True, t = True, ws = True)
            UpperArmJoint = cmds.joint(radius = 0.1, p = UpperArmPos, name = 'RT_Rig_' + Side + '_UpperArm')
            
            Elbow = cmds.ls('RT_' + Side + '_Elbow')
            ElbowPos = cmds.xform(Elbow, q = True, t = True, ws = True)
            ElbowLoc = cmds.joint(radius = 0.1, p = ElbowPos, name = 'RT_Rig_' + Side + '_Elbow')
            
            Wrist = cmds.ls('RT_' + Side + '_Wrist')
            WristPos = cmds.xform(Wrist, q = True, t = True, ws = True)
            WristLoc = cmds.joint(radius = 0.1, p = WristPos, name = 'RT_Rig_' + Side + '_Wrist')