import json
import maya.cmds as cmds
import maya.OpenMaya as om

class NamingChecks():

    def import_naming_conventions(self):
        """
        Import naming conventions from a file
        """
        file_path = r"D:/git/maya/model_checker/json_data/naming_convention.json"
        with open(file_path, 'r') as file:
            self.naming_conventions = json.load(file)


    def separate_data(self):
        """
        Check for naming conventions in the scene
        """
        self.import_naming_conventions()
        for name, data in self.naming_conventions.items():
            if name == "name_structure":
                for key, value in data.items():
                    print(key)
                    if key == "name":
                        self.structure = value
                    elif key == "separator":
                        self.separator = value
            elif name == "suffixes":
                for key, value in data.items():
                    print(key)
                    if key == "name":
                        self.structure = value
                    elif key == "separator":
                        self.separator = value


    def variables(self):
        """
        Check for naming conventions in the scene
        """
        self.side_suffix = ["L", "R", "C"]


    def check_naming_structure(self):
        """
        Check for naming structure in the scene
        """
        items = cmds.ls(type='transform')
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
            if len(name) != 3 :
                bad_names.append(obj)
            else:
                pos = cmds.xform(obj, query=True, worldSpace=True, translation=True)
                x_value = pos[0]
                if (x_value == 0 and name[0] == "C") or (x_value < 0 and name[0] == "R") or (x_value > 0 and name[0] == "L"):
                    continue
                else:
                    bad_names_side.append(obj)

                    

        
        return bad_names_side, bad_names

    def duplicated_names(self):
        """
        Check for duplicated names in the scene
        """
        items = cmds.ls(type='transform')
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
    
    def check_pasted_nodes(self):
        """
        Check for pasted nodes in the scene
        """
        items = cmds.ls(transforms=True, textures=True, shapes=False)
        print(items)
        pasted_nodes = []
        for obj in items:
            if "pasted__" in obj:
                pasted_nodes.append(obj)
        if pasted_nodes:
            return pasted_nodes
        else:
            return None
    
    def check_namespaces(self):
        """
        Check for name spaces in the scene
        """
        name_spaces = []
        items = cmds.ls(transforms=True, textures=True, shapes=False)
        for obj in items:
            if ":" in obj:
                name_spaces.append(obj)
        if name_spaces:
            return name_spaces
        else:
            return None


print(NamingChecks().check_namespaces())