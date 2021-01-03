import maya.cmds as cmds

# Wrapper class that holds data on a IK handle
class IkHandle():
    def __init__(self):
        self.name = 'None'
        self.solverType = 'None'
        self.sourceJoint = 'None'
        self.endJoint = 'None'
        self.degree = 'None'
        
    def __init__(self, Data):
        self.name = Data.get('Name')
        self.solverType = Data.get('Solver')
        self.sourceJoint = Data.get('SourceJoint')
        self.endJoint = Data.get('EndJoint')
        self.degree = Data.get('Degree')
        
    def toStr(self):
        return self.solverType + ' ' + self.sourceJoint + ' ' + self.endJoint
                
    def buildHandler(self):
        if self.solverType == 'ikSplineSolver':
            # Special case for spine solvers 
            rootJoint = cmds.ls(self.sourceJoint, type = 'joint')
            rootPosition = cmds.xform(rootJoint, q = True, t = True, ws = True)
            endJoint = cmds.ls(self.endJoint, type = 'joint')
            
            parentJoint = endJoint
            positions = []
             
            # list all joint locations from effector to parent
            while parentJoint != rootJoint and parentJoint:
                position = cmds.xform(parentJoint, q = True, t = True, ws = True)
                positions.append(position)
                parentJoint = cmds.listRelatives(parentJoint, p = True)
                
            position = cmds.xform(rootJoint, q = True, t = True, ws = True)
            positions.append(position)
            positions.reverse()
            
            # Create curves to control the spine
            cmds.curve(p = [(rootPosition[0], rootPosition[1], rootPosition[2])], n = 'Curve', degree = self.degree)
            for position in positions:
                cmds.curve('Curve', a = True, p = position)
                
            curveCV = cmds.ls('Curve.cv[0:]', fl = True)
            parent = None
            for k, cv in enumerate(curveCV):
                cluster = cmds.cluster(cv, cv, n = 'Curve_Cluster_' + str(k))
                
                if parent:
                    cmds.parent(cluster, parent)
                    
                parent = cluster
            
            cmds.ikHandle(n = self.name, sj = rootJoint[0], ee = endJoint[0], sol = self.solverType, c = 'Curve', ccv = False)
        else:            
            cmds.ikHandle(name = self.name, sj = cmds.ls(self.sourceJoint)[0], ee = cmds.ls(self.endJoint)[0], sol = self.solverType)
        
         
# Container for all IK handles
class IkHandler():
    def importConfig(self, Data):
        ikConfig = Data['IK'] or []
        
        self.handlers = []
        for handleData in ikConfig:
            newHandler = IkHandle(handleData)
            self.handlers.append(newHandler)
            
        self.refreshList()
        
    def refreshList(self):
        for handle in self.handlers:
            cmds.textScrollList('listWidget', edit=True, append=[handle.toStr()])
            
    def buildHandlers(self):
        for handle in self.handlers:
            handle.buildHandler()
    
    def __init__(self):
        self.handlers = []
