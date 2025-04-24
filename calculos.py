# class Icalculo:
#   def cal_iva(self,iva=0.12,valor=0):
#     pass
    
#   def cal_discount(self,valor=0,discount=0):
#     pass

from abc import ABC, abstractmethod

class Icalculo(ABC):
    @abstractmethod
    def cal_iva(self,iva:float=0.12,valor:float=0)->float:
      pass
    @abstractmethod
    def cal_discount(self,valor:float=0,discount:float=0)->float:
      pass
# ical = Icalculo()