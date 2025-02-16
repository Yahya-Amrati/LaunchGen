import streamlit.web.cli as stcli
import sys, os

def resolve_path(path):
    return os.path.abspath(os.path.join(os.getcwd(), path))

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", resolve_path("UI.py"), "--global.developmentMode=false"]
    sys.exit(stcli.main())
