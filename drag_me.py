"""
Drag and drop this file into the viewport to run the package installer
"""
import sys
import os
import shutil
import maya.cmds as cmds
import maya.OpenMaya as om
from functools import partial
from random import uniform
from importlib import reload

def onMayaDroppedPythonFile(*args):
    """
    Runs when file is dropped into the Maya's viewport
    The name of this function is what Maya expects/uses as entry point, so it cannot be changed
    """
    error_find, path = findScriptPath()
    if error_find == "Error":
        print("Error Find Script Path")
        progress_bar("Error")
        return
    error_maya, scripts_path, scripts_folder = findMayaScriptPath()
    if error_maya == "Error":
        print("Error Find Maya Script Path")
        progress_bar("Error")
        return
    error_move, result = moveScriptToPath(path, scripts_path)
    if error_move == "Error":
        print("Error Move Script To Path")
        progress_bar("Error")
        return
    error_user = update_user_setup(scripts_folder)
    if error_user == "Error":
        print("Error User Setup")
        progress_bar("Error")
        return
    add_script_to_shelf()
    print(error_find, error_maya, error_move, error_user)
    if error_find == "Error" or error_maya == "Error" or error_move == "Error" or error_user == "Error":
        progress_bar("Error")
    else:
        progress_bar(None)

def update_user_setup(scripts_path):
    user_setup_name = "userSetup.py"
    
    code_to_add = """
import maya.cmds as cmds
print("Dentro")
if cmds.menu("ModelChecker", exists=True):
    cmds.deleteUI("ModelChecker")

cmds.menu("ModelChecker", label="Model Checker", parent="MayaWindow")
cmds.menuItem(label="Model Checker", command=partial(import model_checker))

"""

    files = os.listdir(scripts_path)
    setup = []
    for file in files:
        if file == user_setup_name:
            setup.append(file)
    
    if setup:
        if len(setup) == 1:
            user_setup_path = os.path.join(scripts_path,user_setup_name)
            with open(user_setup_path, 'a') as file:
                file.write(code_to_add)
            om.MGlobal.displayInfo("Code added to userSetup.py")
        else:
            om.MGlobal.displayError("More than one userSetup.py, skipping!")
            return
    else:
        user_setup_path = os.path.join(scripts_path,user_setup_name)
        with open(user_setup_path, 'w') as file:
            file.write(code_to_add)
        om.MGlobal.displayInfo("userSetup.py created and code added")      




def findScriptPath(*args):
    """
    Finds the path of the executed script.
    """

    parent_dir = os.path.abspath(__file__).replace('\drag_me.py', '')
    if parent_dir:
        return None, parent_dir
    else:
        return "Error Find Script Path", parent_dir
    

def findMayaScriptPath(*args):
    """
    Finds the path of maya script path.
    """
    version = cmds.about(v=True)

    enviroment = os.environ["MAYA_SCRIPT_PATH"]
    enviroment = enviroment.split(";")
    for enviroments in enviroment:
        if f"Documents/maya/{version}/scripts" in enviroments:
            final_path = enviroments

    scripts_path = final_path
    final_path = os.path.join(final_path, 'model_checker')
    if os.path.exists(final_path):
        return "Error Find Maya Script Path", final_path, scripts_path


    if scripts_path and final_path:
        return None, final_path, scripts_path
    else:
        return "Error Find Maya Script Path", final_path, scripts_path


def moveScriptToPath(source_path, target_path, *args):
    """
    Moves the script to the target path.
    """
    try:
        # Copy the entire directory tree
        shutil.copytree(source_path, target_path)
        return None, "Success"
    except Exception as e:
        return "Error move Script To Path", "Error"

def call_window(*args):
    try:
        import model_checker
        reload(model_checker)
    except ImportError as e:
        om.MGlobal.displayError("Module not found")
        return


def add_script_to_shelf():
    """
    Adds a custom button on shelf for providing the UI
    """
    # Check if the menu already exists and delete it
    if cmds.menu("ModelChecker", exists=True):
        cmds.deleteUI("ModelChecker")

    # Add a new menu next to the "Help" menu
    cmds.menu("ModelChecker", label="Model Checker", parent="MayaWindow")

    # Add menu items
    cmds.menuItem(label="Model Checker",command=call_window)

def progress_bar(error_type):
    amount = 0

    cmds.progressWindow(    title='Model Checker installer',
                                            progress=amount,
                                            status='Installing!',
                                            isInterruptable=True )

    if error_type == "Error":
        max_number = 60
    else:
        max_number = 100

    while amount < max_number :
            # Check if the dialog has been cancelled
            if cmds.progressWindow( query=True, isCancelled=True ) :
                    break

            # Check if end condition has been reached
            if cmds.progressWindow( query=True, progress=True ) >= 100 :
                    break

            amount += uniform(0.1, 5)


            cmds.progressWindow( edit=True, progress=round(amount, 2), status=(f"Installing ") )

            cmds.pause( seconds=uniform(0.5, 1.5) )

    cmds.progressWindow(endProgress=1)
    if error_type == "Error":
        cmds.confirmDialog(title='Installation Failed', message='Installation failed!', button=['OK'])
    else:
        cmds.confirmDialog(title='Installation Complete', message='Installation complete!', button=['OK'])