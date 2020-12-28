import maya.cmds as cmds
import settings

def BuildLocators():
    if cmds.objExists(settings.LocatorsGrp):
        cmds.delete(settings.LocatorsGrp)
   
    cmds.group(em = True, name = settings.LocatorsGrp)
    root = cmds.spaceLocator(n = 'RT_Root')
    cmds.move(0, settings.RootHeight, 0, root)
    sc = settings.Scale
    cmds.scale(sc, sc, sc, root)
    cmds.parent(root, settings.LocatorsGrp)
   
    BuildSpines()
    BuildArm(-1)
    BuildArm(1)
    BuildLegs(1)
    BuildLegs(-1)
    
def MirrorLocators():
    selection = cmds.ls(sl=True,long=False) or []
    if selection:
        Locator = selection[0]
        TargetLocator = Locator.replace('_R_', '_L_')
        
        SourceLocation = cmds.xform(Locator, q = True, t = True, ws = True)
        cmds.move(-SourceLocation[0], SourceLocation[1], SourceLocation[2], TargetLocator)
       

def BuildSpines():
    print 'Enter Build Spines function'
    
    print settings.SpineCount
    for index in range(0, settings.SpineCount):
        Spine = cmds.spaceLocator(n = 'RT_Spine_' + str(index))
        
        if index == 0:
            cmds.parent(Spine, 'RT_Root', relative = True)
        else:
            cmds.parent(Spine, 'RT_Spine_' + str(index - 1), relative = True)
            
        
        cmds.move(0, settings.SpineOffset, 0, Spine, r = True)
            
        
def BuildArm(Side):
    SpineLocator = 'RT_Spine_' + str(settings.SpineCount - 1) 
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
    cmds.move(0.35 * Side, 0, 0, arm, r = True)
    cmds.move(0.1 * Side, -0.5, -0.2, elbow, r = True)
    cmds.move(0, -0.5, 0.2, wrist, r = True)
    
    # HANDS
    CreateHands(Side, wrist)
    
def BuildLegs(Side):
    SideChar = 'L' if Side == 1 else 'R'
    LegGrpName = SideChar + '_LegGrp'
        
    # UPPER LEG
    upperLegGRP = cmds.group(em = True, name = LegGrpName)
    cmds.parent(upperLegGRP, 'RT_Root', relative = True)
    cmds.move(Side * 0.15, 0, 0, upperLegGRP, r = True)
        
    upperLeg = cmds.spaceLocator(n = SideChar + '_UpperLeg')
    cmds.parent(upperLeg, LegGrpName, relative = True)
    cmds.move(0, 0, 0, upperLeg, r = True)
        
    # lower leg
    lowerLeg = cmds.spaceLocator(n = SideChar + '_LowerLeg')
    cmds.parent(lowerLeg, SideChar + '_UpperLeg', relative = True)
    cmds.move(0, -0.6, 0, lowerLeg, r = True)
        
    # foot
    foot = cmds.spaceLocator(n = SideChar + '_Foot')
    cmds.parent(foot, SideChar + '_LowerLeg', relative = True)
    cmds.move(0, -0.7, 0, foot, r = True)
        
        
    # football
    football = cmds.spaceLocator(n = SideChar + '_FootBall')
    cmds.parent(football, SideChar + '_Foot', relative = True)
    cmds.move(0, -0.2, 0.1, football, r = True)
        
    # toes
    toes = cmds.spaceLocator(n = SideChar + '_Toes')
    cmds.parent(toes, SideChar + '_FootBall', relative = True)
    cmds.move(0, 0, 0.2, toes, r = True)
        
def CreateHands(Side, Root):
    SideChar = 'L' if Side == 1 else 'R'
    
    hand = cmds.group(em = True, name = SideChar + '_HandGrp')
    pos = cmds.xform(Root, q=True, t = True, ws = True)
    cmds.move(pos[0], pos[1], pos[2], hand)
    cmds.parent(hand, SideChar + '_Wrist')
    
    for index in range(0, settings.FingersCount):
        BuildFingers(Side, pos, index)
  
def BuildFingers(Side, RootLocation, Count):
    SideChar = 'L' if Side == 1 else 'R'
    
    for index in range(0, 3):
        finger = cmds.spaceLocator(n = SideChar + '_Finger_' + str(Count) + '_' + str(index))
        cmds.scale(0.05, 0.05, 0.05, finger)
        
        if index == 0:
            cmds.parent(finger, SideChar + '_HandGrp')
        else:
            cmds.parent(finger, SideChar + '_Finger_' + str(Count) + '_' + str(index - 1))
        
        cmds.move(RootLocation[0] + Side * (0.1 + (0.1 * index)), RootLocation[1] - (0.1 + (0.1 * index)), RootLocation[2] - (0.05 * Count), finger)
    