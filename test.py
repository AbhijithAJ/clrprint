from socket import timeout
from clrprint import *

a = clrinput('Enter : ', clr='g', timeout=3) or 1

print(a)