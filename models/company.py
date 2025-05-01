from typing import Dict,Any
class Company:
    next = 0  
    def __init__(self, name:str="SuperMaxi", ruc:str="0943213456001")->None:
        Company.next += 1
        self.__id = Company.next  
        self.business_name = name 
        self.ruc = ruc  
        
    @property
    def id(self)->int:
        return self.__id
    
    def show(self)->None:
        print(f"Id:{self.id} Empresa: {self.business_name} ruc:{self.ruc}")
        
    def getJson(self)->Dict[str,Any]:
        return {"id":self.id, "rasonsocial": self.business_name, "ruc":self.ruc}
    
    @staticmethod
    def get_business_name()->str:
        return f"Empresa:Corporacion el Rosado ruc:0876543294001"
        
    
