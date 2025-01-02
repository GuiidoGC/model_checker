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
    
def check_pivots(sel):
    """
    Check for objects with non-centered pivots in the scene

    Args:
    """
    non_centered_pivots = []
    for obj in sel:
        pivot = cmds.xform(obj, q=True, worldSpace=True, piv=True)
        print(pivot)
        if pivot != [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]:
            non_centered_pivots.append(obj)
        else:
            continue
    if non_centered_pivots:
        return non_centered_pivots

def check_ngons(sel):
    """
    Check for ngons in the scene

    Args:
    """
    ngons = []
    for obj in sel:
        faces = cmds.polyEvaluate(obj, face=True)
        for i in range(faces):
            vertices = cmds.polyInfo(f"{obj}.f[{i}]", faceToVertex=True)
            vertices = vertices[0].split("    ")
            if len(vertices) > 6:
                ngons.append(f"{obj}.f[{i}]")
            else:
                continue
    if ngons:
        return ngons
    
def check_tris(sel):
    """
    Check for tris in the scene

    Args:
    """
    tris = []
    for obj in sel:
        faces = cmds.polyEvaluate(obj, triangle=True)
        print(faces)
        # for i in range(faces):
        #     vertices = cmds.polyInfo(f"{obj}.f[{i}]", faceToVertex=True)
        #     vertices = vertices[0].split("    ")
        #     print(vertices)
        #     if len(vertices) == 4:
        #         tris.append(f"{obj}.f[{i}]")
        #     else:
        #         continue
    if tris:
        return tris

def check_non_manifold(sel):
    """
    Check for non-manifold geometry in the scene

    Args:
    """
    print(sel)
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

def check_zero_cv_positions(sel):
    """
    Check for zero cv positions in the scene

    Args:
    """


    zero_cv_positions = []
    for obj in sel:
        cv_positions = cmds.ls(f"{obj}.pnts[*].pntx" , fl=True)
        for cv in cv_positions:
            position = cmds.pointPosition(cv, w=True)
            if position == [0.0, 0.0, 0.0]:
                zero_cv_positions.append(cv)
            else:
                continue
    if zero_cv_positions:
        return zero_cv_positions
    else:
        return None


sel = cmds.ls(sl=True)
print(check_non_manifold(sel))
