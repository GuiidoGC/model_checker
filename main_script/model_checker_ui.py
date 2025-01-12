import maya.cmds as cmds
import maya.OpenMaya as om
from functools import partial
import general_checks as gc
import naming_checks as nc
import model_checks as mc
from importlib import reload
import json
import os
import webbrowser
reload(gc)
reload(nc)
reload(mc)

class ModelCheckerUI():
    """
    Class to create the UI for the model checker tool
    """
    def select_errors(self, *args):
        """
        Select the errors in the scene

        Args:
            self: The class instance
            Args: The arguments passed to the function by the UI
        """

        # Select the errors in the scene
        query = cmds.textScrollList(self.text_scroll_list, query=True, allItems=True)

        if query:
            select_items = []
            for index, item in enumerate(query):
                if index % 2 != 0 and index != 0: # Check if the index is odd
                    
                    item = item.split("----> ")[1]
                    item = item.split(",")
                    for i in item:
                        renamed = i.replace("['", "").replace("']", "").replace("'", "") # Rename the item
                        if renamed not in select_items:
                            select_items.append(renamed)
                        else:
                            continue
                    

            cmds.select(select_items, add=True)
            om.MGlobal.displayInfo("Errors selected") # Display the info message
        else:
            om.MGlobal.displayError("No errors to select") # Display the error message

    def export_log(self, *args):
        """
        Export the log file

        Args:
            self: The class instance
            Args: The arguments passed to the function by the UI
        """

        # Export the log file
        query = cmds.textScrollList(self.text_scroll_list, query=True, allItems=True) # Query the console output

        if query:
            log_dir = os.path.join(self.default_path, "logs")
            base_file_path = os.path.join(self.default_path, "logs/model_checker_log_001.json") # Set the base file path
            counter = 1
            while os.path.exists(base_file_path): # Check if the file exists
                base_file_path = os.path.join(log_dir, f"model_checker_log_{str(counter).zfill(2)}.json") # Set the file path
                counter += 1
            file_path = base_file_path

            with open(file_path, 'w') as json_file: # Open the JSON file
                json.dump(query, json_file, indent=4)

            om.MGlobal.displayInfo(f"Exported log to {file_path}") # Display the info message
        else:
            om.MGlobal.displayError("No log to export") # Display the error message
       
    def general_module_caller(self):
        """
        Call the module that contains the general checks functions

        Args:
            self: The class instance
        """



        # Get the checkboxes values
        empyt_checks = cmds.checkBoxGrp(self.general_checks_checkbox, query=True, value1=True)
        history_checks = cmds.checkBoxGrp(self.general_checks_checkbox, query=True, value2=True)
        unnused_sh_checks = cmds.checkBoxGrp(self.general_checks_checkbox, query=True, value3=True)
        unnused_tx_checks = cmds.checkBoxGrp(self.general_checks_checkbox, query=True, value4=True)

        if empyt_checks or history_checks or unnused_sh_checks or unnused_tx_checks:
            if cmds.ls(sl=True): # Check if there is a selection
                sel = cmds.ls(sl=True)
                textures = cmds.ls(sl=True)
                shaders = cmds.ls(sl=True)
                om.MGlobal.displayInfo("Running checkers on selected objects")
            else: # If there is no selection, check all the objects
                sel = cmds.ls(type='transform')
                textures = cmds.ls(type='file')
                shaders = cmds.ls(type='shadingEngine')
                om.MGlobal.displayInfo("Running checkers on all objects")
        else:
            return
        # Run the checks
        if empyt_checks:
            result = gc.check_empty_groups(sel) # Call the function to check for empty groups
            if result:
                text_print  = f"----> {result}"
                cmds.textScrollList(self.text_scroll_list, edit=True, append=["Next line contains the empty groups:"], font="boldLabelFont") # Add the text to the console
                cmds.textScrollList(self.text_scroll_list, edit=True, append=[text_print])
            else:
                cmds.textScrollList(self.text_scroll_list, edit=True, append=["No empty groups found"], font="boldLabelFont")

        if history_checks:
            result = gc.check_node_hisotry(sel) # Call the function to check for nodes with history
            if result:
                text_print  = f"----> {result}"
                cmds.textScrollList(self.text_scroll_list, edit=True, append=["Next line contains the nodes with history:"], font="boldLabelFont") # Add the text to the console
                cmds.textScrollList(self.text_scroll_list, edit=True, append=[text_print])
            else:
                cmds.textScrollList(self.text_scroll_list, edit=True, append=["No nodes with history found"], font="boldLabelFont")

        if unnused_sh_checks:
            if shaders:
                result = gc.check_unnused_shaders(shaders) # Call the function to check for unnused shaders
                if result:
                    text_print  = f"----> {result}"
                    cmds.textScrollList(self.text_scroll_list, edit=True, append=["Next line contains the unnused shaders:"], font="boldLabelFont") # Add the text to the console
                    cmds.textScrollList(self.text_scroll_list, edit=True, append=[text_print])
                else:
                    cmds.textScrollList(self.text_scroll_list, edit=True, append=["No unnused shaders found"], font="boldLabelFont")
            
            else:
                om.MGlobal.displayError("No shaders found")

        if unnused_tx_checks:
            if textures:
                result = gc.check_unnused_textures(textures) # Call the function to check for unnused textures
                if result:
                    text_print  = f"----> {result}"
                    cmds.textScrollList(self.text_scroll_list, edit=True, append=["Next line contains the unnused textures:"], font="boldLabelFont") # Add the text to the console
                    cmds.textScrollList(self.text_scroll_list, edit=True, append=[text_print])
                else:
                    cmds.textScrollList(self.text_scroll_list, edit=True, append=["No unnused textures found"], font="boldLabelFont")
            else:
                om.MGlobal.displayError("No textures found")

    def naming_module_caller(self):
        """
        Call the module that contains the naming checks functions

        Args:
            self: The class instance
        """

        export_data = self.get_query_export_tab()

       


        # Get the checkboxes values
        naming_checks = cmds.checkBoxGrp(self.naming_checks_checkbox, query=True, value1=True)
        duplicated_checks = cmds.checkBoxGrp(self.naming_checks_checkbox, query=True, value2=True)
        pasted_checks = cmds.checkBoxGrp(self.naming_checks_checkbox, query=True, value3=True)
        namespace_checks = cmds.checkBoxGrp(self.naming_checks_checkbox, query=True, value4=True)

        if naming_checks or duplicated_checks or pasted_checks or namespace_checks:
            
            if cmds.ls(sl=True): # Check if there is a selection
                sel = cmds.ls(sl=True)
                pasted_sel = cmds.ls(sl=True)
                om.MGlobal.displayInfo("Running checkers on selected objects")
            else: # If there is no selection, check all the objects
                sel = cmds.ls(type='transform')
                pasted_sel = cmds.ls(transforms=True, textures=True, shapes=False)
                om.MGlobal.displayInfo("Running checkers on all objects")
        
        else:
            return

        # Run the checks

        if naming_checks:
            result = nc.check_naming_structure(sel, export_data) # Call the function to check for namings
            if result:
                text_print  = f"----> {result}"
                cmds.textScrollList(self.text_scroll_list, edit=True, append=["Next line contains the nodes with wrong naming:"], font="boldLabelFont") # Add the text to the console
                cmds.textScrollList(self.text_scroll_list, edit=True, append=[text_print])
            else:
                cmds.textScrollList(self.text_scroll_list, edit=True, append=["All names seems correct"], font="boldLabelFont")

            
        if duplicated_checks:
            result = nc.duplicated_names(sel)
            if result:
                text_print  = f"----> {result}"
                cmds.textScrollList(self.text_scroll_list, edit=True, append=["Next line contains the duplicated names:"], font="boldLabelFont") # Add the text to the console
                cmds.textScrollList(self.text_scroll_list, edit=True, append=[text_print])
            else:
                cmds.textScrollList(self.text_scroll_list, edit=True, append=["No duplicated names found"], font="boldLabelFont")
           

        if pasted_checks:
            result = nc.check_pasted_nodes(pasted_sel)
            if result:
                text_print  = f"----> {result}"
                cmds.textScrollList(self.text_scroll_list, edit=True, append=["Next line contains the pasted nodes:"], font="boldLabelFont") # Add the text to the console
                cmds.textScrollList(self.text_scroll_list, edit=True, append=[text_print])
            else:
                cmds.textScrollList(self.text_scroll_list, edit=True, append=["No pasted nodes found"], font="boldLabelFont")

        if namespace_checks:
            result = nc.check_namespaces(pasted_sel)
            if result:
                text_print  = f"----> {result}"
                cmds.textScrollList(self.text_scroll_list, edit=True, append=["Next line contains the nodes with namespaces:"], font="boldLabelFont") # Add the text to the console
                cmds.textScrollList(self.text_scroll_list, edit=True, append=[text_print])
            else:
                cmds.textScrollList(self.text_scroll_list, edit=True, append=["No nodes with namespace found"], font="boldLabelFont")

    def model_module_caller(self):
        """
        Call the module that contains the model checker functions

        Args:
            self: The class instance
        """


        
        # Get the checkboxes values
        object_freezed_checks = cmds.checkBoxGrp(self.model_checks_01_checkbox, query=True, value1=True)
        pivots_checks = cmds.checkBoxGrp(self.model_checks_01_checkbox, query=True, value2=True)
        ngons_checks = cmds.checkBoxGrp(self.model_checks_01_checkbox, query=True, value3=True)
        non_manifold_checks = cmds.checkBoxGrp(self.model_checks_01_checkbox, query=True, value4=True)

        if object_freezed_checks or pivots_checks or ngons_checks or non_manifold_checks:
            if cmds.ls(sl=True):
                sel = cmds.ls(sl=True)
                om.MGlobal.displayInfo("Running checkers on selected objects")
            else:
                sel = cmds.ls(type='transform')
                om.MGlobal.displayInfo("Running checkers on all objects")
        else:
            return

        # Run the checks
        if object_freezed_checks:
            result = mc.check_object_unfreezed(sel)
            if result:
                text_print  = f"----> {result}"
                cmds.textScrollList(self.text_scroll_list, edit=True, append=["Next line contains the freezed objects:"], font="boldLabelFont") # Add the text to the console
                cmds.textScrollList(self.text_scroll_list, edit=True, append=[text_print]) 
            else:
                cmds.textScrollList(self.text_scroll_list, edit=True, append=["No freezed objects found"], font="boldLabelFont")
        
        if pivots_checks:
            result = mc.check_pivots(sel)
            if result:
                text_print  = f"----> {result}"
                cmds.textScrollList(self.text_scroll_list, edit=True, append=["Next line contains the objects with non-centered pivots:"], font="boldLabelFont") # Add the text to the console
                cmds.textScrollList(self.text_scroll_list, edit=True, append=[text_print])
            else:
                cmds.textScrollList(self.text_scroll_list, edit=True, append=["No objects with non-centered pivots found"], font="boldLabelFont")
        
        if ngons_checks:
            result = mc.check_ngons(sel)
            if result:
                text_print  = f"----> {result}"
                cmds.textScrollList(self.text_scroll_list, edit=True, append=["Next line contains the objects with n-gons:"], font="boldLabelFont") # Add the text to the console
                cmds.textScrollList(self.text_scroll_list, edit=True, append=[text_print])
            else:
                cmds.textScrollList(self.text_scroll_list, edit=True, append=["No objects with n-gons found"], font="boldLabelFont")
        
        if non_manifold_checks:
            result = mc.check_non_manifold(sel)
            if result:
                text_print  = f"----> {result}"
                cmds.textScrollList(self.text_scroll_list, edit=True, append=["Next line contains the objects with non-manifold geometry:"], font="boldLabelFont") # Add the text to the console
                cmds.textScrollList(self.text_scroll_list, edit=True, append=[text_print])
            else:
                cmds.textScrollList(self.text_scroll_list, edit=True, append=["No objects with non-manifold geometry found"], font="boldLabelFont")

                                                                              
    def module_caller(self, *args):
        """
        Call the module that contains the model checker functions

        Args:
            self: The class instance
            Args: The arguments passed to the function by the UI
        """

        # Clear the console
        cmds.textScrollList(self.text_scroll_list, edit=True, removeAll=True)

        # Call the general checks module
        self.general_module_caller()

        self.naming_module_caller()

        self.model_module_caller()

    def clear_console(self, *args):
        """
        Clear the console output

        Args:
            self: The class instance
            Args: The arguments passed to the function by the UI
        """
        # Clear the console
        cmds.textScrollList(self.text_scroll_list, edit=True, removeAll=True)
        om.MGlobal.displayInfo("Console cleared")

    def check_all_action(self, *args):
        """
        Check all the checkboxes

        Args:
            self: The class instance
            Args: The arguments passed to the function by the UI
        """

        # Check all the checkboxes
        cmds.checkBoxGrp(self.general_checks_checkbox, edit=True, valueArray4=[True, True, True, True])

        cmds.checkBoxGrp(self.naming_checks_checkbox, edit=True, valueArray4=[True, True, True, True])

        cmds.checkBoxGrp(self.model_checks_01_checkbox, edit=True, valueArray4=[True, True, True, True])


    def uncheck_all_action(self, *args):
        """
        Uncheck all the checkboxes

        Args:
            self: The class instance
            Args: The arguments passed to the function by the UI
        """
         
        # Uncheck all the checkboxes
        cmds.checkBoxGrp(self.general_checks_checkbox, edit=True, valueArray4=[False, False, False, False])

        cmds.checkBoxGrp(self.naming_checks_checkbox, edit=True, valueArray4=[False, False, False, False])

        cmds.checkBoxGrp(self.model_checks_01_checkbox, edit=True, valueArray4=[False, False, False, False])


    def model_checker_tab_ui(self):
        """
        Create the UI for the model checker tab

        Args:
            self: The class instance
        """
        
        # Create the model checker tab
        self.checker_tab = cmds.columnLayout(adjustableColumn=True, parent=self.tabs)

        cmds.separator(parent=self.checker_tab, style='doubleDash', height=10)

        cmds.text(label="Select the checks you want to perform", parent=self.checker_tab)

        cmds.separator(parent=self.checker_tab, style='none', height=10)

        # Create the frame for general checks
        general_frame = cmds.frameLayout(label="General", collapsable=True, parent=self.checker_tab, statusBarMessage="Get the options for general checks")

        general_form_layout = cmds.formLayout(parent=general_frame)
        # Create the checkboxes for the general checks
        self.general_checks_checkbox = cmds.checkBoxGrp(numberOfCheckBoxes=4, 
                                                labelArray4=["Check Empty Group", "Check Node History", "Check Unused Shader", "Check Unused Texture"], 
                                                parent=general_form_layout, 
                                                columnAlign=(1, 'left'), 
                                                vertical=True,
                                                columnWidth=[(1, 200)])
        
        cmds.formLayout(general_form_layout, edit=True, attachForm=[(self.general_checks_checkbox, 'left', 20), (self.general_checks_checkbox, 'top', 5)])

        cmds.separator(parent=self.checker_tab, style='none', height=10)          


        # Create the frame for naming checks
        naming_frame = cmds.frameLayout(label="Naming", collapsable=True, parent=self.checker_tab, statusBarMessage="Get the options for naming checks")

        naming_form_layout = cmds.formLayout(parent=naming_frame)
        # Create the checkboxes for the naming checks
        self.naming_checks_checkbox = cmds.checkBoxGrp(numberOfCheckBoxes=4, 
                                                labelArray4=["Check Namings", "Check Duplicated Names", "Check Pasted Nodes", "Check Namespace"], 
                                                parent=naming_form_layout, 
                                                columnAlign=(1, 'left'), 
                                                vertical=True,
                                                columnWidth=[(1, 200)])
        
        cmds.formLayout(naming_form_layout, edit=True, attachForm=[(self.naming_checks_checkbox, 'left', 20), (self.naming_checks_checkbox, 'top', 5)])

        cmds.separator(parent=self.checker_tab, style='none', height=10)        

        # Create the frame for model checks
        model_frame = cmds.frameLayout(label="Model", collapsable=True, parent=self.checker_tab, statusBarMessage="Get the options for model checks")

        model_form_layout = cmds.formLayout(parent=model_frame)

        # Create the checkboxes for the model checks
        self.model_checks_01_checkbox = cmds.checkBoxGrp(numberOfCheckBoxes=4, 
                                                labelArray4=["Check Object Freezed", "Check Pivots", "Check N-Gons", "Check non-manifold geometry"], 
                                                parent=model_form_layout, 
                                                columnAlign=(1, 'left'), 
                                                vertical=True,
                                                columnWidth=[(1, 200)])

        cmds.formLayout(model_form_layout, edit=True, attachForm=[(self.model_checks_01_checkbox, 'left', 20), (self.model_checks_01_checkbox, 'top', 5)])

        cmds.separator(parent=self.checker_tab, style='none', height=10)        

        # Create the frame for the output console
        output_console_label = cmds.text(label="OUTPUT CONSOLE", parent=self.checker_tab, font="boldLabelFont", height=30)

        # Create console output
        self.text_scroll_list = cmds.textScrollList(parent=self.checker_tab, allowMultiSelection=True)

        cmds.separator(parent=self.checker_tab, style='none', height=10)

        final_buttons_form = cmds.formLayout(parent=self.checker_tab)

        # Create the buttons for the model checker tab
        check_all_button = cmds.button(label="Check All", parent=final_buttons_form, command=self.check_all_action)
        unchecked_all_button = cmds.button(label="Uncheck All", parent=final_buttons_form, command=self.uncheck_all_action)
        export_log_button = cmds.button(label="Export Log", parent=final_buttons_form, command=self.export_log) 
        run_checker_button = cmds.button(label="Run Checkers", parent=final_buttons_form, command=self.module_caller)
        select_errors_button = cmds.button(label="Select Errors", parent=final_buttons_form, command=self.select_errors)
        clear_console = cmds.button(label="Clear console", parent=final_buttons_form, command=self.clear_console)


        cmds.formLayout(final_buttons_form, edit=True, attachForm=[(check_all_button, 'left', 5), (check_all_button, 'bottom', 5),
                                                                (export_log_button, 'right', 5), (export_log_button, 'bottom', 5),
                                                                (unchecked_all_button, 'left', 70), (unchecked_all_button, 'bottom', 5),
                                                                (select_errors_button, 'left', 150), (select_errors_button, 'bottom', 5),
                                                                (run_checker_button, 'right', 80), (run_checker_button, 'bottom', 5),
                                                                (clear_console, 'right', 170), (clear_console, 'bottom', 5),
                                                                ])

    def export_json_button(self, *args):
        """
        Export the JSON file

        Args:
            self: The class instance
            Args: The arguments passed to the function by the UI
        """


        export_data = self.get_query_export_tab()

        # Export the data to a JSON file
        radio_query = cmds.radioButtonGrp(self.export_checkBox, query=True, select=True)

        if radio_query == 1:
            json_path = os.path.join(self.default_path, "json_data")
            base_file_path = os.path.join(self.default_path, "json_data/naming_convention_01.json")
            counter = 1
            while os.path.exists(base_file_path):
                base_file_path = os.path.join(json_path, f"naming_convention_{str(counter).zfill(2)}.json")
                counter += 1
            file_path = base_file_path
            
        else:
            file_path = cmds.fileDialog2(fileFilter="JSON Files (*.json)", dialogStyle=2, fileMode=0)[0]

        if file_path:
            try:
                with open(file_path, 'w') as json_file: # Open the JSON file
                    json.dump(export_data, json_file, indent=4)


                om.MGlobal.displayInfo(f"Exported configuration to {file_path}")
            except PermissionError:
                om.MGlobal.displayError(f"Permission denied: {file_path}")
                new_file_path = cmds.fileDialog2(fileFilter="JSON Files (*.json)", dialogStyle=2, fileMode=0)[0] # Open the file dialog
                if new_file_path:
                    with open(new_file_path, 'w') as json_file:
                        json.dump(export_data, json_file, indent=4)
                    om.MGlobal.displayInfo(f"Exported configuration to {new_file_path}")
                else:
                    om.MGlobal.displayError("Export cancelled")
        else:
            om.MGlobal.displayError("Export cancelled")

    def get_query_export_tab(self):
        """
        Get the query from the export tab

        Args:
            self: The class instance
        """
        # Get the query from the export tab
        transforms_type_suffix = cmds.optionMenuGrp(self.transforms_option_menu, query=True, value=True)
        meshes_type_suffix = cmds.optionMenuGrp(self.meshes_option_menu, query=True, value=True)
        joints_type_suffix = cmds.optionMenuGrp(self.joints_option_menu, query=True, value=True)
        locators_type_suffix = cmds.optionMenuGrp(self.locators_option_menu, query=True, value=True)
        clusters_type_suffix = cmds.optionMenuGrp(self.clusters_option_menu, query=True, value=True)
        lights_type_suffix = cmds.optionMenuGrp(self.lights_option_menu, query=True, value=True)
        right_side = cmds.optionMenuGrp(self.right_option_menu, query=True, value=True)
        center_side = cmds.optionMenuGrp(self.center_option_menu, query=True, value=True)
        left_side = cmds.optionMenuGrp(self.left_option_menu, query=True, value=True)
        names = ["Transforms", "Meshes", "Joints", "Locators", "Clusters", "Lights"]
        type_suffix_count = 0
        for i, type_suffix in enumerate([transforms_type_suffix, meshes_type_suffix, joints_type_suffix, locators_type_suffix, clusters_type_suffix, lights_type_suffix]):
            if not type_suffix:
                om.MGlobal.displayError(f"No {names[i]} type_suffix selected")
                return
            else:
                type_suffix_count += 1

        names = ["Left", "Center", "Right"]
        side_count = 0
        for i, side in enumerate([left_side, center_side, right_side]):
            if not side:
                om.MGlobal.displayError(f"No {names[i]} side selected")
                return
            else:
                side_count += 1

        naming_convention = cmds.textField(self.naming_text_field, query=True, text=True) # Get the naming convention

        # Split the naming convention
        if naming_convention:
            splited_naming_convention = naming_convention.split("_")
            parts_splited = []
            if len(splited_naming_convention) > 4:
                om.MGlobal.displayError("Naming convention is too long, decrease the separators")

            else:
                for part in splited_naming_convention:
                    if "><" in part:
                        part_splited = part.split("><")
                        temp_split = []
                        for i in part_splited:
                            part_splited_renamed = i.replace("<", "").replace(">", "")
                            temp_split.append(part_splited_renamed)
                        parts_splited.append(temp_split)
                    else:
                        parts_splited.append(part.replace("<", "").replace(">", ""))

        else:
            om.MGlobal.displayError("No naming convention set")
            return

        # Create the export data
        if parts_splited and type_suffix_count == 6 and side_count == 3:
            export_data = {
                "type_suffix": { "Transforms": transforms_type_suffix, "Meshes": meshes_type_suffix, "Joints": joints_type_suffix, "Locators": locators_type_suffix, "Clusters": clusters_type_suffix, "Lights": lights_type_suffix },
                "NamingConvention": parts_splited,
                "side": { "Left": left_side, "Center": center_side, "Right": right_side },
            }
        return export_data

    def load_config(self, *args):
        """
        Load the config file

        Args:
            self: The class instance
            Args: The arguments passed to the function by the UI
        """

        # Load the config file
        text_query = cmds.textField(self.text_field, query=True, text=True)

        if text_query:
            self.custom_config = text_query

            # Open the JSON file
            with open(self.custom_config, 'r') as json_file:
                config_data = json.load(json_file)

            # Set the values from the JSON file
            for key, value in config_data.items():
                if key == "type_suffix":
                    for key, value in value.items():
                        if key == "Transforms":
                            cmds.optionMenuGrp(self.transforms_option_menu, edit=True, value=value)
                        if key == "Meshes":
                            cmds.optionMenuGrp(self.meshes_option_menu, edit=True, value=value)
                        if key == "Joints":
                            cmds.optionMenuGrp(self.joints_option_menu, edit=True, value=value)
                        if key == "Locators":
                            cmds.optionMenuGrp(self.locators_option_menu, edit=True, value=value)
                        if key == "Clusters":
                            cmds.optionMenuGrp(self.clusters_option_menu, edit=True, value=value)
                        if key == "Lights":
                            cmds.optionMenuGrp(self.lights_option_menu, edit=True, value=value)
                if key == "NamingConvention":
                    final_text = ""
                    for i, items in enumerate(value):
                        if isinstance(items, str):
                            renamed_item = f"<{items}>"
                            final_text += renamed_item
                        else:

                            for item in items:
                                renamed_item = f"<{item}>"
                                final_text += renamed_item
                        if i != len(value) - 1:
                            final_text += "_"
                    cmds.textField(self.naming_text_field, edit=True, text=final_text)
                if key == "side":
                    for key, value in value.items():
                        if key == "Left":
                            cmds.optionMenuGrp(self.left_option_menu, edit=True, value=value)
                        if key == "Center":
                            cmds.optionMenuGrp(self.center_option_menu, edit=True, value=value)
                        if key == "Right":
                            cmds.optionMenuGrp(self.right_option_menu, edit=True, value=value)



            om.MGlobal.displayInfo(f"Config file loaded: {text_query}")


        else:
            om.MGlobal.displayError("No file selected")

    def file_dialog(self, *args):
        """
        Open a file dialog

        Args:
            self: The class instance
            Args: The arguments passed to the function by the UI
        """

        # Open a file dialog
        self.json_path = cmds.fileDialog2(fileFilter="JSON Files (*.json)", dialogStyle=2, fileMode=1)

        if self.json_path:
            cmds.textField(self.text_field, edit=True, text=self.json_path[0])

    def insert_keyword(self, keyword, naming_text_field, *args):
        """
        Insert the selected keyword into the text field.
        
        Args:
            self: The class instance
            keyword: The keyword to insert
            naming_text_field: The text field to insert the keyword
            Args: The arguments passed to the function by the UI
        """

        # Get the current text from the text field
        current_text = cmds.textField(naming_text_field, query=True, text=True)
        
        # Update the text field with the keyword appended
        new_text = current_text + keyword
        cmds.textField(naming_text_field, edit=True, text=new_text)

    def export_tab_ui(self):
        """
        Create the UI for the export tab

        Args:
            self: The class instance
        """

        # Create the export tab
        self.export_tab = cmds.columnLayout(adjustableColumn=True, parent=self.tabs)

        cmds.separator(parent=self.export_tab, style='none', height=10)

        cmds.text(label="Set all the desire configuration", parent=self.export_tab)

        cmds.separator(parent=self.export_tab, style='none', height=10)

        # Create the frame for the naming convention
        path_form_layout = cmds.formLayout(parent=self.export_tab)   

        # Create the text field for the naming convention
        list_json_files = cmds.getFileList(folder=os.path.join(self.default_path, "json_data"), filespec="*.json")
        list_json_files.sort(reverse=True)
        highest_json = os.path.join(self.default_path, "json_data", list_json_files[0])

        # Create the text field for the path
        folder_button = cmds.iconTextButton("folder_button", st="iconOnly", h=20, backgroundColor=(0.3, 0.3, 0.3), image=":/folder-open.png", ebg=True, parent = path_form_layout)
        self.text_field = cmds.textField("text_field",text=highest_json, h=20, w=500, bgc=(0.3, 0.3, 0.3), parent = path_form_layout, )
        load_button = cmds.button("load_button", label="Load Config", parent=path_form_layout, command=self.load_config)

        cmds.iconTextButton(folder_button, edit=True, command=self.file_dialog)

        cmds.formLayout(path_form_layout, edit=True, attachForm=[(folder_button, 'left', 5), (folder_button, 'top', 5),
                                                                (self.text_field, 'top', 5),
                                                                (load_button, 'right', 5), (load_button, 'top', 5)],
                        attachControl=[(self.text_field, 'left', 5, folder_button), (self.text_field, 'right', 5, load_button)])

        cmds.separator(parent=self.export_tab, style='none', height=10)

        # Create the frame for the naming convention
        cmds.text(label="NAMING CONVENTION CONFIG", parent=self.export_tab, font="boldLabelFont")

        cmds.separator(parent=self.export_tab, style='none', height=10)

        type_suffix_form_layout = cmds.formLayout(parent=self.export_tab)

       # Create the option menus for the naming convention

        # ------- LEFT ------- #

        self.transforms_option_menu = cmds.optionMenuGrp(parent=type_suffix_form_layout, label="Transforms", columnWidth2=[100, 100], columnAlign2=["left", "left"])
        cmds.menuItem(label="GRP")
        cmds.menuItem(label="grp")
        cmds.menuItem(label="TRN")
        cmds.menuItem(label="trn")

        self.meshes_option_menu = cmds.optionMenuGrp(parent=type_suffix_form_layout, label="Meshes", columnWidth2=[100, 100], columnAlign2=["left", "left"])
        cmds.menuItem(label="MSH")
        cmds.menuItem(label="mesh")
        cmds.menuItem(label="GEO")
        cmds.menuItem(label="geo")


        self.joints_option_menu = cmds.optionMenuGrp(parent=type_suffix_form_layout, label="Joints", columnWidth2=[100, 100], columnAlign2=["left", "left"])
        cmds.menuItem(label="JNT")
        cmds.menuItem(label="jnt")

        # ------- RIGHT ------- #

        self.locators_option_menu = cmds.optionMenuGrp(parent=type_suffix_form_layout, label="Locators", columnWidth2=[100, 100], columnAlign2=["left", "left"])
        cmds.menuItem(label="LOC")
        cmds.menuItem(label="loc")


        self.clusters_option_menu = cmds.optionMenuGrp(parent=type_suffix_form_layout, label="Clusters", columnWidth2=[100, 100], columnAlign2=["left", "left"])
        cmds.menuItem(label="CLS")
        cmds.menuItem(label="cls")
        cmds.menuItem(label="CLU")
        cmds.menuItem(label="clu")

        self.lights_option_menu = cmds.optionMenuGrp(parent=type_suffix_form_layout, label="Lights", columnWidth2=[100, 100], columnAlign2=["left", "left"])
        cmds.menuItem(label="LGT")
        cmds.menuItem(label="lgt")
        cmds.menuItem(label="LTI")
        cmds.menuItem(label="lti")

        # ------- CENTER ------- #

        self.left_option_menu = cmds.optionMenuGrp(parent=type_suffix_form_layout, label="Left", columnWidth2=[100, 100], columnAlign2=["left", "left"])
        cmds.menuItem(label="L")
        cmds.menuItem(label="l")
        cmds.menuItem(label="Left")
        cmds.menuItem(label="left")

        self.center_option_menu = cmds.optionMenuGrp(parent=type_suffix_form_layout, label="Center", columnWidth2=[100, 100], columnAlign2=["left", "left"])
        cmds.menuItem(label="C")
        cmds.menuItem(label="c")
        cmds.menuItem(label="Center")
        cmds.menuItem(label="center")

        self.right_option_menu = cmds.optionMenuGrp(parent=type_suffix_form_layout, label="Right", columnWidth2=[100, 100], columnAlign2=["left", "left"])
        cmds.menuItem(label="R")
        cmds.menuItem(label="r")
        cmds.menuItem(label="Right")
        cmds.menuItem(label="right")


        # Attach the form layout
        cmds.formLayout(type_suffix_form_layout, edit=True, attachForm=[
            (self.transforms_option_menu, 'left', 50), (self.transforms_option_menu, 'top', 25),
            (self.meshes_option_menu, 'left', 50), (self.meshes_option_menu, 'top', 55),
            (self.joints_option_menu, 'left', 50), (self.joints_option_menu, 'top', 85),
            (self.locators_option_menu, 'right', 50), (self.locators_option_menu, 'top', 25),
            (self.clusters_option_menu, 'right', 50), (self.clusters_option_menu, 'top', 55),
            (self.lights_option_menu, 'right', 50), (self.lights_option_menu, 'top', 85),
            (self.left_option_menu, 'left', 130), (self.left_option_menu, 'top', 125),
            (self.center_option_menu, 'left', 350), (self.center_option_menu, 'top', 125),
            (self.right_option_menu, 'left', 580), (self.right_option_menu, 'top', 125)
            
        ])

        cmds.separator(parent=self.export_tab, style='none', height=30)

        naming_form_layout = cmds.formLayout(parent=self.export_tab)

        # Create the text field
        naming_text = cmds.text(label="Naming convention", parent=naming_form_layout)
        self.naming_text_field = cmds.textField("textFieldWithPopup", text="<Side>_<Name><Tile>_<Type>", parent=naming_form_layout, width=100)
        
        # Attach a popup menu to the text field
        cmds.popupMenu("popupMenu", parent=self.naming_text_field)
        
        # Add menu items to the popup menu
        keywords = ["<Side>", "<Name>", "<Tile>", "<Type>", "<CatClark>", "_"]
        for keyword in keywords:
            cmds.menuItem(label=keyword, command=partial(self.insert_keyword, keyword, self.naming_text_field))

        # Attach the form layout
        cmds.formLayout(naming_form_layout, edit=True, attachForm=[
            (naming_text, 'left', 50), (naming_text, 'top', 5),
            (self.naming_text_field, 'left', 175), (self.naming_text_field, 'top', 5),
            (self.naming_text_field, 'right', 50)
        ])     

        # Create the separator
        cmds.separator(parent=self.export_tab, style='none', height=10)

        export_form_layout = cmds.formLayout(parent=self.export_tab)
        self.export_checkBox = cmds.radioButtonGrp(numberOfRadioButtons=2, labelArray2=["Default Path", "Custom Path"], parent=export_form_layout, columnAlign=(1, 'left'), select=1, vertical=True)
        export_button = cmds.button(label="Export JSON", parent=export_form_layout, command=self.export_json_button)

        # Attach the form layout
        cmds.formLayout(export_form_layout, edit=True, attachForm=[
            (self.export_checkBox, 'left', 50), (self.export_checkBox, 'top', 5),
            (export_button, 'left', 250), (export_button, 'top', 10),
            (export_button, 'right', 50)

        ])

    def create_ui(self, main_path):
        """
        Create the main UI for the model checker tool

        Args:
            self: The class instance
        """

        self.default_path = main_path

        # Check if the window already exists and delete it
        if cmds.window("modelCheckerUI", exists=True):
            cmds.deleteUI("modelCheckerUI", window=True)
        
        # Create the main window
        window = cmds.window("modelCheckerUI", title="Model Checker", widthHeight=(300, 200), menuBar=True, resizeToFitChildren=True)
        column_layout = cmds.columnLayout(adjustableColumn=True)

        form_layout = cmds.formLayout(parent=column_layout)    
        text_label = cmds.text(label="Model Checker Tool", parent=form_layout)
        # Create the help button
        help_button = cmds.button(label="Tool Help", command=partial(webbrowser.open, "https://github.com/GuiidoGC/model_checker"), parent=form_layout)
        
        cmds.formLayout(form_layout, edit=True, attachForm=[(text_label, 'left', 5), (text_label, 'top', 10),
                                                            (help_button, 'right', 5), (help_button, 'top', 5)])
        

        cmds.separator(parent=column_layout, style='none', height=10)

        # Create the tabs for the model checker tool
        self.tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=25, parent=column_layout)
        # Create the model checker tab
        self.model_checker_tab_ui()
        # Create the export tab
        self.export_tab_ui()
    
        # Set the tab labels
        cmds.tabLayout(self.tabs, edit=True, tabLabel=((self.checker_tab, "Model checker"), (self.export_tab, "Config")))

        text_layout = cmds.formLayout(parent=column_layout)  
        copy_right = cmds.text(label="Copyright (c) 2025, Guido Gonzalez. All rights reserved.", parent=text_layout, height=15)
        version_text = cmds.text(label="Version 1.0.0", parent=text_layout, height=15)

        cmds.formLayout(text_layout, edit=True, attachForm=[(copy_right, 'left', 5), (copy_right, 'bottom', 10),
                                                            (version_text, 'right', 5), (version_text, 'bottom', 5)])
        


        cmds.showWindow(window)


# ModelCheckerUI().create_ui()

