# -*- coding: utf-8 -*-
import subprocess, ctypes, locale


def get_cmd_encoding():
    return_string = ""
    test_string = r"‰ˆ¸ƒ÷‹ﬂ"
    arglist = ("echo "+test_string).split(" ")
    output = subprocess.Popen(arglist, shell=True, stdout=subprocess.PIPE,
                              stdin=subprocess.PIPE).communicate()[0]
    endocing_list = ["utf-8", "cp1252", "cp850"]
    for encoding in endocing_list:
        print(encoding)
        try:
            return_string = output.decode(encoding).strip()
            print(return_string)
        except:
            print("exception happened")
            return_string = ""

ctypes_cdll = ctypes.cdll.kernel32
ctypes_windll = ctypes.windll.kernel32

def fixCodePage():
    import sys
    import codecs
    import ctypes
    if sys.platform == 'win32':
        if sys.stdout.encoding != 'cp65001':
            os.system("echo off")
            os.system("chcp 65001") # Change active page code
            sys.stdout.write("\x1b[A") # Removes the output of chcp command
            sys.stdout.flush()
        LF_FACESIZE = 32
        STD_OUTPUT_HANDLE = -11
        class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

        class CONSOLE_FONT_INFOEX(ctypes.Structure):
            _fields_ = [("cbSize", ctypes.c_ulong),
            ("nFont", ctypes.c_ulong),
            ("dwFontSize", COORD),
            ("FontFamily", ctypes.c_uint),
            ("FontWeight", ctypes.c_uint),
            ("FaceName", ctypes.c_wchar * LF_FACESIZE)]

        font = CONSOLE_FONT_INFOEX()
        font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
        font.nFont = 12
        font.dwFontSize.X = 7
        font.dwFontSize.Y = 12
        font.FontFamily = 54
        font.FontWeight = 400
        font.FaceName = "Lucida Console"
        handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        ctypes.windll.kernel32.SetCurrentConsoleFontEx(handle, ctypes.c_long(False), ctypes.pointer(font))


get_cmd_encoding()
print("\nretrived ecodings:\n")
print("locale.getdefaultlocale() \t\t: ", locale.getdefaultlocale())
print("locale.getlocale() \t\t\t: ", locale.getlocale())
print("locale.getpreferredencoding() \t: ", locale.getpreferredencoding())
print("ctypes_cdll.GetConsoleCP() \t\t: ", ctypes_cdll.GetConsoleCP())
print("ctypes_cdll.GetConsoleOutputCP()\t: ", ctypes_cdll.GetConsoleOutputCP())
print("ctypes_windll.GetConsoleCP() \t\t: ", ctypes_windll.GetConsoleCP())
print("ctypes_windll.GetConsoleOutputCP()\t: ", ctypes_windll.GetConsoleOutputCP())
print("chcp command\t\t\t: ", subprocess.check_output("chcp", shell=True))
# just to keep the external System Terminal open
input()