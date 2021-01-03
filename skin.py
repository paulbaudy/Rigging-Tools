import maya.cmds as cmds
import settings

def getSkinningMethod():
    return cmds.optionMenu('skinMethodBox', query=True, select=True)

def BindSkin():
    selection = cmds.ls(sl = True)
    
    if len(selection) > 0:
        cmds.skinCluster(selection[0], settings.inst.RigRootName, bm = settings.inst.BindMethod, sm = getSkinningMethod(), dr = settings.inst.DropOffRate)
        cmds.geomBind('skinCluster1', bm = settings.inst.BindMethod, gvp = [settings.inst.GeodesicRes, 1])
        
    else:
        cmds.confirmDialog(title='No mesh selected', message='You need to have a mesh selected.')
        
        
        
   
        