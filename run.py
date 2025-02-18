# cython: language_level=3
# sourcery skip: use-fstring-for-concatenation
import sys
import os
import streamlit.web.cli as stcli
import Utils_minecraft
import dependecies
import downloads

file_dependencies = ["UI.py", "downloads.py", "Utils_minecraft.py", "dependecies.py", "Gen.py", "Data_structure.py", "Utils_net.py"]

for i in file_dependencies:
    if not os.path.exists(downloads.path + i):
        downloads.main()
        break

dependecies.check()
def resolve_path(path):
    """this is a function for resolving the path"""
    return os.path.abspath(os.path.join(Utils_minecraft.local_path(), path))
sys.argv = ["streamlit", "run", resolve_path("UI.py"), "--global.developmentMode=false"]
sys.exit(stcli.main())
