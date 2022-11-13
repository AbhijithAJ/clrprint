'''
        __                _       __ 
  _____/ /________  _____(_)___  / /_
 / ___/ / ___/ __ \/ ___/ / __ \/ __/
/ /__/ / /  / /_/ / /  / / / / / /_  
\___/_/_/  / .___/_/  /_/_/ /_/\__/  
          /_/                        

- Colorful output
- Work's on IDLE, windows powerShell, Linux terminal
- Simply input() and print() with clrinput() and clrprint()
- Basic colors only. Red, green, yellow, blue, purple, and black/white (default)
- Flexible to print or take input only on demand (on DEBUG)
- User input timeout limit. (This is not supported on IDLE)

Colors available:
         red
         yellow
         green
         blue
         purple
         default
         magenta

How to use: 

    It is as simple as using ,'print' and 'input' functions with an
    additional parameter 'clr'. single letter is enough to represent
    color.

    Just replace 'print' with "clrprint",
    replace 'input' with "clrinput"
    and pass your texts and desired colors.

    Pass a DEBUG parameter to print only on DEBUG mode

    Pass timeout parameter to clrinput to take user input in desired time

    Note: input timeout feature is not supported on IDLE.

    Know more at https://github.com/AbhijithAJ/clrprint
        
DEVELOPED BY:
    Abhijith Boppe
    See more at https://bio.link/abhijithboppe
    Support me: https://www.buymeacoffee.com/abhijithboppe
    Thanks for using the module.

'''
import sys
from .inputTimeLimit import timedInput
if sys.platform == 'win32':
    from colorama import init  # for windows powershell and cmd.
    init()  
from termcolor import colored, cprint   # for terminal

IDLE = False
try:
    # This will only work in IDLE
    shell_connect = sys.stdout.shell    # check if idle 
    colormap = {
        "red": ("COMMENT", "Red"),
        "yellow": ("KEYWORD", "Light Red"),
        "green": ("STRING", "Green"),
        "blue": ("stdout", "Blue"),
        "purple": ("BUILTIN", "Purple"),  # color magenta
        "magenta": ("BUILTIN", "Purple"),
        "default": ("SYNC", "Black")
    }
    IDLE = True
    def _printColorText(text, clr):
        shell_connect.write(text, colormap[clr][0])

except AttributeError:
    # This will only work linux terminal,win powershell, cmd
    colormap = {
        "red": "red",
        "green": "green",
        "blue": "blue",
        "purple": "magenta",
        "default": "white",
        "magenta": "magenta",
        "yellow": "yellow"
    }
    def _printColorText(text, clr):
        cprint(text, colormap[clr], attrs=['bold'], file=sys.stderr, end='')        

except Exception as e:
    raise Exception('Unfortunate error: '+e)

def _chkDatatypes(clr, sep, end):
    if not isinstance(sep, str):
        raise Exception('"sep" must be string')
    if not isinstance(end, str):
        raise Exception('"end" must be a string')
    if not isinstance(clr, str) and not isinstance(clr, list):
        raise Exception('"clr" must be string with single color or multiple colors separeted by "," or a list of colors')

def _chk_clr(clr):
    '''
    check if given clr or 1st char is available 
    '''
    clr = clr.strip().lower()
    clr = clr if clr in colormap.keys() else clr[0] if clr != '' else 'default' # if not available/spelled wrong take 1st char of clr
    if len(clr) == 1:
        clrs = [clrs[0] for clrs in colormap.keys()]       # get 1st chars of colors available in colormap
        if clr in clrs:                                    # if given char is available, get the color via index
            return tuple(colormap.keys())[clrs.index(clr)]
        return "default"                                # else default color
    return clr

