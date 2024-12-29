import webbrowser

import maya.cmds as cmds
import maya.OpenMaya as om
from functools import partial

class ModelCheckerUI():
    """
    Class to create the UI for the model checker tool
    """

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
        general_frame = cmds.frameLayout(label="General", collapsable=True, parent=self.checker_tab)

        form_layout = cmds.formLayout(parent=general_frame)
        # Create the checkboxes for the general checks
        self.general_checks_checkbox = cmds.checkBoxGrp(numberOfCheckBoxes=4, 
                                                labelArray4=["Check empty group", "Check node history", "Check unused shader", "Check unused texture"], 
                                                parent=form_layout, 
                                                columnAlign=(1, 'left'), 
                                                vertical=True,
                                                columnWidth=[(1, 200)])
        
        cmds.formLayout(form_layout, edit=True, attachForm=[(self.general_checks_checkbox, 'left', 20), (self.general_checks_checkbox, 'top', 5)])

        cmds.separator(parent=self.checker_tab, style='none', height=10)          


        # Create the frame for naming checks
        naming_frame = cmds.frameLayout(label="Naming", collapsable=True, parent=self.checker_tab)

        form_layout = cmds.formLayout(parent=naming_frame)
        # Create the checkboxes for the naming checks
        self.naming_checks_checkbox = cmds.checkBoxGrp(numberOfCheckBoxes=4, 
                                                labelArray4=["Check namings", "Check duplicated names", "Check pasted nodes", "Check Namespace"], 
                                                parent=form_layout, 
                                                columnAlign=(1, 'left'), 
                                                vertical=True,
                                                columnWidth=[(1, 200)])
        
        cmds.formLayout(form_layout, edit=True, attachForm=[(self.naming_checks_checkbox, 'left', 20), (self.naming_checks_checkbox, 'top', 5)])

        cmds.separator(parent=self.checker_tab, style='none', height=10)        

        # Create the frame for model checks
        model_frame = cmds.frameLayout(label="Model", collapsable=True, parent=self.checker_tab)

        form_layout = cmds.formLayout(parent=model_frame)
        # Create the checkboxes for the model checks
        self.model_checks_checkbox = cmds.checkBoxGrp(numberOfCheckBoxes=4, 
                                                labelArray4=["Check items freezed", "Check pivots", "Check cv's position", "Check Namespace"], 
                                                parent=form_layout, 
                                                columnAlign=(1, 'left'), 
                                                vertical=True,
                                                columnWidth=[(1, 200)])
        
        cmds.formLayout(form_layout, edit=True, attachForm=[(self.model_checks_checkbox, 'left', 20), (self.model_checks_checkbox, 'top', 5)])

        cmds.separator(parent=self.checker_tab, style='none', height=10)        


        output_console_label = cmds.text(label="OUTPUT CONSOLE", parent=self.checker_tab, font="boldLabelFont", height=30)

        # Create console output
        text_scroll_list = cmds.textScrollList(parent=self.checker_tab, allowMultiSelection=True)

        cmds.separator(parent=self.checker_tab, style='none', height=10)

        final_buttons_form = cmds.formLayout(parent=self.checker_tab)

        # Create the buttons for the model checker tab
        check_all_button = cmds.button(label="Check All", parent=final_buttons_form)
        unchecked_all_button = cmds.button(label="Uncheck All", parent=final_buttons_form)
        export_log_button = cmds.button(label="Export Log", parent=final_buttons_form)
        run_checker_button = cmds.button(label="Run Checkers", parent=final_buttons_form)
        select_errors_button = cmds.button(label="Select Errors", parent=final_buttons_form)
        

        cmds.formLayout(final_buttons_form, edit=True, attachForm=[(check_all_button, 'left', 5), (check_all_button, 'bottom', 5),
                                                                (export_log_button, 'right', 5), (export_log_button, 'bottom', 5),
                                                                (unchecked_all_button, 'left', 70), (unchecked_all_button, 'bottom', 5),
                                                                (select_errors_button, 'left', 150), (select_errors_button, 'bottom', 5),
                                                                (run_checker_button, 'right', 80), (run_checker_button, 'bottom', 5)])



    def export_tab_ui(self):
        """
        Create the UI for the export tab

        Args:
            self: The class instance
        """

        self.export_tab = cmds.columnLayout(adjustableColumn=True, parent=self.tabs)
        path_form_layout = cmds.formLayout(parent=self.export_tab)   

        folder_button = cmds.iconTextButton("folder_button", st="iconOnly", h=20, backgroundColor=(0.3, 0.3, 0.3), image=":/folder-open.png", ebg=True, parent = path_form_layout)
        text_field = cmds.textField("text_field", font="obliqueLabelFont", h=20, w=500, bgc=(0.3, 0.3, 0.3), parent = path_form_layout)
        export_button = cmds.button("export_button", label="Export Curve", parent=path_form_layout)

        cmds.formLayout(path_form_layout, edit=True, attachForm=[(folder_button, 'left', 5), (folder_button, 'top', 5),
                                                                (text_field, 'top', 5),
                                                                (export_button, 'right', 5), (export_button, 'top', 5)],
                        attachControl=[(text_field, 'left', 5, folder_button), (text_field, 'right', 5, export_button)])


    def create_ui(self):
        """
        Create the main UI for the model checker tool

        Args:
            self: The class instance
        """

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


        cmds.showWindow(window)


ModelCheckerUI().create_ui()

