import maya.cmds as cmds

def BuildController(data):
    target_ik = data.get('TargetIK')
    if target_ik:
        ctrl = cmds.circle(nr = (0,1,0), c = (0,0,0), radius = 0.2, degree = 1, s = 16, name = data.get('Name'))
        location = cmds.xform(data.get('TargetIK'), q=True, t = True, ws = True)
        cmds.move(location[0], location[1], location[2], ctrl)
        cmds.pointConstraint(ctrl, data.get('TargetIK'), mo = False)
        cmds.orientConstraint(ctrl, data.get('Orient'), mo = True)
    
def BuildControllers(data):
    for ctrlData in data:
        BuildController(ctrlData)