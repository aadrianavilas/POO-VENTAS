from models.components import Menu,Valida
from utilities import borrarPantalla,gotoxy,show_error_and_clear,show_tabulate
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from models.clsJson import JsonFile
from models.company  import Company
from models.customer import RegularClient,VipClient
from models.iCrud import ICrud
from typing import List,Dict, Any,Tuple
from utilities import path

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


        
    def delete(self)->None:
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
            
        
    def consult(self)->None:
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

                    if opc1 in['1','2']:
                        type_client=["regular","vip"]
                        typ=type_client[int(opc1)-1]
                        list_filter=json_file.find('type',typ)
                        
                        new_list:List[Tuple[Any]]=[
                            (client['dni'],client['name'],client['last_name'],client['value'])
                            for client in list_filter
                        ]
                        if not new_list:
                            show_error_and_clear(2,2,f"No hay clientes {typ}",red_color,reset_color)
                            return
                        print(f"Clientes {typ}")
                        show_tabulate(new_list,['DNI','Nombre','Apellido','Valor'])
                        input(reset_color+'\n Presiona Enter para continuar...'+green_color)

            input(reset_color+'\nPresiona Enter para continuar...')
