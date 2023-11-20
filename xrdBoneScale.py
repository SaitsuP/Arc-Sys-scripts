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
from pathlib import Path

class ScaleInfo:
    time = 0.0
    sclX = 0
    sclY = 0
    sclZ = 0

class CustomDrawOperator(bpy.types.Operator):
    bl_idname = "object.custom_draw"
    bl_label = "Import"

    filepath:bpy.props.StringProperty(subtype="FILE_PATH")
    files:CollectionProperty(type=bpy.types.PropertyGroup)

    def execute(self, context):
        folder = (os.path.dirname(self.filepath))
        NameFile = open(os.path.join(str(Path(folder).parents[1]), "NameTable.txt"), "r")
        for i in self.files:
                animFile = open((os.path.join(folder, i.name)),"rb")
                animFile.seek(28, 0)
                animNameIndex = str(struct.unpack('i', animFile.read(4))[0])
                
                print(animNameIndex)
                
                animName = ''
                NameFile.seek(0,0)

                for line in NameFile:
                    if line.startswith(animNameIndex):
                        animName = line
                        break
                
                animNameStart = animName.index('"')
                animName = animName[animNameStart+1:]
                animName = animName[:-2]
                
                scaleFolder = os.path.join(folder, Path(i.name).stem)
                
                try:
                    for filename in os.listdir(scaleFolder):
                        CurFile = open(os.path.join(scaleFolder, filename),"rb")
                        s = CurFile.read()
                        #print(s)
                        frameList = []
                        boneName = 0
                        
                        scaleKey = 0
                        index = 0
                              
                        NameFile.seek(0,0)
                              
                        for line in NameFile:
                            if '"ScaleKeys"' in line:
                                scaleKey = index
                                break
                            index += 1
                        
                        scaleKeyIndex = s.find(scaleKey.to_bytes(4, 'little'))

                        # - Location of Scale Keys
                        CurFile.seek(scaleKeyIndex,0)
                        CurFile.read(4)

                        # - Array Property
                        CurFile.read(4)
                        #print()

                        # - Seek through junk
                        CurFile.seek(16,1)

                        # - Array Count
                        count = struct.unpack('i', CurFile.read(4) )[0]
                        for i in range(count):
                            scaleInfo = ScaleInfo()
                            newTable = []
                            scaleVector = [0,0,0]
                            newTable.append(['Time',struct.unpack('i', CurFile.read(4))[0]])
                            
                            newTable.append(['null',struct.unpack('i', CurFile.read(4))[0]])
                            
                            # - Float Property
                            newTable.append(['Float Property',struct.unpack('i', CurFile.read(4))[0]])
                            
                            # - Seek throgh junk
                            newTable.append(['null',struct.unpack('i', CurFile.read(4))[0]])
                            newTable.append(['Unknown (AnimationCompressionAlgorithm_CutScene)',struct.unpack('i', CurFile.read(4))[0]])
                            newTable.append(['null',struct.unpack('i', CurFile.read(4))[0]])
                            
                            scaleInfo.time = struct.unpack('<f', CurFile.read(4))
                            
                            # - Scale Vector
                            newTable.append(['Scale Vector',struct.unpack('i', CurFile.read(4))[0]])
                            
                            # - Seek throgh junk
                            newTable.append(['null',struct.unpack('i', CurFile.read(4))[0]])
                            
                            # - Struct Property
                            newTable.append(['Struct Property',struct.unpack('i', CurFile.read(4))[0]])
                            
                            # - Seek throgh junk
                            newTable.append(['null',struct.unpack('i', CurFile.read(4))[0]])
                            newTable.append(['Unknown (AnimSelector)',struct.unpack('i', CurFile.read(4))[0]])
                            newTable.append(['null',struct.unpack('i', CurFile.read(4))[0]])
                            
                            # - Vector
                            newTable.append(['Vector',struct.unpack('i', CurFile.read(4))[0]])
                            
                            newTable.append(['null',struct.unpack('i', CurFile.read(4))[0]])
                            
                            scaleInfo.sclX = struct.unpack('<f', CurFile.read(4))
                            scaleInfo.sclY = struct.unpack('<f', CurFile.read(4))
                            scaleInfo.sclZ = struct.unpack('<f', CurFile.read(4))
                            
                            newTable.append(['Unknown (None)',struct.unpack('i', CurFile.read(4))[0]])
                            newTable.append(['null',struct.unpack('i', CurFile.read(4))[0]])
                            
                            
                            frameList.append(scaleInfo)
                            
                        nameList = 0
                        index = 0
                        
                        NameFile.seek(0,0)
                        
                        for line in NameFile:
                            if '"SkelControlNameList"' in line:
                                nameList = index
                                break
                            index += 1
                        
                        nameListIndex = s.find(nameList.to_bytes(4, 'little'))

                        # - Location of Scale Keys
                        CurFile.seek(nameListIndex,0)
                        CurFile.read(4)
                        CurFile.read(12)
                        CurFile.read(12)

                        boneName = struct.unpack('i', CurFile.read(4))

                        nameIndex = str(boneName[0])

                        name = ''
                
                        NameFile.seek(0,0)

                        for line in NameFile:
                            if line.startswith(nameIndex):
                                name = line
                                break
                        
                        nameStart = name.index('"')
                        name = name[nameStart+1:]
                        name = name[:-2]

                        obj = bpy.context.object
                        bpy.ops.object.mode_set(mode='POSE', toggle=False)
                        bpy.context.scene.frame_start = 0
                        
                        actionName = ''
                        for track in obj.animation_data.nla_tracks:
                            if track.name.startswith(animName):
                                actionName = track.name + '_' + obj.name
                        
                        obj.animation_data.action = bpy.data.actions.get(actionName)
                        
                        bone = obj.pose.bones.get(name)
                        if bone is not None:
                            for frame in frameList:
                                frameIndex = frame.time[0] * bpy.context.scene.render.fps
                                scl = Vector((frame.sclX[0], frame.sclY[0], frame.sclZ[0]))
                                bone.scale = scl
                                bone.keyframe_insert(data_path='scale', frame = frameIndex)
                except:
                    continue
        return {'FINISHED'}
    
        # --- End File Loop
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

bpy.utils.register_class(CustomDrawOperator)

# test call
bpy.ops.object.custom_draw('INVOKE_DEFAULT')