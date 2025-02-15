import dependecies ; dependecies.check()  # noqa: E702
import json
import Gen
import streamlit as st
from Data_structure import MinecraftLauncher
import Utils_minecraft

# Hide Streamlit default UI elements
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stToolbar"] {display: none !important;}
    </style>
"""
st.set_page_config(layout="wide", page_title="LaunchGen", page_icon="😁")
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Session state initialization
if "page" not in st.session_state:
    st.session_state.page = 1
if "Launcher_Name" not in st.session_state:
    st.session_state.Launcher_Name = ""
if "Launcher_base" not in st.session_state:
    st.session_state.Launcher_base = ""
if "Launcher_Version" not in st.session_state:
    st.session_state.Launcher_Version = ""
if "is_vanilla" not in st.session_state:
    st.session_state.is_vanilla = False
if "is_forge" not in st.session_state:
    st.session_state.is_forge = False
if "is_fabric" not in st.session_state:
    st.session_state.is_fabric = False


# Central container
def C():
    a, b, c = st.columns([1, 3, 1])
    return b


# Page 1: Launcher Name Input
def P1():
    d = C()
    with d:
        st.markdown(
            "<h1 style='text-align:center;color:#333;'>LaunchGen</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h3 style='text-align:center;color:#555;'>Input your launcher name</h3>",
            unsafe_allow_html=True,
        )
        with st.form("f1"):
            n = st.text_input(
                "Launcher Name", value=st.session_state.Launcher_Name, key="name_input"
            )
            s = st.form_submit_button("Next", use_container_width=True)
            if s:
                if n.strip():
                    st.session_state.Launcher_Name = n.strip().title()
                    st.session_state.page = 2
                    st.rerun()
                else:
                    st.error("Please enter a launcher name.")


# Page 2: Launcher Base Selection
def P2():
    d = C()
    with d:
        st.markdown(
            "<h1 style='text-align:center;color:#333;'>LaunchGen</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h3 style='text-align:center;color:#555;'>Choose your launcher base</h3>",
            unsafe_allow_html=True,
        )
        with st.form("f2"):
            b = st.selectbox(
                "Launcher Base",
                options=["Vanilla", "Forge"],
                index=0
                if st.session_state.Launcher_base == ""
                else ["Vanilla", "Forge"].index(st.session_state.Launcher_base),
            )
            a1, a2 = st.columns(2)
            with a1:
                bs = st.form_submit_button("Back", use_container_width=True)
            with a2:
                ns = st.form_submit_button("Next", use_container_width=True)
            if bs:
                st.session_state.page = 1
                st.rerun()
            elif ns:
                st.session_state.Launcher_base = b
                st.session_state.is_vanilla = b == "Vanilla"
                st.session_state.is_forge = b == "Forge"
                st.session_state.is_fabric = False
                st.session_state.page = 3
                st.rerun()


# Page 3: Launcher Version Input
def P3():
    d = C()
    with d:
        st.markdown(
            "<h1 style='text-align:center;color:#333;'>LaunchGen</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h3 style='text-align:center;color:#555;'>Enter your launcher MC version</h3>",
            unsafe_allow_html=True,
        )
        with st.form("f3"):
            v = st.text_input(
                "MC Version",
                value=st.session_state.Launcher_Version,
                key="version_input"
            )
            a1, a2 = st.columns(2)
            with a1:
                bs = st.form_submit_button("Back", use_container_width=True)
            with a2:
                ns = st.form_submit_button("Next", use_container_width=True)
            if bs:
                st.session_state.page = 2
                st.rerun()
            elif ns:
                if not v.strip():
                    st.warning("Please enter a valid version.")
                elif not Utils_minecraft.check_is_version_valid(v):
                    st.error("The version you entered is not valid.")
                else:
                    st.session_state.Launcher_Version = v.strip()
                    st.session_state.page = 4
                    st.rerun()


# Page 4: Final Launcher Information
def PF():
    d = C()
    with d:
        try:
            L = MinecraftLauncher(
                name=f"_{st.session_state.Launcher_Name}",
                is_forge=st.session_state.is_forge,
                is_fabric=st.session_state.is_fabric,
                is_vanilla=st.session_state.is_vanilla,
                version_Launcher=st.session_state.Launcher_Version,
            )
        except TypeError as e:
            st.error(f"Error creating launcher data: {e}")
            return

        with st.form("f4"):
            st.markdown(
                "<h1 style='text-align:center;color:#333;'>LaunchGen</h1>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<h3 style='text-align:center;color:#555;'>Your Launcher Information</h3>",
                unsafe_allow_html=True,
            )
            dta = L.__dict__
            st.json(dta)
            ex = st.form_submit_button("Exit", use_container_width=True)
            if ex:
                try:
                    with open("launcher.json", "w") as jf:
                        json.dump(dta, jf, indent=4)
                    st.warning("Wait compiling launcher")
                    Gen.generate_final_product(dta)
                except Exception as e:
                    st.error(f"An error occurred while saving data: {e}")
                st.session_state.page = 1
                st.rerun()


# Page Navigation
if st.session_state.page == 1:
    P1()
elif st.session_state.page == 2:
    P2()
elif st.session_state.page == 3:
    P3()
elif st.session_state.page == 4:
    PF()
