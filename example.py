from clrprint import *
clrhelp()

clr = clrinput("Choose any color: ").strip()
clrprint("This is the color choosen by you",clr=clr)

clr = clrinput("Choose 3 colors separated with <space> :").strip().split(' ')
clrprint("color1","color2","color3",clr=clr)

