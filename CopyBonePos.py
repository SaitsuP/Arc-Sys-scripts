import bpy

ref_ob = bpy.context.object
other_ob = [ob for ob in bpy.data.objects if ob.select_get()]
other_ob.remove(ref_ob)
other_ob = other_ob[0]

bpy.context.view_layer.objects.active = other_ob

bpy.ops.object.mode_set(mode='OBJECT')
for bone in ref_ob.pose.bones:
    if bone.name in other_ob.pose.bones:
        bpy.ops.object.mode_set(mode='POSE')
        other_ob.pose.bones[bone.name].matrix = bone.matrix
        bpy.ops.object.mode_set(mode='OBJECT')