import maya.cmds as cmds
import maya.OpenMaya as om

def check_naming_structure(items, export_data):
    """
    Check for naming structure in the scene
    """
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

    for i, part in enumerate(naming_convention):
        if "Side" in part:
            side_index = i + 1
        elif "Type" in part:
            type_index = i + 1

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

    for obj in final_items:
        name = obj.split("_")
        if len(name) != len(naming_convention):
            bad_names.append(obj)
            continue

        
        if side_index:
            pos = cmds.xform(obj, q=True, worldSpace=True, translation=True)
            side = center_side if pos[0] == 0 else (right_side if pos[0] > 0 else left_side)
            
            if not side in name[side_index-1]:
                bad_names.append(obj)
                continue

        if type_index:
            obj_type = cmds.objectType(obj)
            if obj_type == "transform":
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
            elif obj_type == "cluster":
                if not clusters_type in name[type_index-1]:
                    bad_names.append(obj)
                    continue
            elif obj_type == "light":
                if not lights_type in name[type_index-1]:
                    bad_names.append(obj)
                    continue
    
    return bad_names

def duplicated_names(items):
    """
    Check for duplicated names in the scene
    """
    duplicated_names = []
    name_count = {}
    
    for obj in items:
        short_name = obj.split('|')[-1]
        if short_name in name_count:
            name_count[short_name].append(obj)
        else:
            name_count[short_name] = [obj]
    
    for name, obj_list in name_count.items():
        if len(obj_list) > 1:
            duplicated_names.extend(obj_list)
    
    if duplicated_names:
        return duplicated_names
    else:
        return None

def check_pasted_nodes(items):
    """
    Check for pasted nodes in the scene
    """
    pasted_nodes = []
    for obj in items:
        if "pasted__" in obj:
            pasted_nodes.append(obj)
    if pasted_nodes:
        return pasted_nodes
    else:
        return None

def check_namespaces(items):
    """
    Check for name spaces in the scene
    """
    name_spaces = []
    for obj in items:
        if ":" in obj:
            name_spaces.append(obj)
    if name_spaces:
        return name_spaces
    else:
        return None
