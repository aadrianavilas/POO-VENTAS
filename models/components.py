from utilities import borrarPantalla, gotoxy
import time
from typing import List,Any,Dict
from datetime import datetime

class Menu:
    def __init__(self,titulo:str="",opciones:List[str]=[],col:int=6,fil:int=1)->None:
        self.titulo=titulo
        self.opciones=opciones
        self.col=col
        self.fil=fil
        
    def menu(self)->str:
        gotoxy(self.col,self.fil);print(self.titulo)
        self.col-=5
        for opcion in self.opciones:
            self.fil +=1
            gotoxy(self.col,self.fil);print(opcion)
        gotoxy(self.col+5,self.fil+2)
        opc = input(f"Elija opcion[1...{len(self.opciones)}]: ") 

        return opc   


class Valida:
    def solo_numeros(self,mensajeError:str,col:int,fil:int,cant:int=23)->str:
        while True: 
            gotoxy(col,fil)            
            valor = input()
            try:
                if int(valor) > 0:
                    break
            except:
                gotoxy(col,fil);print(mensajeError)
                time.sleep(1)
                gotoxy(col,fil);print(" "*cant)
        return valor

    def solo_letras(self,mensaje:str,mensajeError:str,col:int,fil:int)->str: 
        while True:
            gotoxy(col,fil) 
            valor = str(input("{}".format(mensaje)))
            if valor.isalpha():
                break
            else:
                gotoxy(col+len(mensaje),fil);print("{}".format(mensajeError))
                time.sleep(1)
                gotoxy(col+len(mensaje),fil);print(" "*20)
        return valor

    def solo_decimales(self,mensaje:str,mensajeError:str,col:int,fil:int)->float:
        while True:
            gotoxy(col,fil) 
            valor = str(input("{}".format(mensaje)))
            try:
                valor = float(valor)
                if valor > float(0):
                    break
            except:
                gotoxy(col,fil);print("{}".format(mensajeError))
                time.sleep(1)
                gotoxy(col,fil);print(" "*20)
        return valor
    
    def cedula(self,cedula:str)->bool:
        if len(cedula)!=10:
            return False
        
        if not "01"<=cedula[:2]<="24":
            return False

        digits:List[int]=[2,1,2,1,2,1,2,1,2]
        ced:List[int]=[int(d) for d in cedula[:10]]
        total:int=0
        for d in range(9):
            var=ced[d]*digits[d]
            if var>9:
                var-=9
            total+=var

        verificator= 0 if total % 10 == 0 else 10 - (total % 10)
        return verificator==int(cedula[9])

        
    def date(self,col:int,fil:int):
        while True:
            try:
                gotoxy(col,fil);date=input()
                datetime.strptime(date, "%d-%m-%Y")
                return date
            except:
                gotoxy(col,fil);print("Error: formato fecha inválido")
                time.sleep(1)
                gotoxy(col,fil);print(" "*30)
            



  

