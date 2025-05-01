
from models.components import Menu,Valida
from utilities import borrarPantalla,gotoxy,show_error_and_clear,show_tabulate
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from models.clsJson import JsonFile
from models.company  import Company
from models.customer import RegularClient,VipClient
from models.sales import Sale
from models.product  import Product
from models.iCrud import ICrud
import datetime
import time
from functools import reduce
from typing import List,Dict, Any,Tuple
from utilities import path


class CrudSales(ICrud):
    def create(self)->None:
        # cabecera de la venta

        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        json_file_invoices:JsonFile = JsonFile(path+'/archivos/invoices.json')
        invoices:List[Any] = json_file_invoices.read()
        if not invoices:
            ult_invoices:int=1
        else:
            ult_invoices:int = invoices[-1]["invoice"]+1
            
        gotoxy(2,1);print(green_color+"*"*98+reset_color)
        gotoxy(33,2);print(blue_color+"Registro de Venta")
        gotoxy(15,3);print(blue_color+Company.get_business_name())
        gotoxy(8,4);print(f"Factura#:{ult_invoices:04d} {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(70,4);print("Subtotal:")
        gotoxy(70,5);print("Decuento:")
        gotoxy(70,6);print("Iva     :")
        gotoxy(70,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        while True:
            dni:str=validar.solo_numeros("Error: Dni invalido",23,6)
            json_file_client:JsonFile = JsonFile(path+'/archivos/clients.json')
            client:List[Any] = json_file_client.find("dni",dni)
            if not client:
                show_error_and_clear(23,6,'Cliente no existe',red_color,blue_color)
                continue
            break
        card:bool
        client:Dict[str,Any] = client[0]
        if client['type']=='regular':
            card=True if client['payment_method']=='tarjeta' else False
            cli = RegularClient(client["name"],client["last_name"], client["dni"], card)
        else:
            cli = VipClient(client["name"],client["last_name"], client["dni"]) 
       
        sale:Sale = Sale(ult_invoices,cli)
        gotoxy(35,6);print(cli.fullName())
        gotoxy(2,8);print(green_color+"*"*98+reset_color) 
        gotoxy(5,9);print(purple_color+"Linea") 
        gotoxy(12,9);print("Id_Articulo") #12
        gotoxy(26,9);print("Descripcion") #24
        gotoxy(46,9);print("Precio") #38
        gotoxy(56,9);print("Cantidad") #48
        gotoxy(70,9);print("Subtotal") #58
        gotoxy(81,9);print("n->Terminar Venta)"+reset_color)#70
        # detalle de la venta
        follow :str="s"
        line:int=1
        products_add:List[Any]=[]
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line)
            id:int=int(validar.solo_numeros("Error: Solo numeros",15,9+line))
            json_file_product:JsonFile = JsonFile(path+'/archivos/products.json')
            prods:List[Any] = json_file_product.find("id",id)
            list_products:List[Any]=json_file_product.read()
            if not prods:
                gotoxy(24,9+line);print("Producto no existe")
                time.sleep(1)
                gotoxy(24,9+line);print(" "*20)
            else:    
                prods:Dict[str,Any] = prods[0]
                
                product:Product = Product(prods["id"],prods["description"],prods["price"],prods["stock"])
                gotoxy(26,9+line);print(product.descrip)
                gotoxy(46,9+line);print(product.preci)
                sin_stock:bool=False
                while True:
                    qyt:int=int(validar.solo_numeros("Error:Solo numeros",57,9+line))
                    if prods['stock']==0:
                        sin_stock=True
                        break
                        
                    if prods['stock']<qyt: 
                        gotoxy(57,9+line);print('No hay stock suficiente')
                        time.sleep(2)
                        gotoxy(57,9+line);print(" "*60)
                        continue
                    else:
                        new_stock:int=prods['stock']-qyt
                        list_products:List[Dict[str,Any]]=[{**product,'stock':new_stock} if product['id']==id else product for product in list_products]
                        json_file_product.save(list_products)
                        break

                    
                if sin_stock:
                    gotoxy(7,9+line);print(" "*100)
                    show_error_and_clear(7,9+line,'Linea cancelada por falta de stock',red_color,reset_color,100)
                    continue
                gotoxy(71,9+line);print(product.preci*qyt)
                sale.add_detail(product,qyt)
                gotoxy(80,4);print(round(sale.subtotal,2))
                gotoxy(80,5);print(round(sale.discount,2))
                gotoxy(80,6);print(round(sale.iva,2))
                gotoxy(80,7);print(round(sale.total,2))
                gotoxy(82,9+line);follow=input() or "s"  
                gotoxy(89,9+line);print(green_color+"✔"+reset_color)
                products_add.append((prods['id'],qyt))
                line += 1

                
        gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9+line);procesar = input().lower()
        if procesar == "s":
            gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
            # print(sale.getJson())  
            
            data:Dict[str,Any] = sale.getJson()
            data["invoice"]=ult_invoices
            invoices.append(data)
            json_file_invoices.save(invoices)
           
               
        else:
            gotoxy(20,10+line);print(red_color+"Venta Cancelada"+reset_color)  
            for product in list_products:
                for id_product,quantity in products_add:
                    if product['id']==id_product:
                        product['stock']+=quantity
                        break
            json_file_product.save(list_products)      
        time.sleep(2)    
    
    def update(self)->None:
            validar=Valida()
            while True:
                print('\033c', end='')
                gotoxy(2,1);print(green_color+"█"*90)
                gotoxy(2,2);print("██"+" "*34+"Modificar Venta"+" "*37+"██")
                gotoxy(2,4);print("Ingrese id Factura: ")
                gotoxy(2,4);invoice_id:int=int(validar.solo_numeros(red_color+"Error: solo número"+green_color,22,4))
                json_file:JsonFile = JsonFile(path+'/archivos/invoices.json')
                json_products:JsonFile=JsonFile(path+'/archivos/products.json')
                
                list_invoices:List[Any]=json_file.read()
                invoice_found:List[str,Any]=json_file.find("invoice",invoice_id)
                if not invoice_found:
                    show_error_and_clear(22,4,"Factura no existe",red_color,green_color)
                    continue

                name_client,last_name=invoice_found[0]['client'].split(" ")
                if invoice_found[0]['payment_method']=='credito':
                    client=VipClient(name_client,last_name,invoice_found[0]['dni'])
                else:
                    client=RegularClient(name_client,last_name,invoice_found[0]['dni'],card=True)

                data:List[Tuple[Any]]=[]
                last_line:int=0
                for i,item in enumerate(invoice_found[0]['details']):
                    data.append((i+1,item['product'],item['price'],item['quantity'],item['quantity']*item['price']))
                    last_line=i

                opc:str=''
                while opc!='3':
                    borrarPantalla()
                    menu_clients:Menu = Menu("Menu Productos",["1) Modificar cantidad","2) Modificar a otro producto","3) Salir"],2,5)
                    opc = menu_clients.menu()
                    borrarPantalla()

                    show_tabulate(data,['ID','Descripción','Precio', 'Cantidad','Subtotal'])
                    print('\nModificar productos')
                    
                    gotoxy(5,8+last_line);print('Ingrese id producto: ')
                    line_product:int=int(validar.solo_numeros('Error: solo números',26,8+last_line))
                    if not line_product in range(1,len(invoice_found[0]['details'])+1):
                        show_error_and_clear(26,8+last_line,"Producto no existe",red_color,green_color)
                        continue
                    gotoxy(5,8+last_line);print(" "*60)

                    if opc=='1':
                        gotoxy(5,8+last_line);print('Nueva cantidad: ')
                        quantity=int(validar.solo_numeros('Error: solo numero',22,8+last_line))
                        break
                    elif opc=='2':
                        gotoxy(5,8+last_line);print('Otro producto (id): ')
                        id_product:int=int(validar.solo_numeros('Error: solo numero',25,8+last_line))
                        list_products:List[Any]=json_products.read()
                        product_found:List[Any]=json_products.find('id',id_product)
                        if not product_found:
                            show_error_and_clear(25,8+last_line,"Producto no existe",red_color,green_color)
                            continue
                        gotoxy(5,9+last_line);print('Nueva cantidad: ')
                        quantity:int=int(validar.solo_numeros('Error: solo numero',22,9+last_line))
                        if product_found[0]['stock']<quantity:
                            show_error_and_clear(22,9+last_line,"No hay suficiente stock",red_color,green_color,23)
                            continue

                        data:List[Dict[str,Any]]=[{**product,'stock':product_found[0]['stock']-quantity} if product['id']==id_product else product 
                              for product in list_products]
                        json_products.save(data)
                        break
                

                borrarPantalla()
                for invoice in list_invoices:
                    if invoice['invoice']==invoice_id: 
                        invoice["details"][line_product-1]["quantity"]=quantity
                        if opc=='2':
                            invoice["details"][line_product-1]['product']=product_found[0]["description"]
                            invoice["details"][line_product-1]["price"]=product_found[0]["price"]

                        new_subtotal:float=sum(product['price']*product['quantity'] for product in invoice['details'])
                        new_discount:float=new_subtotal*client.discount
                        new_iva:float=new_subtotal*0.12
                        total:float=new_subtotal+new_iva-new_discount
                        
                        invoice.update({
                             'subtotal': round(new_subtotal, 2),
                             'discount': round(new_discount, 2),
                             'iva': round(new_iva, 2),
                             'total': round(total, 2)
                         })
                        
                        json_file.save(list_invoices)
                        
                        print(green_color+"Se cambió correctamente"+reset_color)
                        break
                     
                if input('¿Quieres continuar modificando (s/n)?')=='n':
                    break

            
            input("presione una tecla para continuar...")  

    
    def delete(self)->None:
        validar = Valida()
        while True:
            print('\033c', end='')
            gotoxy(2,1);print(green_color+"█"*90)
            gotoxy(2,2);print("██"+" "*34+"Eliminar Venta"+" "*38+"██")
            gotoxy(2,4);print("Ingrese id Factura: ")
            gotoxy(2,4);invoice:int=int(validar.solo_numeros(red_color+"Error: solo número"+green_color,22,4))
            json_file:JsonFile = JsonFile(path+'/archivos/invoices.json')
            invoices:List[Any]=json_file.read()
            invoice_found:List[Any]=json_file.find("invoice",invoice)
            if not invoice_found:
                show_error_and_clear(22,4,"Factura no existe",red_color,green_color)
                continue
            filter_invoices:List[Dict[str,Any]]=[item for item in invoices if invoice!=item['invoice']]
            json_file.save(filter_invoices)
            print(green_color+"😊 Venta eliminada correctamente 😊"+reset_color)
            break

        input("presione una tecla para continuar...")  


        
    
    def consult(self)->None:
        validar=Valida()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Venta"+" "*35+"██")
        opc:str=''
        while opc!='3':
            borrarPantalla()
            menu_clients:Menu = Menu("Menu Compras",["1) Ver por id","2) Ver todas","3) Salir"],2,5)
            opc = menu_clients.menu()
            borrarPantalla()
            if opc=='1':
               gotoxy(2,4);print("Ingrese Factura: ")
               invoice:int=int(validar.solo_numeros("No valido",19,4))
               json_file:JsonFile = JsonFile(path+'/archivos/invoices.json')
               invoices_list:List[str,Any] = json_file.find("invoice",invoice)
               if not invoices_list:
                   show_error_and_clear(18,4,"Factura no existe",red_color,green_color)
                   continue
               invoices:Dict[str,Any]=invoices_list[0]
               print(f"Impresion de la Factura#{invoice}")
               print(f"Fecha: {invoices['date']}")
               print(f"Cliente: {invoices['client']}")
               data:List[Tuple[Any]]=[]
               for i,item in enumerate(invoices['details']):
                    data.append((i+1,item['product'],item['price'],item['quantity'],item['quantity']*item['price']))

               show_tabulate(data,["Id","Descripcion","Precio U","Cantidad","Subtotal"])
        
               print(f"Subtotal: {invoices['subtotal']}")
               print(f"Descuento: {round(invoices['discount'],2)}")
               print(f"Iva: {invoices['iva']}")
               print(f"Total: {invoices['total']}")
               input(reset_color+"\nPresione una tecla para continuar..."+green_color)
            elif opc=='2':    
               json_file:JsonFile = JsonFile(path+'/archivos/invoices.json')
               invoices:List[Any] = json_file.read()
               print("Consulta de Facturas")
               
               data:List[Any]=[(invoice['invoice'],invoice['date'],invoice['client'],invoice['total']) for invoice in invoices]
               
               show_tabulate(data,["Id","Fecha","Cliente","Total"])
            #    for fac in invoices:
            #        print(f"{fac['invoice']}    {fac['date']}   {fac['client']}   {fac['total']}")
               suma:float = reduce(lambda total, invoice: round(total+ invoice["total"],2), 
               invoices,0)
               totales_map:float = list(map(lambda invoice: invoice["total"], invoices))


               max_invoice:float = max(totales_map)
               min_invoice:float = min(totales_map)
               tot_invoices:float = sum(totales_map)
               # print("filter cliente: ",total_client)
               print(f"map Facturas:{totales_map}")
               print(f"              max Factura:{max_invoice}")
               print(f"              min Factura:{min_invoice}")
               print(f"              sum Factura:{tot_invoices}")
               print(f"              reduce Facturas:{suma}")
               input(reset_color+"\nPresione una tecla para continuar..."+green_color)
        
        borrarPantalla()
        input(reset_color+"\npresione una tecla para continuar...") 