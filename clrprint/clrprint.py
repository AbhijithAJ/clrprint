import sys
if sys.platform == 'win32':
    from colorama import init  # for windows powershell and cmd this should be initialized
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
        "yellow": "yellow",
        "green": "green",
        "blue": "blue",
        "purple": "magenta",
        "default": "white",
        "magenta": "magenta"
    }
    def _printColorText(text, clr):
        cprint(text, colormap[clr], attrs=['bold'], file=sys.stderr, end='')        

except Exception as e:
    clrprint('Unfortunate error: ' ,e, clr='r')

def _chkDatatypes(clr, sep, end):
    if not isinstance(sep, str):
        raise Exception('sep must be string')
    if not isinstance(end, str):
        raise Exception('end must be a string')
    if not isinstance(clr, str):
        raise Exception('clr must be string with single color or multiple colors separeted by ","')
    elif not isinstance(clr, str):
        raise Exception("clr must be string or list with string elements")

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
    if ',' in clr:     # check for multi colors
        for clr in clr.split(','):   # separeate colors
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
    and pass your texts and desired colors as shown .
    '''
    clrprint(usage, clr='yellow')
    clrprint('Examples:', clr='p')
    clrprint("\tclrprint('your text', clr='green')")
    clrprint('\t\tyour text', clr='g')
    clrprint("\tclrinput('Enter input: ', clr='y')")
    clrprint('\t\tEnter input: |', clr='y')
    clrprint("\n\tclrprint('multi','colors','in a line', clr='r,g,b')")
    clrprint("\t\tmulti", "colors", "in a line", clr='r,g,b')
    clrprint("\n\tYou can user input/output only on debug with a debug param as shown: ", clr='p')
    clrprint("\t\tclrprint('Error: Some Error Message', clr='y',debug=True)")
    clrprint("\t\tclrinput('Can I over write a file X? : ', clr='y', debug=True)")


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
    
def clrinput(*text, clr="default", debug=True):
    '''
    take text and print with given color
    and also take input.
    Asks input only when debug is True
    else returns None
    '''
    if not debug:
        return
    clrprint(*text, clr=clr)
    return input()

#These only work for powershell, command prompt and Terminal but not for IDLE
def clrit(*text, clr='default', end:str = "", sep: str = ' '):
    if IDLE: raise Exception("clrit is not supported on IDLE")
    colored_string = ''
    texts_clrs = _textColor(*text, clr=clr, end=end, sep=sep)
    for text_clr in texts_clrs:
        colored_string += colored(text_clr[0], color=colormap[text_clr[1]] , attrs=['bold'])
    return colored_string