import maya.cmds as cmds
import maya.OpenMaya as om

def check_naming_structure(items, export_data):
    """
    Check for naming structure in the scene

    Args:
        items (list): List of nodes to check
        export_data (dict): Export data from the export file
    """
    # Get the naming convention from the export data
    for key, value in export_data.items():
            if key == "type_suffix":
                for key, value in value.items():
                    if key == "Transforms":
                        transforms_type = value
                    if key == "Meshes":
                        meshes_type = value
                    if key == "Joints":
                        joints_type = value
                    if key == "Locators":
                        locators_type = value
                    if key == "Clusters":
                        clusters_type = value
                    if key == "Lights":
                        lights_type = value
            if key == "NamingConvention":
                naming_convention = value
            if key == "side":
                for key, value in value.items():
                    if key == "Left":
                        left_side = value
                    if key == "Center":
                        center_side = value
                    if key == "Right":
                        right_side = value

    # Get the indexes of the side and type in the naming convention
    for i, part in enumerate(naming_convention):
        if "Side" in part:
            side_index = i + 1
        elif "Type" in part:
            type_index = i + 1

    # Check the naming structure of the items
    final_items = []
    for obj in items:
        relatives = cmds.listRelatives(obj, shapes=True)
        if relatives:
            for relative in relatives:
                if cmds.objectType(relative) != "camera":
                    final_items.append(obj)
                else:    
                    continue
        else:
            final_items.append(obj)

    bad_names = []

    # Check the naming structure of the items
    for obj in final_items:
        name = obj.split("_")
        if len(name) != len(naming_convention):
            bad_names.append(obj)
            continue

        # Check the side and type of the object
        if side_index:
            pos = cmds.xform(obj, q=True, worldSpace=True, translation=True)
            side = center_side if pos[0] == 0 else (right_side if pos[0] > 0 else left_side)
            
            if not side in name[side_index-1]:
                bad_names.append(obj)
                continue
        
        # Check the type of the object and if it has the correct name
        if type_index:
            obj_type = cmds.objectType(obj)
            if obj_type == "transform":
                if cmds.listRelatives(obj, shapes=True):
                    shape = cmds.listRelatives(obj, shapes=True)[0]
                    shape_type = cmds.objectType(shape)
                    if shape_type == "mesh":
                        if not meshes_type in name[type_index-1]:
                            bad_names.append(obj)
                            continue
                    elif shape_type == "joint":
                        if not joints_type in name[type_index-1]:
                            bad_names.append(obj)
                            continue
                    elif shape_type == "locator":
                        if not locators_type in name[type_index-1]:
                            bad_names.append(obj)
                            continue
                    elif shape_type == "clusterHandle":
                        if not clusters_type in name[type_index-1]:
                            bad_names.append(obj)
                            continue
                    elif shape_type == "aiAreaLight":
                        if not lights_type in name[type_index-1]:
                            bad_names.append(obj)
                            continue
                else:
                    if not  transforms_type in name[type_index-1]:
                        bad_names.append(obj)
                        continue
            elif obj_type == "mesh":
                if not meshes_type in name[type_index-1]:
                    bad_names.append(obj)
                    continue
            elif obj_type == "joint":
                if not joints_type in name[type_index-1]:
                    bad_names.append(obj)
                    continue
            elif obj_type == "locator":
                if not locators_type in name[type_index-1]:
                    bad_names.append(obj)
                    continue
            elif obj_type == "clusterHandle":
                if not clusters_type in name[type_index-1]:
                    bad_names.append(obj)
                    continue
            elif obj_type == "aiAreaLight":
                if not lights_type in name[type_index-1]:
                    bad_names.append(obj)
                    continue
    bad_names = list(set(bad_names))

    # Return the list of bad names or none
    return bad_names

def duplicated_names(items):
    """
    Check for duplicated names in the scene

    Args:
        items (list): List of nodes to check
    """
    duplicated_names = []
    name_count = {}
    
    # Get the short name of the objects
    for obj in items:
        # Get the short name of the object
        short_name = obj.split('|')[-1]
        if short_name in name_count:
            name_count[short_name].append(obj)
        else:
            name_count[short_name] = [obj]
    
    # Check for duplicated names
    for name, obj_list in name_count.items():
        if len(obj_list) > 1:
            duplicated_names.extend(obj_list)
    
    # Return the list of duplicated names or none
    if duplicated_names:
        return duplicated_names
    else:
        return None

def check_pasted_nodes(items):
    """
    Check for pasted nodes in the scene

    Args:
        items (list): List of nodes to check
    """
    pasted_nodes = []
    # Check for pasted nodes
    for obj in items:
        if "pasted__" in obj:
            # Add the pasted node to the list
            pasted_nodes.append(obj)
    if pasted_nodes:
        return pasted_nodes
    else:
        return None

def check_namespaces(items):
    """
    Check for name spaces in the scene

    Args:
        items (list): List of nodes to check
    """
    name_spaces = []
    # Check for name spaces
    for obj in items:
        # Check if the object has a name space
        if ":" in obj:
            name_spaces.append(obj)
    
    # Return the list of name spaces or none
    if name_spaces:
        return name_spaces
    else:
        return None
