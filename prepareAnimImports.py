# Sets all animations to constant interpolation, and removes the object suffix from all NLA tracks & actions.
# Select the armature in the outliner before running the script.

import bpy

obj = bpy.context.active_object
actions = bpy.data.actions
nlaTracks = obj.animation_data.nla_tracks

def setConstantInterpolation():
    for a in actions:
        try:
            fcurves = a.fcurves
            for fcurve in fcurves:
                for kf in fcurve.keyframe_points:
                    kf.interpolation = 'CONSTANT'
        except:
            pass

def renameActions():
    for a in actions:
        try:
            a.name = a.name.replace("_" + obj.name, "")
        except:
            pass

def renameNlaStrips():
    for a in nlaTracks:
        try:
            a.strips[0].name = a.strips[0].name.replace("_" + obj.name, "")
        except:
            pass

setConstantInterpolation()
renameActions()
renameNlaStrips()
