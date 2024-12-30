"""
Drag and drop this file into the viewport to run the package installer
"""
import sys
import os
import shutil
import maya.cmds as cmds



def onMayaDroppedPythonFile(*args):
    """
    Runs when file is dropped into the Maya's viewport
    The name of this function is what Maya expects/uses as entry point, so it cannot be changed
    """
    path = findScriptPath()
    scripts_path = findMayaScriptPath()
    result = moveScriptToPath(path, scripts_path)
    add_script_to_shelf()
    # print(result)

    # Initial Feedback
    print("_"*40)
    print("Initializing Drag-and-Drop Setup...")
    # print(result)

    print(path)
    print(scripts_path)

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

    final_path = os.path.join(final_path, 'model_checker')

    return final_path


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
        parent_dir = os.path.abspath(__file__).replace('\drag_me.py', '')
        sys.path.append(parent_dir)
        import model_checker
        from importlib import reload
        reload(model_checker)

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
