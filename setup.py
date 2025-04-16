from cx_Freeze import setup, Executable
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Include the images and other required files
build_exe_options = {
    "include_files": ["complete1.png","trash1.png"]
}

setup(
    name="To-Do_List",
    version="1.0",
    description="It Is A Simple To-Do-List To Write A Task And Manage Them",
    options={"build_exe": build_exe_options},
    executables=[Executable("to-do.py", icon="to-do.ico", base=base)]
)
