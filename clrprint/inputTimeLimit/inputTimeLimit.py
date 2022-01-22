import sys
import time
from typing import Tuple, Union
if(sys.platform == "win32"):
    import msvcrt
    import ctypes
    from ctypes import wintypes
else:
    import select
    import tty
    import termios

def timedInput(timeout: int = 5, resetOnInput: bool = True, maxLength: int = 0, allowCharacters: str = "", endCharacters: str = "\x1b\n\r", inputType: str = "text"):
    if (maxLength < 0) or len(endCharacters) == 0:
        return "", False
    def checkStdin():
        if(sys.platform == "win32"):
            return msvcrt.kbhit()
        else:
            return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

    def readStdin():
        if(sys.platform == "win32"):
            return msvcrt.getwch()
        else:
            return sys.stdin.read(1)

    if(not sys.__stdin__.isatty()):
        raise RuntimeError(
            "inputTimeLimit() requires an interactive shell, cannot continue.")
    else:
        __savedConsoleSettings = __getStdoutSettings()
        __enableStdoutAnsiEscape()

        userInput = ""
        timeStart = time.time()
        timedOut = False

        while(True):
            if(timeout > -1 and (time.time() - timeStart) >= timeout):
                timedOut = True
                break
            if(checkStdin()):
                inputCharacter = readStdin() 
                if(inputCharacter in endCharacters):
                    break
                if(inputCharacter != '\b' and inputCharacter != '\x7f'):
                    if inputCharacter not in '\x00\xe0':
                        userInput += inputCharacter
                        print(inputCharacter, end='', flush=True)
                        if(maxLength == 1 and len(userInput) == 1 and inputType == "single"):
                            break
                else:
                    if(len(userInput)):
                        userInput = userInput[0:len(userInput) - 1]
                        print("\x1b[1D\x1b[0K", end='', flush=True)
                if(resetOnInput and timeout > -1):
                    timeStart = time.time()
        print("")
        __setStdoutSettings(__savedConsoleSettings)
        return userInput, timedOut

def __getStdoutSettings():
    if(sys.platform == "win32"):
        __savedConsoleSettings = wintypes.DWORD()
        kernel32 = ctypes.windll.kernel32
        # The Windows standard handle -11 is stdout
        kernel32.GetConsoleMode(
            kernel32.GetStdHandle(-11), ctypes.byref(__savedConsoleSettings))
    else:
        __savedConsoleSettings = termios.tcgetattr(sys.stdin)
    return __savedConsoleSettings


def __setStdoutSettings(__savedConsoleSettings):
    if(sys.platform == "win32"):
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(
            kernel32.GetStdHandle(-11), __savedConsoleSettings)
    else:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, __savedConsoleSettings)


def __enableStdoutAnsiEscape():
    if(sys.platform == "win32"):
        kernel32 = ctypes.windll.kernel32
        # Enable ANSI escape sequence parsing
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    else:
        # Should be enabled by default under Linux (and OSX?), just set cbreak-mode
        tty.setcbreak(sys.stdin.fileno(), termios.TCSADRAIN)