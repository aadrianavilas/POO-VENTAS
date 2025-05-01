from typing import List, Any, Dict
class Product:
    next = 0
    def __init__(self,id:int=0, descrip:str="Ninguno", preci:float=0, stock:int=0)->None:
        # Método constructor para inicializar los atributos de la clase Cliente
        Product.next += 1
        self.__id = id  # Asigna el ID único a la 
        self.descrip = descrip
        self.preci = preci
        self.__stock = stock  
                    
    @property
    def stock(self)->int:
        return self.__stock
    
    def __repr__(self)->str:
        # Método especial para representar la clase Cliente como una cadena
        return f'Producto:{self.__id} {self.descrip} {self.preci} {self.stock}'  
    
    def __str__(self)->str:
        # Método especial para representar la clase Cliente como una cadena
        return f'Producto:{self.__id} {self.descrip} {self.preci} {self.stock}'  
    
    def getJson(self)->Dict[str,Any]:
        # Método especial para representar la clase Cliente como una cadena
        return {"id":self.__id,"description":self.descrip,"price":self.preci,"stock": self.stock}
      
    def show(self)->None:
        # Método para imprimir los detalles del cliente en la consola
       
        print(f'{self.__id}  {self.descrip}           {self.preci}  {self.stock}')  
          
