import maya.cmds as cmds
import maya.OpenMaya as om


def check_empty_groups(selection):
    """
    Check for empty groups in the scene

    Args:
        selection (list): List of nodes to check
    """
    empty_groups = []
    for node in selection:
        # Check if the node has children
        if not cmds.listRelatives(node, children=True):
            empty_groups.append(node)
    # Return the list of empty groups or none
    if empty_groups:
        return empty_groups
    else:
        return None 
    
def check_node_hisotry(selection):
    """
    Check for nodes with history in the scene

    Args:
        selection (list): List of nodes to check
    """
    nodes_with_history = []
    for node in selection:
        # Check if the node has history
        history = cmds.listHistory(node)
        for i in history:
            if i != node:
                if "Shape" in i:
                    continue
                else:
                    nodes_with_history.append(node)
    # Return the list of nodes with history or none
    if nodes_with_history:
        return nodes_with_history
    # Return the list of nodes with history or none
    else:
        return None
    
def check_unnused_textures(textures):
    """
    Check for unnused textures in the scene
    
    Args:
        selection (list): List of nodes to check
    """
    unnused_textures = []
    for texture in textures:
        # Check if the node is a texture
        if cmds.objectType(texture) == "file":
            x = cmds.listConnections(texture, source=False, destination=True)
            for items in x:
                if "defaultTextureList" in items:
                    x.remove(items)
                if not x:
                    unnused_textures.append(texture)
        else:
            # Display error if the node is not a texture
            om.MGlobal_displayError(f"{texture} is not a texture")
    # Return the list of unnused textures or none
    if unnused_textures:
        return unnused_textures
    else:
        return None
    
def check_unnused_shaders(shaders):
    """
    Check for unnused shaders in the scene
    
    Args:
        selection (list): List of nodes to check
    """
    unnused_shaders = []
    for shader in shaders:
        # Check if the node is a shader
        if cmds.objectType(shader) == "shadingEngine":
            connections = cmds.listConnections(shader, type='mesh')
            if not connections:
                unnused_shaders.append(shader)
        else:
            # Display error if the node is not a shader
            om.MGlobal_displayError(f"{shader} is not a shader")

    # Return the list of unnused shaders or none
    if unnused_shaders:
        return unnused_shaders
    else:
        return None