import maya.cmds as cmds
import maya.OpenMaya as om


def check_empty_groups(selection):
    """
    Check for empty groups in the scene
    """
    empty_groups = []
    for node in selection:
        if not cmds.listRelatives(node, children=True):
            empty_groups.append(node)
    if empty_groups:
        return empty_groups
    else:
        return None 
    
def check_node_hisotry(selection):
    """
    Check for nodes with history in the scene
    """
    nodes_with_history = []
    for node in selection:
        history = cmds.listHistory(node)
        for i in history:
            if i != node:
                if "Shape" in i:
                    continue
                else:
                    nodes_with_history.append(node)
    if nodes_with_history:
        return nodes_with_history
    else:
        return None
    
def check_unnused_textures(textures):
    """
    Check for unnused textures in the scene
    """
    unnused_textures = []
    for texture in textures:
        if cmds.objectType(texture) == "file":
            x = cmds.listConnections(texture, source=False, destination=True)
            for items in x:
                if "defaultTextureList" in items:
                    x.remove(items)
                if not x:
                    unnused_textures.append(texture)
        else:
            om.MGlobal_displayError(f"{texture} is not a texture")
    if unnused_textures:
        return unnused_textures
    else:
        return None
    
def check_unnused_shaders(shaders):
    """
    Check for unnused shaders in the scene
    """
    unnused_shaders = []
    for shader in shaders:
        if cmds.objectType(shader) == "shadingEngine":
            connections = cmds.listConnections(shader, type='mesh')
            if not connections:
                unnused_shaders.append(shader)
        else:
            om.MGlobal_displayError(f"{shader} is not a shader")
    if unnused_shaders:
        return unnused_shaders
    else:
        return None