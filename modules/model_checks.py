import maya.cmds as cmds
import maya.OpenMaya as om

def check_object_unfreezed(sel):
    """
    Check for freezed objects in the scene

    Args:
        selection (list): List of nodes to check
    """


    unfreezed_objects = []
    for obj in sel:
        # Get the translation, rotation and scale values of the object
        translation = cmds.xform(obj, q=True, worldSpace=True, translation=True)
        rotation = cmds.xform(obj, q=True, worldSpace=True, rotation=True)
        scale = cmds.xform(obj, q=True, worldSpace=True, scale=True)
        # Check if the object is freezed
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
    # Return the list of unfreezed objects or none
    if unfreezed_objects:
        return unfreezed_objects
    else:
        return None

    
def check_pivots(sel):
    """
    Check for objects with non-centered pivots in the scene

    Args:
        selection (list): List of nodes to check
    """
    non_centered_pivots = []
    for obj in sel:
        # Get the pivot values of the object
        pivot = cmds.xform(obj, q=True, worldSpace=True, piv=True)
        if pivot != [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]:
            non_centered_pivots.append(obj)
        else:
            continue
    # Return the list of objects with non-centered pivots or none
    if non_centered_pivots:
        return non_centered_pivots
    else: 
        return None

def check_ngons(sel):
    """
    Check for ngons in the scene

    Args:
        selection (list): List of nodes to check
    """
    ngons = []
    for obj in sel:
        # Get the relative shape of the object
        relative = cmds.listRelatives(obj, shapes=True)
        if relative:
            # Check if the object is a mesh
            if cmds.objectType(relative) == "mesh":
                faces = cmds.polyEvaluate(obj, face=True)
                for i in range(faces):
                    # Get the vertices of the face
                    vertices = cmds.polyInfo(f"{obj}.f[{i}]", faceToVertex=True)
                    vertices = vertices[0].split()
                    # Check if the face has more than 6 vertices
                    if len(vertices) > 6:
                        ngons.append(f"{obj}.f[{i}]")
                    else:
                        continue
        else:
            continue
    if ngons:
        return ngons

def check_non_manifold(sel):
    """
    Check for non-manifold geometry in the scene

    Args:
        selection (list): List of nodes to check
    """
    non_manifold = []
    for obj in sel:
        # Get the non-manifold faces of the object
        non_manifold_faces = cmds.polyInfo(obj, nonManifoldEdges=True)
        # Check if the object has non-manifold faces
        if non_manifold_faces:
            non_manifold.append(obj)
        else:
            continue
    # Return the list of objects with non-manifold faces or none
    if non_manifold:
        return non_manifold
    else:
        return None    

