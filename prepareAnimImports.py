# Sets all animations to constant interpolation.
# Removes the object suffix from all NLA tracks & actions.
# Clamps bone scale to prevent absolute zero (which can cause issues in UE4).
import bpy

def drawPanel(txt):
    def draw(self, context):
        self.layout.label(text=txt)
    bpy.context.window_manager.popup_menu(draw, title = "prepareAnimImports", icon = "INFO")

def grabObj():
    try:
        obj = bpy.context.active_object
        match obj.type:
            case "MESH":
                if obj.parent and obj.parent.type == "ARMATURE":
                    return obj.parent
                else:
                    return None
            case "ARMATURE":
                return obj
            case _:
                return None
    except:
        return None

def setConstantInterpolation():
    for a in actions:
        try:
            for fcurve in a.fcurves:
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

def clampKeyframeScale():
    for a in actions:
        try:
            for fcurve in a.fcurves:
                if fcurve.data_path.endswith("scale"):
                    for kf in fcurve.keyframe_points:
                        if kf.co.y == 0:
                            kf.co.y = 0.001
        except:
            pass

obj = grabObj()
if obj is None:
    drawPanel("Select the proper armature/mesh first, please.")
else:
    actions = bpy.data.actions
    nlaTracks = obj.animation_data.nla_tracks

    setConstantInterpolation()
    renameActions()
    renameNlaStrips()
    clampKeyframeScale()
    drawPanel("Done :)")
