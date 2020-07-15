import sys     
if sys.platform == 'win32':
    from colorama import init # for windows
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
            "default": ("SYNC", "Black")}
    
    def myclrtxt(text,clr,end='\n'):
        shell_connect.write(text+end, colormap[clr][0])

except AttributeError:
    # This will only work linux teminal,win powershell, cmd
    colormap = {"red":"red",
            "yellow": "yellow",
            "green": "green",
            "blue": "blue",
            "purple": "magenta",
            "default": "white"}

    def myclrtxt(text,clr,end='\n'):
        cprint(text, colormap[clr], attrs=['bold'], file=sys.stderr,end=end)
    
except Exception as a:
	clrprint(a,clr='r')

def chk_clr(clr):
    '''
    chek if given clr or 1st char is available 
    '''
    clr = clr if clr in colormap.keys() else clr[0]            # if not available/spelled wrong take 1st char of clr
    if len(clr) == 1:           
        clrs = [clrs[0] for clrs in colormap.keys()]           # get 1st chars of colors available in colormap
        if clr in clrs:                                        # if given char is available, get the color via index
            clr = tuple(colormap.keys())[clrs.index(clr)]
        else:
            clr ="default"                                     # else default color
    return clr

def clrhelp():
    '''
    print available colors
    '''
    for clr in colormap:
        clrprint(clr,clr=clr)
    clrprint("\nColors are available",clr='default')
    usage ='''
    It is as simple as using 'print' and 'input' functions with an 
    additional parameter 'clr'. single letter is enough to represent 
    color.

    Just replace 'print' with "clrprint",
    replace 'input' with "clrinput"
    and pass your color with text
    '''.format()
    clrprint(usage,clr='yellow')
    clrprint("Ex: clrprint('your text',clr='green')",clr='g')
    clrprint("Ex: clrinput('your text',clr='g')",clr='g')

    
def clrprint(*text, clr="default", end="\n",sep=' '):
    '''
    take text and print with given color
    '''
    text = tuple([str(elem)for elem in text]) # convert all elements in text(type-tuple) to string 
    text = sep.join(text)
    clr = chk_clr(clr.strip().lower())
    myclrtxt(text,clr,end)

def clrinput(text, clr="default"):
    '''
    take text and print with given color 
    and also take input
    '''
    clrprint(str(text), clr=clr, end='')
    return input()

