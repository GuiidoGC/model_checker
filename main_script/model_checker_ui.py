import maya.cmds as cmds
import maya.OpenMaya as om
from functools import partial
import general_checks as gc
from importlib import reload
import json
import os
import webbrowser
reload(gc)

class ModelCheckerUI():
    """
    Class to create the UI for the model checker tool
    """

    def general_module_caller(self, *args):
        """
        Call the module that contains the general checks functions

        Args:
            self: The class instance
            Args: The arguments passed to the function by the UI
        """

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

        # Get the checkboxes values
        empyt_checks = cmds.checkBoxGrp(self.general_checks_checkbox, query=True, value1=True)
        history_checks = cmds.checkBoxGrp(self.general_checks_checkbox, query=True, value2=True)
        unnused_sh_checks = cmds.checkBoxGrp(self.general_checks_checkbox, query=True, value3=True)
        unnused_tx_checks = cmds.checkBoxGrp(self.general_checks_checkbox, query=True, value4=True)

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

    def query_console(self, *args):
        """
        Query the console output

        Args:
            self: The class instance
            Args: The arguments passed to the function by the UI
        """

        # Query the console output
        console_output = cmds.textScrollList(self.text_scroll_list, query=True, allItems=True)
        print(console_output)

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

        cmds.checkBoxGrp(self.model_checks_02_checkbox, edit=True, valueArray3=[True, True, True])

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

        cmds.checkBoxGrp(self.model_checks_02_checkbox, edit=True, valueArray3=[False, False, False])

    def model_checker_tab_ui(self):
        """
        Create the UI for the model checker tab

        Args:
            self: The class instance
        """
        
        # Create the model checker tab
        self.checker_tab = cmds.columnLayout(adjustableColumn=True, parent=self.tabs)

        cmds.separator(parent=self.checker_tab, style='none', height=10)

        cmds.text(label="Select the checks you want to perform", parent=self.checker_tab)

        cmds.separator(parent=self.checker_tab, style='none', height=10)

        # Create the frame for general checks
        general_frame = cmds.frameLayout(label="General", collapsable=True, parent=self.checker_tab, statusBarMessage="Get the options for general checks")

        form_layout = cmds.formLayout(parent=general_frame)
        # Create the checkboxes for the general checks
        self.general_checks_checkbox = cmds.checkBoxGrp(numberOfCheckBoxes=4, 
                                                labelArray4=["Check Empty Group", "Check Node History", "Check Unused Shader", "Check Unused Texture"], 
                                                parent=form_layout, 
                                                columnAlign=(1, 'left'), 
                                                vertical=True,
                                                columnWidth=[(1, 200)])
        
        cmds.formLayout(form_layout, edit=True, attachForm=[(self.general_checks_checkbox, 'left', 20), (self.general_checks_checkbox, 'top', 5)])

        cmds.separator(parent=self.checker_tab, style='none', height=10)          


        # Create the frame for naming checks
        naming_frame = cmds.frameLayout(label="Naming", collapsable=True, parent=self.checker_tab, statusBarMessage="Get the options for naming checks")

        form_layout = cmds.formLayout(parent=naming_frame)
        # Create the checkboxes for the naming checks
        self.naming_checks_checkbox = cmds.checkBoxGrp(numberOfCheckBoxes=4, 
                                                labelArray4=["Check Namings", "Check Duplicated Names", "Check Pasted Nodes", "Check Namespace"], 
                                                parent=form_layout, 
                                                columnAlign=(1, 'left'), 
                                                vertical=True,
                                                columnWidth=[(1, 200)])
        
        cmds.formLayout(form_layout, edit=True, attachForm=[(self.naming_checks_checkbox, 'left', 20), (self.naming_checks_checkbox, 'top', 5)])

        cmds.separator(parent=self.checker_tab, style='none', height=10)        

        # Create the frame for model checks
        model_frame = cmds.frameLayout(label="Model", collapsable=True, parent=self.checker_tab, statusBarMessage="Get the options for model checks")

        form_layout = cmds.formLayout(parent=model_frame)
        # Create the checkboxes for the model checks
        self.model_checks_01_checkbox = cmds.checkBoxGrp(numberOfCheckBoxes=4, 
                                                labelArray4=["Check Object Freezed", "Check Pivots", "Check Cv's Position", "Check N-Gons"], 
                                                parent=form_layout, 
                                                columnAlign=(1, 'left'), 
                                                vertical=True,
                                                columnWidth=[(1, 200)])
        
        self.model_checks_02_checkbox = cmds.checkBoxGrp(numberOfCheckBoxes=3, 
                                                labelArray3=["Check Triangles", "Check Symmetry", "Check non-manifold geometry"], 
                                                parent=form_layout, 
                                                columnAlign=(1, 'left'), 
                                                vertical=True,
                                                columnWidth=[(1, 200)])




        cmds.formLayout(form_layout, edit=True, attachForm=[(self.model_checks_01_checkbox, 'left', 20), (self.model_checks_01_checkbox, 'top', 5),
                                                            (self.model_checks_02_checkbox, 'left', 20), (self.model_checks_02_checkbox, 'top', 72),])

        cmds.separator(parent=self.checker_tab, style='none', height=10)        


        output_console_label = cmds.text(label="OUTPUT CONSOLE", parent=self.checker_tab, font="boldLabelFont", height=30)

        # Create console output
        self.text_scroll_list = cmds.textScrollList(parent=self.checker_tab, allowMultiSelection=True)

        cmds.separator(parent=self.checker_tab, style='none', height=10)

        final_buttons_form = cmds.formLayout(parent=self.checker_tab)

        # Create the buttons for the model checker tab
        check_all_button = cmds.button(label="Check All", parent=final_buttons_form, command=self.check_all_action)
        unchecked_all_button = cmds.button(label="Uncheck All", parent=final_buttons_form, command=self.uncheck_all_action)
        export_log_button = cmds.button(label="Export Log", parent=final_buttons_form)
        run_checker_button = cmds.button(label="Run Checkers", parent=final_buttons_form, command=self.module_caller)
        select_errors_button = cmds.button(label="Select Errors", parent=final_buttons_form)
        clear_console = cmds.button(label="Clear console", parent=final_buttons_form, command=self.clear_console)


        cmds.formLayout(final_buttons_form, edit=True, attachForm=[(check_all_button, 'left', 5), (check_all_button, 'bottom', 5),
                                                                (export_log_button, 'right', 5), (export_log_button, 'bottom', 5),
                                                                (unchecked_all_button, 'left', 70), (unchecked_all_button, 'bottom', 5),
                                                                (select_errors_button, 'left', 150), (select_errors_button, 'bottom', 5),
                                                                (run_checker_button, 'right', 80), (run_checker_button, 'bottom', 5),
                                                                (clear_console, 'right', 170), (clear_console, 'bottom', 5),
                                                                ])

    def get_query_export_tab(self, *args):
        """
        Get the query from the export tab

        Args:
            self: The class instance
            Args: The arguments passed to the function by the UI
        """
        transforms_prefix = cmds.optionMenuGrp(self.transforms_option_menu, query=True, value=True)
        meshes_prefix = cmds.optionMenuGrp(self.meshes_option_menu, query=True, value=True)
        joints_prefix = cmds.optionMenuGrp(self.joints_option_menu, query=True, value=True)
        locators_prefix = cmds.optionMenuGrp(self.locators_option_menu, query=True, value=True)
        clusters_prefix = cmds.optionMenuGrp(self.clusters_option_menu, query=True, value=True)
        lights_prefix = cmds.optionMenuGrp(self.lights_option_menu, query=True, value=True)
        right_suffix = cmds.optionMenuGrp(self.right_option_menu, query=True, value=True)
        center_suffix = cmds.optionMenuGrp(self.center_option_menu, query=True, value=True)
        left_suffix = cmds.optionMenuGrp(self.left_option_menu, query=True, value=True)
        names = ["Transforms", "Meshes", "Joints", "Locators", "Clusters", "Lights"]
        prefix_count = 0
        for i, prefix in enumerate([transforms_prefix, meshes_prefix, joints_prefix, locators_prefix, clusters_prefix, lights_prefix]):
            if not prefix:
                om.MGlobal.displayError(f"No {names[i]} prefix selected")
                return
            else:
                prefix_count += 1

        names = ["Left", "Center", "Right"]
        suffix_count = 0
        for i, suffix in enumerate([left_suffix, center_suffix, right_suffix]):
            if not suffix:
                om.MGlobal.displayError(f"No {names[i]} suffix selected")
                return
            else:
                suffix_count += 1

        naming_convention = cmds.textField(self.naming_text_field, query=True, text=True)

        if naming_convention:
            splited_naming_convention = naming_convention.split("_")
            parts_splited = []
            if len(splited_naming_convention) > 4:
                om.MGlobal.displayError("Naming convention is too long, decrease the separators")

            else:
                temp_split = []
                for part in splited_naming_convention:
                    if "><" in part:
                        part_splited = part.split("><")
                        for i in part_splited:
                            part_splited_renamed = i.replace("<", "").replace(">", "")
                            temp_split.append(part_splited_renamed)
                        parts_splited.append(temp_split)
                    else:
                        parts_splited.append(part.replace("<", "").replace(">", ""))

        else:
            om.MGlobal.displayError("No naming convention set")
            return

        if parts_splited and prefix_count == 6 and suffix_count == 3:
            export_data = {
                "Prefix": { "Transforms": transforms_prefix, "Meshes": meshes_prefix, "Joints": joints_prefix, "Locators": locators_prefix, "Clusters": clusters_prefix, "Lights": lights_prefix },
                "NamingConvention": parts_splited,
                "Suffix": { "Left": left_suffix, "Center": center_suffix, "Right": right_suffix },
            }
        
        # Export the data to a JSON file
        # file_path = cmds.fileDialog2(fileFilter="JSON Files (*.json)", dialogStyle=2, fileMode=0)
        radio_query = cmds.radioButtonGrp(self.export_checkBox, query=True, select=True)

        if radio_query == 1:
            json_path = os.path.join(self.default_path, "json_data")
            base_file_path = os.path.join(self.default_path, "json_data/naming_convention.json")
            counter = 1
            while os.path.exists(base_file_path):
                base_file_path = os.path.join(json_path, f"naming_convention_{str(counter).zfill(2)}.json")
                counter += 1
            file_path = base_file_path
            
        else:
            file_path = cmds.fileDialog2(fileFilter="JSON Files (*.json)", dialogStyle=2, fileMode=0)

        print(file_path)

        if file_path:
            try:
                with open(file_path[0], 'w') as json_file:
                    json.dump(export_data, json_file, indent=4)
                om.MGlobal.displayInfo(f"Exported configuration to {file_path[0]}")
            except PermissionError:
                om.MGlobal.displayError(f"Permission denied: {file_path[0]}")
                new_file_path = cmds.fileDialog2(fileFilter="JSON Files (*.json)", dialogStyle=2, fileMode=0)
                if new_file_path:
                    with open(new_file_path[0], 'w') as json_file:
                        json.dump(export_data, json_file, indent=4)
                    om.MGlobal.displayInfo(f"Exported configuration to {new_file_path[0]}")
                else:
                    om.MGlobal.displayError("Export cancelled")
        else:
            om.MGlobal.displayError("Export cancelled")

        



    def load_config(self, *args):
        """
        Load the config file

        Args:
            self: The class instance
            Args: The arguments passed to the function by the UI
        """

        # Load the config file
        text_query = cmds.textField(self.text_field, query=True, text=True)
        print(text_query)

        if text_query:
            self.custom_config = text_query
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
        """Insert the selected keyword into the text field."""
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

        self.export_tab = cmds.columnLayout(adjustableColumn=True, parent=self.tabs)

        cmds.separator(parent=self.export_tab, style='none', height=10)

        cmds.text(label="Set all the desire configuration", parent=self.export_tab)

        cmds.separator(parent=self.export_tab, style='none', height=10)

        path_form_layout = cmds.formLayout(parent=self.export_tab)   

        folder_button = cmds.iconTextButton("folder_button", st="iconOnly", h=20, backgroundColor=(0.3, 0.3, 0.3), image=":/folder-open.png", ebg=True, parent = path_form_layout)
        self.text_field = cmds.textField("text_field",placeholderText="Set path of json file", h=20, w=500, bgc=(0.3, 0.3, 0.3), parent = path_form_layout, )
        load_button = cmds.button("load_button", label="Load Config", parent=path_form_layout, command=self.load_config)

        cmds.iconTextButton(folder_button, edit=True, command=self.file_dialog)

        cmds.formLayout(path_form_layout, edit=True, attachForm=[(folder_button, 'left', 5), (folder_button, 'top', 5),
                                                                (self.text_field, 'top', 5),
                                                                (load_button, 'right', 5), (load_button, 'top', 5)],
                        attachControl=[(self.text_field, 'left', 5, folder_button), (self.text_field, 'right', 5, load_button)])

        cmds.separator(parent=self.export_tab, style='none', height=10)

        cmds.text(label="NAMING CONVENTION CONFIG", parent=self.export_tab, font="boldLabelFont")

        cmds.separator(parent=self.export_tab, style='none', height=10)

        prefix_form_layout = cmds.formLayout(parent=self.export_tab)

       # Create the option menus for the naming convention

        # ------- LEFT ------- #

        self.transforms_option_menu = cmds.optionMenuGrp(parent=prefix_form_layout, label="Transforms", columnWidth2=[100, 100], columnAlign2=["left", "left"])
        cmds.menuItem(label="GRP")
        cmds.menuItem(label="grp")
        cmds.menuItem(label="TRN")
        cmds.menuItem(label="trn")

        self.meshes_option_menu = cmds.optionMenuGrp(parent=prefix_form_layout, label="Meshes", columnWidth2=[100, 100], columnAlign2=["left", "left"])
        cmds.menuItem(label="MSH")
        cmds.menuItem(label="mesh")
        cmds.menuItem(label="GEO")
        cmds.menuItem(label="geo")


        self.joints_option_menu = cmds.optionMenuGrp(parent=prefix_form_layout, label="Joints", columnWidth2=[100, 100], columnAlign2=["left", "left"])
        cmds.menuItem(label="JNT")
        cmds.menuItem(label="jnt")

        # ------- RIGHT ------- #

        self.locators_option_menu = cmds.optionMenuGrp(parent=prefix_form_layout, label="Locators", columnWidth2=[100, 100], columnAlign2=["left", "left"])
        cmds.menuItem(label="LOC")
        cmds.menuItem(label="loc")


        self.clusters_option_menu = cmds.optionMenuGrp(parent=prefix_form_layout, label="Clusters", columnWidth2=[100, 100], columnAlign2=["left", "left"])
        cmds.menuItem(label="CLS")
        cmds.menuItem(label="cls")
        cmds.menuItem(label="CLU")
        cmds.menuItem(label="clu")

        self.lights_option_menu = cmds.optionMenuGrp(parent=prefix_form_layout, label="Lights", columnWidth2=[100, 100], columnAlign2=["left", "left"])
        cmds.menuItem(label="LGT")
        cmds.menuItem(label="lgt")
        cmds.menuItem(label="LTI")
        cmds.menuItem(label="lti")

        # ------- CENTER ------- #

        self.left_option_menu = cmds.optionMenuGrp(parent=prefix_form_layout, label="Left", columnWidth2=[100, 100], columnAlign2=["left", "left"])
        cmds.menuItem(label="L")
        cmds.menuItem(label="l")
        cmds.menuItem(label="Left")
        cmds.menuItem(label="left")

        self.center_option_menu = cmds.optionMenuGrp(parent=prefix_form_layout, label="Center", columnWidth2=[100, 100], columnAlign2=["left", "left"])
        cmds.menuItem(label="C")
        cmds.menuItem(label="c")
        cmds.menuItem(label="Center")
        cmds.menuItem(label="center")

        self.right_option_menu = cmds.optionMenuGrp(parent=prefix_form_layout, label="Right", columnWidth2=[100, 100], columnAlign2=["left", "left"])
        cmds.menuItem(label="R")
        cmds.menuItem(label="r")
        cmds.menuItem(label="Right")
        cmds.menuItem(label="right")

        cmds.formLayout(prefix_form_layout, edit=True, attachForm=[
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
        self.naming_text_field = cmds.textField("textFieldWithPopup", placeholderText="Click here for keywords", parent=naming_form_layout, width=100)
        
        # Attach a popup menu to the text field
        cmds.popupMenu("popupMenu", parent=self.naming_text_field)
        
        # Add menu items to the popup menu
        keywords = ["<Side>", "<Name>", "<Tile>", "<Prefix>", "<CatClark>", "_"]
        for keyword in keywords:
            cmds.menuItem(label=keyword, command=partial(self.insert_keyword, keyword, self.naming_text_field))

        cmds.formLayout(naming_form_layout, edit=True, attachForm=[
            (naming_text, 'left', 50), (naming_text, 'top', 5),
            (self.naming_text_field, 'left', 175), (self.naming_text_field, 'top', 5),
            (self.naming_text_field, 'right', 50)
        ])     

        cmds.separator(parent=self.export_tab, style='none', height=10)

        export_form_layout = cmds.formLayout(parent=self.export_tab)
        self.export_checkBox = cmds.radioButtonGrp(numberOfRadioButtons=2, labelArray2=["Default Path", "Custom Path"], parent=export_form_layout, columnAlign=(1, 'left'), select=1, vertical=True)
        export_button = cmds.button(label="Export JSON", parent=export_form_layout, command=self.get_query_export_tab)

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

        # cmds.menu( label='File', tearOff=True, parent=window )
        # loadOption = cmds.menuItem(label="Load user preferences")
        # saveOption = cmds.menuItem(label="Save user preferences")
        # saveOption = cmds.menuItem(label="Export model check logs")


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

