# Sets timeline end to match the currently active action.
# Additional offset used to extend the timeline range beyond the last keyframe.
offset = 5

import bpy
import math

def drawPanel(txt):
    def draw(self, context):
        self.layout.label(text=txt)
    bpy.context.window_manager.popup_menu(draw, title = "actionTimelineAdjust", icon = "INFO")

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

obj = grabObj()
if obj is None:
    drawPanel("Select the proper armature/mesh first, please.")
else:
    action = obj.animation_data.action
    if action is not None:
        action_frame_end = math.floor(action.frame_range[1] + 1 + offset)
        bpy.context.scene.frame_end = action_frame_end
        drawPanel("Timeline end set to: " + str(action_frame_end))
    else:
        drawPanel("Select an action using the action editor.")