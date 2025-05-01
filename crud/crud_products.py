
from models.components import Menu,Valida
from utilities import borrarPantalla,gotoxy,show_error_and_clear,show_tabulate
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from models.clsJson import JsonFile
from models.company  import Company
from models.product  import Product
from models.iCrud import ICrud
from typing import List,Dict, Any
from utilities import path

class CrudProducts(ICrud):
    def create(self)->None:
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


    
    def update(self)->None:
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
    
    def delete(self)->None:
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

    
    def consult(self)->None:
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
                        
                        
