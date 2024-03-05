# File to test any function calls
# Encode file path so as to not encounter any unicode issues | May or may not be needed

import ai
import vision
import os
from pathlib import Path

dirs = r'C:\Users\logan\codeProjects\Python\MADCOM\Images\WIN_20240227_09_26_44_Pro.jpg'.encode()
print(dirs.decode())