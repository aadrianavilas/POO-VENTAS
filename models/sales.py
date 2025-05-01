from models.calculos import Icalculo
from datetime import date
import os
from typing import Dict,Any
# Colores en formato ANSI escape code
reset_color = "\033[0m"
red_color = "\033[91m"
green_color = "\033[92m"
yellow_color = "\033[93m"
blue_color = "\033[94m"
purple_color = "\033[95m"
cyan_color = "\033[96m"

class SaleDetail:
    _line=0
    def __init__(self,product:object,quantity:int)->None:
        SaleDetail._line += 1
        self.__id = SaleDetail._line
        self.product = product
        self.preci = product.preci
        self.quantity = quantity
    
    @property
    def id(self)->int:
        return self.__id
    
    def __repr__(self)->str:
        return f'{self.id} {self.product.descrip} {self.preci} {self.quantity}'  
        
class Sale(Icalculo):
    next=0
    FACTOR_IVA=0.12
    def __init__(self,id,client:object)->None:
        Sale.next += 1
        self.__invoice = id
        self.date = date.today()
        self.client = client
        self.subtotal = 0
        self.percentage_discount = client.discount 
        self.discount = 0
        self.iva = 0 
        self.total = 0
        self.sale_detail = []
    
    @property
    def invoice(self)->int:
        return self.__invoice
    
    @property
    def dni(self)->int:
        return self.client.dni
    
    @property
    def payment_method(self)->int:
        return self.client.payment_method
    
    def __repr__(self)->str:
        return f'Factura# {self.invoice} {self.date} {self.client.fullName()} {self.total}'  
    
    def cal_iva(self,iva:float=0.12,valor:float=0)->float:
        return round(valor*iva,2)
    
    def cal_discount(self,valor:float=0,discount:float=0)->int:
        return valor*discount
    
    def add_detail(self,prod:object,qty:int)->None:
        detail = SaleDetail(prod,qty)
        self.subtotal += round(detail.preci*detail.quantity,2)
        self.discount = self.cal_discount(self.subtotal,self.percentage_discount)     
        self.iva = self.cal_iva(Sale.FACTOR_IVA,self.subtotal-self.discount)
        self.total = round(self.subtotal+self.iva-self.discount,2)
        self.sale_detail.append(detail)  
    
    def print_invoice(self,company:object)->None:    
        os.system('cls')
        print('\033c', end='')
        print(green_color+"*"*70+reset_color)   
        print(blue_color+f"Empresa: {company.business_name} Ruc: {company.ruc}",end='')    
        print(" Factura#:{:7}Fecha:{}".format(self.invoice,self.date))
        self.client.show()
        print(green_color+"*"*70+reset_color)  
        print(purple_color+"Linea Articulo Precio Cantidad Subtotal")
        for det in self.sale_detail:
            print(blue_color+f"{det.id:5} {det.product.descrip:6} {det.preci:7} {det.quantity:2} {det.preci*det.quantity:14}")  
        print(green_color+"*"*70+reset_color)    
        print(purple_color+" "*23,"Subtotal:  ",str(self.subtotal))
        print(" "*23,"Descuento: ",str(self.discount))
        print(" "*23,"Iva:       ",str(self.iva))
        print(" "*23,"Total:     ",str(self.total)+reset_color)  

        

    def getJson(self)->Dict[str,Any]:
        invoice= {"invoice":self.invoice,"date":self.date.strftime("%Y-%m-%d"),"dni":self.client.dni
        ,"client":self.client.fullName(),"payment_method":self.client.payment_method,"subtotal":self.subtotal,"discount": self.discount,"iva": self.iva,"total": self.total,"details":[]}
        for det in self.sale_detail:
            invoice["details"].append(
                {"product":det.product.descrip,
                "price": det.preci,
                "quantity": det.quantity}
            )  
        return invoice

