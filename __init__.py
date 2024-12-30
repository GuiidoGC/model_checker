import os
import sys



main_path = os.path.abspath(__file__).replace('__init__.py', '')

json_data_path = os.path.join(main_path, 'json_data')
logs_path = os.path.join(main_path, 'logs')
main_script_path = os.path.join(main_path, 'main_script')
modules_path = os.path.join(main_path, 'modules')

sys.path.append(main_path)
sys.path.append(main_script_path)
sys.path.append(modules_path)
sys.path.append(json_data_path)
sys.path.append(logs_path)

import main_script.model_checker_ui as mcui
from importlib import reload
reload(mcui)

mcui.ModelCheckerUI().create_ui(main_path)
