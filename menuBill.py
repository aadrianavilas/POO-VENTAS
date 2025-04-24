from components import Menu,Valida
from utilities import borrarPantalla,gotoxy,show_error_and_clear,show_tabulate
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient,VipClient
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce
from typing import List,Dict, Any,Tuple
from tabulate import tabulate

path, _ = os.path.split(os.path.abspath(__file__))
# Procesos de las Opciones del Menu Facturacion
class CrudClients(ICrud):
    def create(self)->None:
        validar=Valida()
        borrarPantalla()
        print('\033c', end='')
        opc:str=''
        regular:bool=False
        card:bool
        while opc!='3':
            borrarPantalla()
            menu_clients = Menu("Menu Cientes",["1) Cliente Regular","2) Cliente Vip","3) Salir"],20,10)
            opc = menu_clients.menu()
            if opc in ['1','2']:
                regular=(opc=='1')
                if regular:
                    borrarPantalla()
                    answer:str=validar.solo_letras('Tiene tarjeta de credito (s/n): ','Error: solo letra',2,10)
                    card=True if answer=='s' else False  
                opc='3'          
            elif opc=='3':
                return      

        borrarPantalla()  
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Clientes")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        json_file:JsonFile=JsonFile(path+'/archivos/clients.json')
        while True:
            gotoxy(18,4);print('Dni: ')
            dni:str=validar.solo_numeros("Error: Solo numeros",23,4)
            client_json:List[Any]=json_file.find('dni',dni)
            if client_json:
                show_error_and_clear(23,4,'Error: dni registrado',red_color,blue_color,21)
                continue

            if not validar.cedula(dni):
                show_error_and_clear(23,4,'Cédula inválida',red_color,blue_color)
                continue
            break

        

        name:str=validar.solo_letras("Nombre: ",'Error: solo letras',18,5)
        last_name:str=validar.solo_letras("Apellido: ",'Error: solo letras',18,6)

        if regular:
            client=RegularClient(name,last_name,dni,card)
        else:
            client=VipClient(name,last_name,dni)

        data:Dict[str,Any]=client.getJson()
        
        json_file:JsonFile=JsonFile(path+'/archivos/clients.json')
        list_clients:List[Any]=json_file.read()
        list_clients.append(data)
        json_file.save(list_clients)
        print(green_color+'Se guardó correctamente'+reset_color)

        input('Presiona Enter para continuar...')

    def update(self)->None:
        validar=Valida()
        client_found:List[Any]=[]
        while not client_found:
            print('\033c', end='')
            gotoxy(2,1);print(green_color+"█"*90)
            gotoxy(2,2);print("██"+" "*34+"Modificar Cliente"+" "*35+"██")
            gotoxy(2,4);print("Ingrese dni: ")
            gotoxy(2,4);dni=validar.solo_numeros(red_color+"Error: solo número"+green_color,15,4)
            json_file:JsonFile = JsonFile(path+'/archivos/clients.json')
            client_found:List[Any]=json_file.find('dni',dni)
            if not client_found:
                show_error_and_clear(15,4,'Cliente no existe',red_color,green_color)
                continue
            client_dict:Dict[str,Any]=client_found[0]

        opc:str=''
        card:bool
        while True:
            borrarPantalla()
            menu_clients = Menu("Menu Cientes",["1) Cambiar a otro tipo de cliente","2) Modificar datos cliente","3) Salir"],2,5)
            opc = menu_clients.menu()
            borrarPantalla()
            if opc=='1':
                if client_dict['type']=='regular':
                    client=VipClient(client_dict['name'],client_dict['last_name'],client_dict['dni'])
                else:
                    answer=validar.solo_letras('¿Tiene tarjeta de credito (s/n)?: ','Error: solo letra',2,6)
                    card=True if answer=='s' else False
                    client=RegularClient(client_dict['name'],client_dict['last_name'],client_dict['dni'],card)
                data=client.getJson()
                break
            elif opc=='2':
                card:bool=False
                if client_dict['type']=='regular':
                    payment_method="efectivo" if client_dict['payment_method']=='tarjeta' else "tarjeta"
                    answer:str=validar.solo_letras(f'¿Cambiar a {payment_method} (s/n)?: ','Error: solo letra',2,6)
                    if answer=='s':
                        if payment_method=='tarjeta':
                            card=True
                    else: 
                        continue   
                    client=RegularClient(client_dict['name'],client_dict['last_name'],client_dict['dni'],card)
                else:
                    answer:str=validar.solo_letras(f'¿Desea cambiar el limite de crédito (s/n)?: ','Error: solo letra',2,6)
                    if answer=='s':
                        gotoxy(2,7);print("Limite de crédito [10000-20000]: ")
                        limit:int=int(validar.solo_numeros('Error:limite inválido',35,7))
                        client=VipClient(client_dict['name'],client_dict['last_name'],client_dict['dni'])
                        client.limit=limit
                    else: 
                        continue
                data:Dict[str,Any]=client.getJson()
                break
            elif opc=='3':
                return
        list_clients:List[Any]=json_file.read()
        for i,item in enumerate(list_clients):
            if item['dni']==dni:
                list_clients[i]=data
                break
        json_file.save(list_clients)
        print(green_color+'Se modificó correctamente'+reset_color)
        input('Presione Enter para continuar...')


        
    def delete(self):
        validar = Valida()
        while True:
            print('\033c', end='')
            gotoxy(2,1);print(green_color+"█"*90)
            gotoxy(2,2);print("██"+" "*34+"Eliminar Cliente"+" "*36+"██")
            gotoxy(2,4);print("Ingrese dni: ")
            gotoxy(2,4);dni=validar.solo_numeros(red_color+"Error: solo número"+green_color,15,4)
            json_file:JsonFile= JsonFile(path+'/archivos/clients.json')
            list_clients:List[Any]=json_file.read()
            client_found:List[Any]=json_file.find("dni",dni)
            if not client_found:
                show_error_and_clear(15,4,'Cliente no existe',red_color,green_color)
                continue
           
            list_clients:List[Dict[str,Any]]=[client for client in list_clients if client['dni']!=dni]
            json_file.save(list_clients)
            print('Se eliminó correctamente'+reset_color)
            if input('¿Quiere seguir eliminando (s/n)?')=='n':
                break
            input("presione una tecla para continuar...")  
            
        
    def consult(self):
        validar=Valida()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Cliente"+" "*35+"██")
        json_file:JsonFile= JsonFile(path+'/archivos/clients.json')
        list_client:List[Any]=json_file.read()


        opc:str=''
        while opc!='4':
            borrarPantalla()
            menu_clients:Menu = Menu("Menu Cientes",["1) Ver clientes","2) Ver cliente por dni","3) Ver cliente por tipo","4) Salir"],2,5)
            opc = menu_clients.menu()
            borrarPantalla()
            if opc=='1':
                new_list:List[Tuple[Any]]=[
                          (client['dni'],client['name'],client['last_name'],client['value'],
                           client['type']) 
                           for client in list_client
                         ]
                show_tabulate(new_list,['DNI','Nombre','Apellido','Valor','Tipo de cliente'])
                
            elif opc=='2':
                gotoxy(2,4);print("Ingrese dni: ")
                gotoxy(2,4);dni:str=validar.solo_numeros(red_color+"Error: solo número"+green_color,15,4)
                client_found:List[Any]=json_file.find('dni',dni)
                if not client_found:
                    show_error_and_clear(15,4,'Cliente no existe',red_color,green_color)
                    continue
                borrarPantalla()
                gotoxy(5,5);print(f"DNI: {dni}")
                gotoxy(5,6);print(f"Nombre: {client_found[0]['name']}")
                gotoxy(5,7);print(f"Apellido: {client_found[0]['last_name']}")
                gotoxy(5,8);print(f"Valor: {client_found[0]['value']}")
                gotoxy(5,9);print(f"Tipo de cliente: {client_found[0]['type']}")

            elif opc=='3':
                opc1:str=''
                type_client:bool=False
                while opc1!='3':
                    borrarPantalla()
                    menu_clients:Menu = Menu("Menu Cientes",["1) Regular","2) VIP","3) Salir"],2,5)
                    opc1 = menu_clients.menu()
                    borrarPantalla()
                    type_client:str='regular'
                    if opc1 in['1','2']:
                        if opc1=='1':
                            list_filter=json_file.find('type','regular')
                        elif opc1=='2':
                            list_filter=json_file.find('type','vip')
                            type_client='vip'
                        
                        new_list:List[Tuple[Any]]=[
                            (client['dni'],client['name'],client['last_name'],client['value'])
                            for client in list_filter
                        ]
                        print(f"Clientes {type_client}")
                        show_tabulate(new_list,['DNI','Nombre','Apellido','Valor'])
                        input(reset_color+'\n Presiona Enter para continuar...'+green_color)

            input(reset_color+'\nPresiona Enter para continuar...')









