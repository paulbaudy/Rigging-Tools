# Rigging-Tools

Rigging Tools is a set of tools used to generate control rigs on maya written in python.
Rigging Tools is still a work in progress.

It provides a simple user interface, designed with qt for maya, that you can use to change multiple settings that are stored in a single json configuration file, that you can import at any moment.

## Locators

Under the locators tab, you can modify some settings that will affect the position of the locators that will compose our bone hierarchy. You can also mirror some of the locators if you want to echo your changes from one side to another (works both ways, L -> R, and R -> L).

## Joints

Under the Joints tab, you can generate the joints hierarchy based on the locators.
@todo : Have multiple choices when it comes to joint orientations ( xyz, yzx, zxy, zyx, yxz, xzy )

## IK

Under this tab, you can simply create an IK handle quickly and easily, by selecting a solver, the source joint and an end effector. You can also have them stored under the json configuration file, under this format:  
```
        {
            "Name" : "Spine",
            "SourceJoint" : "Rig_Root",
            "EndJoint" : "Spine_3J",
            "Solver" : "ikSplineSolver",
            "Degree" : 1
        }
```

## Controller

This tab is currently a heavy WIP. You'll be able to create and export IK controllers under this format : 
```
        {
            "Name" : "RightLeg_Ctrl",
            "TargetIK" : "RightLeg",
            "Orient" : "R_FootJ"
        }
```
