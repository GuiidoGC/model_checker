import maya.cmds as cmds
import maya.OpenMaya as om

def check_empty_groups():
    """
    Check for empty groups in the scene
    """
    empty_groups = []
    for node in cmds.ls(type='transform'):
        if not cmds.listRelatives(node, children=True):
            empty_groups.append(node)
    if empty_groups:
        return empty_groups
    else:
        return None 
    
def check_node_hisotry():
    """
    Check for nodes with history in the scene
    """
    nodes_with_history = []
    for node in cmds.ls(type='transform'):
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
    
def check_unnused_textures():
    """
    Check for unnused textures in the scene
    """
    textures = cmds.ls(type='file')
    unnused_textures = []
    for texture in textures:
        x = cmds.listConnections(texture, source=False, destination=True)
        for items in x:
            if "defaultTextureList" in items:
                x.remove(items)
            if not x:
                unnused_textures.append(texture)
    if unnused_textures:
        return unnused_textures
    else:
        return None
    
def check_unnused_shaders():
    """
    Check for unnused shaders in the scene
    """
    shaders = cmds.ls(type='shadingEngine')
    unnused_shaders = []
    for shader in shaders:
        connections = cmds.listConnections(shader, type='mesh')
        if not connections:
            unnused_shaders.append(shader)
    if unnused_shaders:
        return unnused_shaders
    else:
        return None