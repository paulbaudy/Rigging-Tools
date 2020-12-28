import maya.cmds as cmds

class IkHandle():
    def __init__(self):
        self.name = 'None'
        self.solverType = 'None'
        self.sourceJoint = 'None'
        self.endJoint = 'None'
        self.degree = 'None'
        
    def __init__(self, Data):
        self.name = Data['Name']
        self.solverType = Data['Solver']
        self.sourceJoint = Data['SourceJoint']
        self.endJoint = Data['EndJoint']
        self.degree = Data['Degree'] if 'Degree' in Data else 0
                
    def buildHandler(self):
        if self.solverType == 'ikSplineSolver':
            # Special case for spine solvers 
            rootJoint = cmds.ls(self.sourceJoint, type = 'joint')
            rootPosition = cmds.xform(rootJoint, q = True, t = True, ws = True)
            endJoint = cmds.ls(self.endJoint, type = 'joint')
            
            parentJoint = endJoint
            positions = []
             
            while parentJoint != rootJoint:
                print parentJoint
                position = cmds.xform(parentJoint, q = True, t = True, ws = True)
                positions.append(position)
                parentJoint = cmds.listRelatives(parentJoint, p = True)
                
            position = cmds.xform(rootJoint, q = True, t = True, ws = True)
            positions.append(position)
                
            print positions
            positions.reverse()
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
        
         

class IkHandler():
    def importConfig(self, Data):
        ikConfig = Data['IK'] or []
        
        self.handlers = []
        for handleData in ikConfig:
            newHandler = IkHandle(handleData)
            newHandler.buildHandler()
            self.handlers.append(newHandler)
            
            
        print self.handlers
    
    def __init__(self):
        print 'yay'

def BuildHandles():
    print 'yay'