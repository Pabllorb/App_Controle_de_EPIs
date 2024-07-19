from cx_Freeze import setup, Executable
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"
elif sys.platform == "win64":
    base = "Win64GUI"

executables = [Executable("main.py", base=base)]

setup(
    name="CadastroDeEpi",
    version="0.1",
    description="Controle de entrada e saida de equipamentos de proteção individual",
    executables=executables
)
