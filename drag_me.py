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


def add_script_to_shelf():
    """
    Adds a custom button on shelf for providing the UI
    """
    # Ensure the shelf exists
    script = '''import model_checker'''
    if not cmds.shelfLayout('Custom', exists=True):
        cmds.shelfLayout('Custom', parent="ShelfLayout")

    # Create the shelf button
    cmds.shelfButton(parent='Custom', annotation='Model Checker', label='Model Checker', image='modelToolkit.png', command=script, sourceType='python')