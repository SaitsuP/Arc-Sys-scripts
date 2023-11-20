import bpy

obj = bpy.context.object
bpy.ops.object.mode_set(mode='POSE', toggle=False)

for track in obj.animation_data.nla_tracks:
    actionName = track.name + '_' + obj.name
    obj.animation_data.action = bpy.data.actions.get(actionName)
    if obj.animation_data.action is not None:
        obj.animation_data.action.name = track.name