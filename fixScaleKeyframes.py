import bpy

obj = bpy.context.object
bpy.ops.object.mode_set(mode='POSE', toggle=False)

for track in obj.animation_data.nla_tracks:
    actionName = track.name + '_' + obj.name
    obj.animation_data.action = bpy.data.actions.get(actionName)
    if obj.animation_data.action is not None:
        fcurves = obj.animation_data.action.fcurves
        for fcurve in fcurves:
            if fcurve.data_path.endswith("scale"):
                for keyframe in fcurve.keyframe_points:
                    keyframe.co_ui[1] *= 100
