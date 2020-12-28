import maya.cmds as cmds

def init():
        global RootHeight
        RootHeight = 0
        global SpineCount
        SpineCount = 0
        global FingersCount
        FingersCount = 0
        global PhalanxCount
        PhalanxCount = 0
       

def initFromView(view):
        print 'init from view'
        
        print 'Settings applied'