class CrudProducts(ICrud):
    def create(self):
        validar=Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Productos")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        gotoxy(18,4);print('Id: ')
        gotoxy(18,5);print('Descripción: ')
        gotoxy(18,6);print('Precio: ')
        gotoxy(18,7);print('Stock: ')

        file_json:JsonFile=JsonFile(path+'/archivos/products.json')
        list_products:List[Any]=file_json.read()
        if not list_products:
            last_id:int=1
        else: 
            last_id:int=list_products[-1]['id']+1
        gotoxy(22,4);print(last_id)
        while True:
            gotoxy(31,5);description_product:str=input('')
            if not description_product.strip():
                show_error_and_clear(31,5,'No válido',red_color,blue_color)
                continue
            break

        price_product:float=validar.solo_decimales("","Error: precio inválido",26,6)
        stock_product:int=int(validar.solo_numeros("Error: Solo numeros",25,7))
        product:Product=Product(last_id,description_product.lower(),price_product,stock_product)
        
        data:Dict[str,Any]=product.getJson()
        list_products.append(data)
        file_json.save(list_products)
        print(green_color+ '\nSe guardó correctamente'+reset_color)
        input('Presione Enter para continuar...')


    
    def update(self):
        validar=Valida()
        product_found:List[Any]=[]
        while not product_found:
            print('\033c', end='')
            gotoxy(2,1);print(green_color+"█"*90)
            gotoxy(2,2);print("██"+" "*34+"Modificar producto"+" "*35+"██")
            gotoxy(2,4);print("Ingrese id: ")
            gotoxy(2,4);id_product:int=int(validar.solo_numeros(red_color+"Error: solo número"+green_color,15,4))
            
            json_file:JsonFile = JsonFile(path+'/archivos/products.json')
            list_products:List[Any]=json_file.read()
            product_found:List[Any]=json_file.find('id',id_product)
            if not product_found:
                show_error_and_clear(15,4,'Producto no existe',red_color,green_color)
                continue

        gotoxy(2,5);print('Presiona Enter si no quiere modificar un producto')
        gotoxy(2,5);print(" "*60)
        gotoxy(20,6);print('Valor guardado')
        gotoxy(50,6);print('Valor nuevo')
        gotoxy(5,7);print('Descripción: ')
        gotoxy(5,8);print('Precio: ')
        gotoxy(5,9);print('Stock: ')
        gotoxy(20,7);print(product_found[0]['description'])
        gotoxy(20,8);print(product_found[0]['price'])
        gotoxy(20,9);print(product_found[0]['stock'])
        gotoxy(50,7);description_product:str=input() 
        gotoxy(50,8);price_product:str=input()
        gotoxy(50,9);stock_product:str=input()
        
        if not description_product.strip():
            description_product:str = product_found[0]['description']
            gotoxy(70, 7); print(red_color + "X" + green_color)

        if not price_product.replace('.', '', 1).isdigit():
            price_product:float = product_found[0]['price']
            gotoxy(70, 8);print(red_color + "X" + green_color)

        if not stock_product.isdigit():
            stock_product:int = product_found[0]['stock']
            gotoxy(70, 9);print(red_color + "X" + green_color)

        if description_product.lower()!=product_found[0]['description'].lower() or float(price_product)!=product_found[0]['price'] or int(stock_product)!=product_found[0]['stock']:
            gotoxy(2,11);input('Presiona una tecla para continuar...')
            gotoxy(50,7);print(" "*40)
            gotoxy(50,8);print(" "*40)
            gotoxy(50,9);print(" "*40)
            gotoxy(50,7);print(description_product)
            gotoxy(50,8);print(price_product)
            gotoxy(50,9);print(stock_product)
            gotoxy(2,11);print(" "*100)
            product_found[0].update({
                'description': description_product,
                'price': float(price_product),
                'stock': int(stock_product)
            })
            for i, item in enumerate(list_products):
                if item['id']==id_product:
                    list_products[i]=product_found[0]
                    break
            json_file.save(list_products)
            print("\nSe modificó exitosamente")
        else:
            print("\nIngrese valores diferentes")

        input(reset_color+'\nPresiona Enter para continuar...')
    
    def delete(self):
        validar = Valida()
        while True:
            print('\033c', end='')
            gotoxy(2,1);print(green_color+"█"*90)
            gotoxy(2,2);print("██"+" "*34+"Eliminar Venta"+" "*38+"██")
            gotoxy(2,4);print("Ingrese id: ")
            gotoxy(2,4);id_product=int(validar.solo_numeros(red_color+"Error: solo número"+green_color,14,4))
            json_file:JsonFile = JsonFile(path+'/archivos/products.json')
            product_found:List[Any]=json_file.find('id',id_product)
            if not product_found:
                show_error_and_clear(14,4,'Producto no encontrado',red_color,green_color)
                continue
            list_products:List[Any]=json_file.read()
            new_products:List[Dict[str,Any]]=[product for product in list_products if product['id']!=id_product]
            json_file.save(new_products)
            print('\nSe eliminó correctamente')
            if input(reset_color+"¿Quiere seguir eliminando (s/n)?: ")== 'n':
                return
            input(reset_color+'\nPresione Enter para continuar...')

    
    def consult(self):
        validar=Valida()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Cliente"+" "*35+"██")
        json_file:JsonFile= JsonFile(path+'/archivos/products.json')
        list_client=json_file.read()
        opc:str=''
        while opc!='3':
            borrarPantalla()
            menu_clients:Menu = Menu("Menu Productos",["1) Ver por id","2) Ver por stock","3) Salir"],2,5)
            opc = menu_clients.menu()
            borrarPantalla()
            if opc in ['1','2']:
                if opc=='1':
                    gotoxy(2,5);print('Ingrese id: ')
                    id_product:int=int(validar.solo_numeros('Id inválido',14,5))
                    list_filter_product:List[Any]=json_file.find('id',id_product)
                elif opc=='2':
                    opc1:str=''
                    list_products:List[Any]=json_file.read()
                    while opc1!='5':
                        borrarPantalla()
                        menu_clients:Menu = Menu(reset_color+"Menu Productos",["1) Stock vacio","2) Mayor a", "3) Menor a" ,"4) Igual a","5) Salir"],2,5)
                        opc1 = menu_clients.menu()
                        borrarPantalla()

                        if '1' <= opc1 <='4':
                            if opc1=='1':
                                list_filter_product:List[Any]=json_file.find('stock',0)
                            else: 
                                gotoxy(2,5);print('Ingrese stock: ')
                                stock_product:int=int(validar.solo_numeros('Stock inválido',18,5))
                                if opc1=='2':
                                    list_filter_product:List[Dict[str,Any]]=[product for product in list_products if product['stock']>stock_product]
                                elif opc1=='3':
                                    list_filter_product:List[Dict[str,Any]]=[product for product in list_products if product['stock']<stock_product]
                                elif opc1=='4':
                                    list_filter_product:List[Any]=json_file.find('stock',stock_product)

                            break


                if not list_filter_product:
                    print(red_color+'No hay productos'+green_color)
                    input(reset_color+'\nPresione Enter para salir...')
                    break

                list_product:List[Dict[str,Any]]=[
                                (product['id'],product['description'],product['price'],product['stock'])
                                for product in list_filter_product
                                ]
                show_tabulate(list_product,['ID','Descripción','Precio','Stock'])
            input(reset_color+'\nPresione Enter para continuar...')
                        
                        


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
       
        sale:Sale = Sale(cli)
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

