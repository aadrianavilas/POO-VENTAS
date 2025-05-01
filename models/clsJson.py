from typing import List,Any,Dict
import json
from abc import ABC, abstractmethod


class IJsonFile(ABC):

    @abstractmethod
    def save(self, data:List[Dict[str,Any]])->None:
        pass

    @abstractmethod
    def read(self)->List[Any]:
        pass

    @abstractmethod
    def find(self,atributo:str,buscado:Any)->List[Any]:
        pass
    
    
class JsonFile(IJsonFile):
    def __init__(self, filename:str)->None:
        self.filename = filename

    def save(self, data:List[Dict[str,Any]])->None:
        with open(self.filename, 'w',encoding='utf-8') as file:
            json.dump(data, file,ensure_ascii=False,indent=4)# dump:graba datos a un archivo json
      
    def read(self)->List[Any]:
        try:
            with open(self.filename,'r',encoding="utf-8") as file:
                data = json.load(file)# load:carga datos desde un archivo json
        except FileNotFoundError:
            data = []
        return data
     
    def find(self,atributo:str,buscado:Any)->List[Any]:
        try:
            with open(self.filename,'r',encoding="utf-8") as file:
                datas = json.load(file)
                data = [item for item in datas if item[atributo] == buscado ]
        except FileNotFoundError:
            data = []
        return data
    