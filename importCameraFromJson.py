import bpy
import bmesh
import os
import io
import struct
from mathutils import Vector
from bpy.props import (BoolProperty,
                       FloatProperty,
                       StringProperty,
                       EnumProperty,
                       CollectionProperty
                       )
import pathlib
import json
import math
 
class FOVKey:
    time = 0.0
    fov = 0.0
       
class PosKey:
    time = 0.0
    pos: Vector
           
class RotKey:
    time = 0.0
    rot: Vector
    
class CameraAnim:
    fov = []
    pos = []
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
                
                cameraAnim = CameraAnim()
                
                floatProp = data[2]
                floatProperties = floatProp.get("Properties")
                floatTrack = floatProperties.get("FloatTrack")
                floatPoints = floatTrack.get("Points")
                
                for fovFrame in floatPoints:
                    fovKey = FOVKey()
                    fovKey.time = float(fovFrame.get("InVal"))
                    fovKey.fov = float(fovFrame.get("OutVal"))
                    cameraAnim.fov.append(fovKey)
                
                move = data[3]
                moveProperties = move.get("Properties")
                
                if moveProperties.get("bLightAnimTrack") or moveProperties.get("bLightAmbientColorTrack"):
                    move = data[4]
                    moveProperties = move.get("Properties")
                
                if moveProperties.get("bLightAnimTrack") or moveProperties.get("bLightAmbientColorTrack"):
                    move = data[5]
                    moveProperties = move.get("Properties")
                
                posTrack = moveProperties.get("PosTrack")
                posPoints = posTrack.get("Points")
                
                for posFrame in posPoints:
                    posKey = PosKey()
                    posKey.time = float(posFrame.get("InVal"))
                    outVal = posFrame.get("OutVal")
                    posKey.pos = Vector((float(outVal.get("Y"))/-100, float(outVal.get("X"))/-100, float(outVal.get("Z"))/100))
                    cameraAnim.pos.append(posKey)
                
                eulTrack = moveProperties.get("EulerTrack")
                eulPoints = eulTrack.get("Points")

                for eulFrame in eulPoints:
                    rotKey = RotKey()
                    rotKey.time = float(eulFrame.get("InVal"))
                    outVal = eulFrame.get("OutVal")
                    rotKey.rot = Vector((float(outVal.get("Y"))/57.3 + 90/57.3, float(outVal.get("X"))/57.3, float(outVal.get("Z"))/-57.3 + 180/57.3))
                    cameraAnim.rot.append(rotKey)
                    
                obj_camera = bpy.context.scene.camera
                
                if obj_camera is not None:
                    obj_camera.animation_data_create()
                    context.scene.frame_start = 0
                    bpy.context.scene.render.fps = 60
                    action = bpy.data.actions.new(i.name[:-5])
                    obj_camera.animation_data.action = action

                    for fovFrameNew in cameraAnim.fov:
                        obj_camera.data.lens = 18*(1/math.tan( (math.pi*fovFrameNew.fov) /360 ))
                        obj_camera.data.keyframe_insert(data_path="lens", frame = fovFrameNew.time * bpy.context.scene.render.fps)
                    for posFrameNew in cameraAnim.pos:
                        obj_camera.location = posFrameNew.pos
                        obj_camera.keyframe_insert(data_path="location", frame = posFrameNew.time * bpy.context.scene.render.fps)
                    for rotFrameNew in cameraAnim.rot:
                        obj_camera.rotation_euler = rotFrameNew.rot
                        obj_camera.keyframe_insert(data_path="rotation_euler", frame = rotFrameNew.time * bpy.context.scene.render.fps)                        
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