def _textColor(*text, clr, end, sep):
    '''
    takes a tuple/string and maps the color for each element.
    Return list with tuple elements Ex: [('word1','clr1'), ('word2','clr2')]
    '''
    _chkDatatypes(clr, end, sep)
    text = list(text)  # convert tuple to list to pop elements
    texts_clrs = []
    if isinstance(clr, list):
        clr = ','.join(clr)
    if ',' in clr:     # check for multi colors
        for clr in clr.strip().split(','):   # separeate colors
            try:
                clr = _chk_clr(clr)   # get the actual color
                txt = str(text.pop(0)) + sep     # pop each element for the color 
                txt = txt if text else txt.rstrip(sep) # strip the end if text list is empty
                texts_clrs.append((txt, clr))    
            except: break
    if text:
        clr = _chk_clr(clr)
        text = [str(elem)for elem in text]  # convert all elements in text(type-tuple) to string 
        text = sep.join(text)
        texts_clrs.append((text, clr))
    texts_clrs.append((end, clr))
    return texts_clrs

def clrhelp():
    '''
    print available colors and usage
    '''
    clrprint("Colors available:", clr='p')
    for clr in colormap:
        clrprint('\t', clr, clr=clr)
    DEBUG = True
    clrprint("How to use: ", clr='p')
    usage = '''
    It is as simple as using ,'print' and 'input' functions with an 
    additional parameter 'clr'. single letter is enough to represent 
    color.

    Just replace 'print' with "clrprint",
    replace 'input' with "clrinput"
    and pass your texts and desired colors as shown.
    '''
    clrprint(usage, clr='g')
    clrprint('Examples:', clr='p')
    clrprint("\tclrprint('your text', clr='green')")
    clrprint('\t\tyour text', clr='g')
    clrprint("\tclrinput('Enter input: ', clr='y')")
    clrprint('\t\tEnter input: |', clr='y')
    clrprint("\n\tclrprint('multi','colors','in a line', clr='r,g,b')")
    clrprint("\t\tmulti", "colors", "in a line", clr='r,g,b')
    clrprint("\n\tYou can input/output only on debug with a debug param as shown: ", clr='p')
    clrprint("\t\tclrprint('Error: Some Error Message', clr='y',debug=True)")
    clrprint("\t\tclrinput('Over write a file X? : ', clr='y', debug=True)")
    clrprint("\n\tNon Blocking input or input timeout with: ", clr='p')
    clrprint("\t\tclrinput(\"Over write a file X? (Choose in 10sec): \", clr='y', debug=True, timeout=10)")
    clrprint("\t\tNote:", " input timeout is not supported on IDLE", clr='r,y')

def clrprint(*text, clr="default", end: str = "\n", sep: str = ' ', debug=True):
    '''
    take *text and print with given color/s
    'clr' can be str or a list with str elements.
    Prints output only when debug is True
    '''
    if not debug:
        return
    if not IDLE: print(clrit(*text, clr=clr, end=end, sep=sep), end='') 
    else:
        texts_clrs = _textColor(*text, clr=clr, end=end, sep=sep)
        for text_clr in texts_clrs:
            _printColorText(text_clr[0], clr=text_clr[1])
    
def clrinput(*text, clr="default", debug=True, timeout=0):
    '''
    take text and print with given color
    and returns user input.
    Asks input only when debug is True
    else return. 
    if timeout > 0 program waits for 
    user input until timeout.
    ontimeout returns None
    '''
    if not debug: return
    if IDLE: 
        if timeout!=0: clrprint('-'*5,'timeout feature is not supported on IDLE. Please enter your input.','-'*5, clr='b,r,b')
        clrprint(*text, clr=clr, end='')
        return input()
    clrprint(*text, clr=clr, end='')
    if timeout: 
        userInput = _clrinputTimeout(timeout)
        return userInput if len(userInput)>0 else None
    return input()

#These only work for powershell, command prompt and Terminal but not for IDLE
def clrit(*text, clr='default', end:str = "", sep: str = ' '):
    '''This will return ASCII colord text.
    '''
    if IDLE: 
        raise Exception('-'*5,'clrit feature is not supported on IDLE','-'*5, clr='b,r,b')
    colored_string = ''
    texts_clrs = _textColor(*text, clr=clr, end=end, sep=sep)
    for text_clr in texts_clrs:
        colored_string += colored(text_clr[0], color=colormap[text_clr[1]] , attrs=['bold'])
    return colored_string

def _clrinputTimeout(timeout):
    '''Input timeout.
    '''
    return timedInput(timeout)[0]