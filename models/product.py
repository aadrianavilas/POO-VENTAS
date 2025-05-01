from typing import Any, Dict
class Product:
    next = 0
    def __init__(self,id:int=0, descrip:str="Ninguno", preci:float=0, stock:int=0)->None:
        Product.next += 1
        self.__id = id  
        self.descrip = descrip
        self.preci = preci
        self.__stock = stock  
                    
    @property
    def id(self)->int:
        return self.__id
    
    @property
    def stock(self)->int:
        return self.__stock
    
    def __repr__(self)->str:
        return f'Producto:{self.id} {self.descrip} {self.preci} {self.stock}'  
    
    def __str__(self)->str:
        return f'Producto:{self.id} {self.descrip} {self.preci} {self.stock}'  
    
    def getJson(self)->Dict[str,Any]:
        return {"id":self.id,"description":self.descrip,"price":self.preci,"stock": self.stock}
      
    def show(self)->None:       
        print(f'{self.id}  {self.descrip}           {self.preci}  {self.stock}')  
          
