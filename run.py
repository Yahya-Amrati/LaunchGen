import sys
import os
import Utils_minecraft
import dependecies
import streamlit.web.cli as stcli

if __name__ == "__main__":
    dependecies.check()
    def resolve_path(path):
        return os.path.abspath(os.path.join(Utils_minecraft.local_path(), path))
    sys.argv = ["streamlit", "run", resolve_path("UI.py"), "--global.developmentMode=false"]
    sys.exit(stcli.main())
