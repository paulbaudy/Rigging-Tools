import maya.cmds as cmds
import settings
import re

settings = reload(settings)

def BuildLocators():
    if cmds.objExists(settings.inst.LocatorsGrp):
        cmds.delete(settings.inst.LocatorsGrp)
   
    cmds.group(em = True, name = settings.inst.LocatorsGrp)
    root = cmds.spaceLocator(n = settings.inst.RootName)
    cmds.move(0, settings.inst.RootHeight, 0, root)
    sc = settings.inst.Scale
    cmds.scale(sc, sc, sc, root)
    cmds.parent(root, settings.inst.LocatorsGrp)
   
    BuildSpines()
    BuildArm(-1)
    BuildArm(1)
    BuildLegs(1)
    BuildLegs(-1)
    BuildNeck()
    
def MirrorLocators():
    selection = cmds.ls(sl=True,long=False) or []
    rep = {"L_": "R_", "R_": "L_"}
    if selection:
        Locator = selection[0]
        SourceLocation = cmds.xform(Locator, q = True, t = True, ws = True)
        rep = dict((re.escape(k), v) for k, v in rep.iteritems()) 
        pattern = re.compile("|".join(rep.keys()))
        Locator = pattern.sub(lambda m: rep[re.escape(m.group(0))], Locator)
        cmds.move(-SourceLocation[0], SourceLocation[1], SourceLocation[2], Locator)
        
def getSpineName(index):
    return settings.inst.SpineName + '_' + str(index)
    
def BuildNeck():
    neck = cmds.spaceLocator(n = settings.inst.NeckName)
    cmds.parent(neck, getSpineName(settings.inst.SpineCount - 1), r = True)
    cmds.move(0, settings.inst.NeckHeight, 0, r = True)
       
def BuildSpines():
    for index in range(0, settings.inst.SpineCount):
        Spine = cmds.spaceLocator(n = getSpineName(index))
        
        if index == 0:
            cmds.parent(Spine, settings.inst.RootName, r = True)
        else:
            cmds.parent(Spine, getSpineName(index - 1), r = True)
            
        
        cmds.move(0, settings.inst.SpineOffset, 0, Spine, r = True)
            
        
def BuildArm(Side):
    SpineLocator = getSpineName(settings.inst.SpineCount - 1) 
    SideChar = 'L' if Side == 1 else 'R'
    
    # ARM GROUP
    arm = cmds.group(em = True, name = SideChar + '_ArmGrp')
    cmds.parent(arm, SpineLocator, relative=True)
            
    # UPPER ARM
    upperArm = cmds.spaceLocator(n = SideChar + '_UpperArm')
    cmds.parent(upperArm, arm, relative=True)
            
    # ELBOW
    elbow = cmds.spaceLocator(n = SideChar + '_Elbow')
    cmds.parent(elbow, upperArm, relative=True)
            
    # WRIST
    wrist = cmds.spaceLocator(n = SideChar + '_Wrist')
    cmds.parent(wrist, elbow, relative=True)
              
    # Offset locators to default values
    cmds.move(settings.inst.ArmSideOffset * Side, 0, 0, arm, r = True)
    cmds.move(settings.inst.ElbowSideOffset * Side, -settings.inst.ElbowHeight, -0.2, elbow, r = True)
    cmds.move(0, -settings.inst.ElbowHeight, 0.2, wrist, r = True)
    
    # HANDS
    CreateHands(Side, wrist)
    
def BuildLegs(Side):
    SideChar = 'L' if Side == 1 else 'R'
    LegGrpName = SideChar + '_LegGrp'
        
    # UPPER LEG
    upperLegGRP = cmds.group(em = True, name = LegGrpName)
    cmds.parent(upperLegGRP, settings.inst.RootName, relative = True)
    cmds.move(Side * settings.inst.LegsSideOffset, 0, 0, upperLegGRP, r = True)
        
    upperLeg = cmds.spaceLocator(n = SideChar + '_UpperLeg')
    cmds.parent(upperLeg, LegGrpName, relative = True)
    cmds.move(0, 0, 0, upperLeg, r = True)
        
    # lower leg
    lowerLeg = cmds.spaceLocator(n = SideChar + '_LowerLeg')
    cmds.parent(lowerLeg, SideChar + '_UpperLeg', relative = True)
    cmds.move(0, -settings.inst.LegsHeight, 0, lowerLeg, r = True)
        
    # foot
    foot = cmds.spaceLocator(n = SideChar + '_Foot')
    cmds.parent(foot, SideChar + '_LowerLeg', relative = True)
    cmds.move(0, -settings.inst.LegsHeight, 0, foot, r = True)
        
    # football
    football = cmds.spaceLocator(n = SideChar + '_FootBall')
    cmds.parent(football, SideChar + '_Foot', relative = True)
    cmds.move(0, -settings.inst.FootballOffset, 0, football, r = True)
        
    # toes
    toes = cmds.spaceLocator(n = SideChar + '_Toes')
    cmds.parent(toes, SideChar + '_FootBall', r = True)
    cmds.move(0, 0, settings.inst.ToesLength, toes, r = True)
        
def CreateHands(Side, Root):
    SideChar = 'L' if Side == 1 else 'R'
    
    hand = cmds.group(em = True, name = SideChar + '_HandGrp')
    pos = cmds.xform(Root, q=True, t = True, ws = True)
    cmds.parent(hand, SideChar + '_Wrist', r = True)
    
    for index in range(0, settings.inst.FingersCount):
        BuildFingers(Side, pos, index)
  
def BuildFingers(Side, RootLocation, Count):
    SideChar = 'L' if Side == 1 else 'R'
    
    for index in range(0, settings.inst.PhalanxCount):
        finger = cmds.spaceLocator(n = SideChar + '_Finger_' + str(Count) + '_' + str(index))
        
        z = - settings.inst.FingerSpacing * Count
        if index == 0:
            cmds.parent(finger, SideChar + '_HandGrp', r = True)
        else:
            cmds.parent(finger, SideChar + '_Finger_' + str(Count) + '_' + str(index - 1), r = True)
            z = 0
            
        sideOffset = settings.inst.PhalanxSideOffset 
        cmds.move(Side * sideOffset, -sideOffset, z, finger, r = True)
    