import bpy
import bmesh
import os
import io
import struct
from mathutils import Euler
from bpy.props import (BoolProperty,
                       FloatProperty,
                       StringProperty,
                       EnumProperty,
                       CollectionProperty
                       )
import pathlib
import json
import math
           
class RotKey:
    time = 0.0
    rot: Euler
    
class LightAnim:
    rot = []
    
class CustomDrawOperator(bpy.types.Operator):
    bl_idname = "object.custom_draw"
    bl_label = "Import"

    filepath:bpy.props.StringProperty(subtype="FILE_PATH")
    files:CollectionProperty(type=bpy.types.PropertyGroup)

    def execute(self, context):
        folder = (os.path.dirname(self.filepath))
        for i in self.files:
            #try:
                CurFile = open((os.path.join(folder, i.name)),"rb")
                data = json.load(CurFile)
                
                lightAnim = LightAnim()
                
                move = data[3]
                moveProperties = move.get("Properties")
                
                if not moveProperties.get("bLightAnimTrack"):
                    move = data[4]
                    moveProperties = move.get("Properties")
                
                if not moveProperties.get("bLightAnimTrack"):
                    move = data[5]
                    moveProperties = move.get("Properties")
                
                eulTrack = moveProperties.get("EulerTrack")
                eulPoints = eulTrack.get("Points")

                for eulFrame in eulPoints:
                    rotKey = RotKey()
                    rotKey.time = float(eulFrame.get("InVal"))
                    outVal = eulFrame.get("OutVal")
                    rotKey.rot = Euler((float(outVal.get("X"))/57.3, float(outVal.get("Y"))/-57.3, float(outVal.get("Z"))/-57.3))
                    lightAnim.rot.append(rotKey)
                    
                light = bpy.context.scene.objects["Sun"]
                
                if light is not None:
                    light.animation_data_create()
                    context.scene.frame_start = 0
                    bpy.context.scene.render.fps = 60
                    action = bpy.data.actions.new(i.name[:-5])
                    light.animation_data.action = action

                    for rotFrameNew in lightAnim.rot:
                        light.rotation_euler = rotFrameNew.rot
                        light.keyframe_insert(data_path="rotation_euler", frame = rotFrameNew.time * bpy.context.scene.render.fps)                        
                else:
                    print("No camera found!")
            #except:
                #continue
        return {'FINISHED'}
    
        # --- End File Loop
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

bpy.utils.register_class(CustomDrawOperator)

# test call
bpy.ops.object.custom_draw('INVOKE_DEFAULT') 