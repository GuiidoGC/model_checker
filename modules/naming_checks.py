import maya.cmds as cmds
import maya.OpenMaya as om

print("Imported naming_checks")

def check_naming_structure(export_data, items):
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

    for obj in items:
        relatives = cmds.listRelatives(obj, shapes=True)
        if relatives:
            for relative in relatives:
                if cmds.objectType(relative) == "camera":
                    items.remove(obj)
                else:    
                    continue
        else:
            continue
        
    bad_names = []
    bad_names_side = []
    for obj in items:
        name = obj.split("_")
        if len(name) != len(naming_convention):
            bad_names.append(obj)

        elif "Side" in naming_convention:
            prefix_index = naming_convention.index("Prefix")
            pos = cmds.xform(obj, query=True, worldSpace=True, translation=True)
            x_value = pos[0]
            if (x_value == 0 and name[0] == center_side) or (x_value < 0 and name[0] == right_side) or (x_value > 0 and name[0] == left_side):
                continue 
            else:
                bad_names_side.append(obj)

        elif "Prefix" in naming_convention:
            prefix_index = naming_convention.index("Prefix")
            obj_type = cmds.objectType(obj)

            if obj_type == "transform":
                if name[prefix_index] != transforms_type:
                    bad_names.append(obj)
            elif obj_type == "mesh":
                if name[prefix_index] != meshes_type:
                    bad_names.append(obj)
            elif obj_type == "joint":
                if name[prefix_index] != joints_type:
                    bad_names.append(obj)
            elif obj_type == "locator":
                if name[prefix_index] != locators_type:
                    bad_names.append(obj)
            elif obj_type == "cluster":
                if name[prefix_index] != clusters_type:
                    bad_names.append(obj)
            elif obj_type == "light":
                if name[prefix_index] != lights_type:
                    bad_names.append(obj)
            else:
                continue

            

                

    
    return bad_names_side, bad_names

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
