import maya.cmds as cmds
import maya.OpenMaya as om

def check_object_unfreezed(sel):
    """
    Check for freezed objects in the scene

    Args:
    """


    unfreezed_objects = []
    for obj in sel:
        translation = cmds.xform(obj, q=True, worldSpace=True, translation=True)
        rotation = cmds.xform(obj, q=True, worldSpace=True, rotation=True)
        scale = cmds.xform(obj, q=True, worldSpace=True, scale=True)
        for i, value in enumerate([translation, rotation, scale]):
            if i != 2:
                if value != [0.0, 0.0, 0.0]:
                    unfreezed_objects.append(obj)
                else:
                    continue
            else:
                if value != [1.0, 1.0, 1.0]:
                    unfreezed_objects.append(obj)
                else:
                    continue

    if unfreezed_objects:
        return unfreezed_objects
    else:
        return None

    
def check_pivots(sel):
    """
    Check for objects with non-centered pivots in the scene

    Args:
    """
    non_centered_pivots = []
    for obj in sel:
        pivot = cmds.xform(obj, q=True, worldSpace=True, piv=True)
        if pivot != [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]:
            non_centered_pivots.append(obj)
        else:
            continue
    if non_centered_pivots:
        return non_centered_pivots
    else: 
        return None

def check_ngons(sel):
    """
    Check for ngons in the scene

    Args:
    """
    ngons = []
    for obj in sel:
        if cmds.nodeType(obj) == "mesh":
            faces = cmds.polyEvaluate(obj, face=True)
            for i in range(faces):
                vertices = cmds.polyInfo(f"{obj}.f[{i}]", faceToVertex=True)
                vertices = vertices[0].split()
                if len(vertices) > 6:
                    ngons.append(f"{obj}.f[{i}]")
                else:
                    continue
    if ngons:
        return ngons

def check_non_manifold(sel):
    """
    Check for non-manifold geometry in the scene

    Args:
    """
    non_manifold = []
    for obj in sel:
        non_manifold_faces = cmds.polyInfo(obj, nonManifoldEdges=True)
        if non_manifold_faces:
            non_manifold.append(obj)
        else:
            continue
    if non_manifold:
        return non_manifold
    else:
        return None    