#Menu Proceso Principal
opc:str=''
while opc !='4':  
    borrarPantalla()      
    menu_main:Menu = Menu("Menu Facturacion",["1) Clientes","2) Productos","3) Ventas","4) Salir"],20,10)
    opc = menu_main.menu()
    if opc == "1":
        opc1:str = ''
        while opc1 !='5':
            borrarPantalla()   
            client=CrudClients()
            menu_clients:Menu = Menu("Menu Cientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc1 = menu_clients.menu()
            if opc1 == "1":
                client.create()
            elif opc1 == "2":
                client.update()
            elif opc1 == "3":
                client.delete()
            elif opc1 == "4":
                client.consult()
            print("Regresando al menu Clientes...")
            # time.sleep(2)            
    elif opc == "2":
        opc2:str = ''
        while opc2 !='5':
            borrarPantalla()  
            product=CrudProducts()  
            menu_products:Menu = Menu("Menu Productos",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                product.create()
            elif opc2 == "2":
                product.update()
            elif opc2 == "3":
                product.delete()
            elif opc2 == "4":
                product.consult()
    elif opc == "3":
        opc3:str =''
        while opc3 !='5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales:Menu = Menu("Menu Ventas",["1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],20,10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales.create()
                
            elif opc3 == "2":
                sales.consult()
                time.sleep(2)

            elif opc3 == "3":
                sales.update()
                time.sleep(2)

            elif opc3 == "4":
                sales.delete()
                time.sleep(2)
     
    print("Regresando al menu Principal...")
    # time.sleep(2)            

borrarPantalla()

input("Presione una tecla para salir...")
borrarPantalla()

