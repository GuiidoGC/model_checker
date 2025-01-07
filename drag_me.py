"""
Drag and drop this file into the viewport to run the package installer
"""
import sys
import os
import shutil
import maya.cmds as cmds
import maya.OpenMaya as om
from functools import partial

print("hola")

def onMayaDroppedPythonFile(*args):
    """
    Runs when file is dropped into the Maya's viewport
    The name of this function is what Maya expects/uses as entry point, so it cannot be changed
    """
    path = findScriptPath()
    scripts_path, scripts_folder = findMayaScriptPath()
    result = moveScriptToPath(path, scripts_path)
    update_user_setup(scripts_folder)
    add_script_to_shelf()


    # Initial Feedback
    print("_"*40)
    print("Initializing Drag-and-Drop Setup...")


def update_user_setup(scripts_path):
    user_setup_name = "userSetup.py"
    
    code_to_add = """
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
        print(len(setup))
        if len(setup) == 1:
            user_setup_path = os.path.join(scripts_path,user_setup_name)
            print(user_setup_path)
            with open(user_setup_path, 'a') as file:
                file.write(code_to_add)
            om.MGlobal.displayInfo("Code added to userSetup.py")
        else:
            print(setup)
            om.MGlobal.displayError("More than one userSetup.py, skipping!")
            return
            




def findScriptPath(*args):
    """
    Finds the path of the executed script.
    """

    parent_dir = os.path.abspath(__file__).replace('\drag_me.py', '')
    
    return parent_dir

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

    return final_path, scripts_path


def moveScriptToPath(source_path, target_path, *args):
    """
    Moves the script to the target path.
    """
    try:
        # Copy the entire directory tree
        shutil.copytree(source_path, target_path)
        return "Successfully installed"
    except Exception as e:
        return f"Failed to move: {e}"

def call_window(*args):
        import model_checker


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
onMayaDroppedPythonFile()
