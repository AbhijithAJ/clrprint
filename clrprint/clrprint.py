import sys     
if sys.platform == 'win32':
    from colorama import init # for windows powershell and cmd
    init()
from termcolor import cprint  # for terminal

try:
    # This will only work in IDLE, it won't work from a command prompt
    shell_connect = sys.stdout.shell    # check if idle or terminal

    colormap = {"red": ("COMMENT", "Red"),
            "yellow": ("KEYWORD", "Light Red"),
            "green": ("STRING", "Green"),
            "blue": ("stdout", "Blue"),
            "purple": ("BUILTIN", "Purple"),   #magenta
            "magenta":("BUILTIN", "Purple"),
            "default": ("SYNC", "Black")}
    
    def myclrtxt(text,clr,end='\n'):
        shell_connect.write(text+end, colormap[clr][0])

except AttributeError:
    # This will only work linux terminal,win powershell, cmd
    colormap = {"red":"red",
            "yellow": "yellow",
            "green": "green",
            "blue": "blue",
            "purple": "magenta",
            "default": "white",
            "magenta":"magenta"}

    def myclrtxt(text,clr,end='\n'):
        cprint(text, colormap[clr], attrs=['bold'], file=sys.stderr,end=end)
    
except Exception as a:
	clrprint(a,clr='r')

def chkDatatypes(clr,sep,end):
    if not isinstance(sep,str):
        raise Exception('sep must be string')
    if not isinstance(end,str):
        raise Exception('end must be a string')
    def chkDatatypeOfClr(clr):
        for el in clr:
            if not isinstance(el,str):
                raise Exception('list must be contain only string type elements')
    if isinstance(clr,list):
        chkDatatypeOfClr(clr)
    elif not isinstance(clr,str):
        raise Exception("clr must be string or list with string elements")

def chk_clr(clr):
    '''
    check if given clr or 1st char is available 
    '''
    clr = clr.strip().lower()
    clr = clr if clr in colormap.keys() else clr[0]            # if not available/spelled wrong take 1st char of clr
    if len(clr) == 1:           
        clrs = [clrs[0] for clrs in colormap.keys()]           # get 1st chars of colors available in colormap
        if clr in clrs:                                        # if given char is available, get the color via index
            clr = tuple(colormap.keys())[clrs.index(clr)]
        else:
            clr ="default"                                     # else default color
    return clr

def clrhelp() -> None:
    '''
    print available colors
    '''
    clrprint("Colors available:",clr='default')
    for clr in colormap:
        clrprint('\t',clr,clr=clr)

    clrprint("How to use: ",clr='g')
    usage ='''
    It is as simple as using 'print' and 'input' functions with an 
    additional parameter 'clr'. single letter is enough to represent 
    color.

    Just replace 'print' with "clrprint",
    replace 'input' with "clrinput"
    and pass your color with text
    '''.format()
    clrprint(usage,clr='yellow')
    clrprint('Examples:')
    clrprint("\tclrprint('your text',clr='green')",clr='g')
    clrprint("\tclrinput('your text',clr='g')",clr='g')
    clrprint("\n\tPrint","Multi","colors","in","single","line with:",clr=['r','y','g','b'])
    clrprint("\t\tEx: clrprint('tex_clr1','tex_clr2',clr=['r','g'])",clr='g')

    
def clrprint(*text, clr="default", end:str="\n",sep:str=' ') -> None:
    '''
    take *text and print with given color/s
    'clr' can be str or a list with str elements.
    '''
    chkDatatypes(clr,end,sep)
    text = list(text)  # convert tuple to list to pop(0)
    if isinstance(clr,list):
        for clr in (clr):
            try:
                clr = chk_clr(clr)
                txt = str(text.pop(0))+sep 
                txt = txt if text else txt.rstrip(sep)
                myclrtxt(txt, clr, end='')
            except Exception as n:
                break
    if text:
        clr = chk_clr(clr)
        text = [str(elem)for elem in text] # convert all elements in text(type-tuple) to string 
        text = sep.join(text)          
        myclrtxt(text, clr, end)
    else:
        myclrtxt('',clr=clr,end=end)

def clrinput(text, clr="default") -> None:
    '''
    take text and print with given color 
    and also take input
    '''
    clrprint(str(text), clr=clr, end='')
    return input()

