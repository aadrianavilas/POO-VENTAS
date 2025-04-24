import os
import datetime
import time
from tabulate import tabulate

# Variables globales: Colores en formato ANSI escape code
reset_color = "\033[0m"
red_color = "\033[91m"
green_color = "\033[92m"
yellow_color = "\033[93m"
blue_color = "\033[94m"
purple_color = "\033[95m"
cyan_color = "\033[96m"

# funciones de usuario

def gotoxy(x:int,y:int)->None:            
    print("%c[%d;%df"%(0x1B,y,x),end="")

def borrarPantalla()->None:
    os.system("cls") 

def mensaje(msg,f,c):
    pass

def show_error_and_clear(col:int,fil:int,message:str,color_text:str=red_color,color_reset:str=reset_color,cant:int=20)->None:
    gotoxy(col,fil);print(color_text+message+color_reset)
    time.sleep(1)
    gotoxy(col,fil);print(" "*cant)

def show_tabulate(data,headers):
    print(tabulate(data,headers=headers,tablefmt='pretty'))

path, _ = os.path.split(os.path.abspath(__file__))
print("ruta: ",path)