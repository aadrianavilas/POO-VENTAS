from models.components import Menu,Valida
from utilities import borrarPantalla,gotoxy,show_error_and_clear,show_tabulate
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from models.clsJson import JsonFile
from models.company  import Company
from models.customer import VipClient
from models.credito import CreditoVenta
from models.sales import Sale
from models.iCrud import ICrud
import time,os
from typing import List,Dict, Any
from utilities import path

class CrudCredito(ICrud):
    def create(self)->None:
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        while True:
            borrarPantalla()
            json_file_invoices:JsonFile = JsonFile(path+'/archivos/invoices.json')
            json_file_creditos:JsonFile = JsonFile(path+'/archivos/pago_creditos.json')

            gotoxy(2,1);print(green_color+"*"*98+reset_color)
            gotoxy(33,2);print(blue_color+"Registro de Pago a Crédito")
            gotoxy(23,3);print(blue_color+Company.get_business_name())
            gotoxy(15,4);print(f"Factura#: ")
            gotoxy(15,5);print(f"Fecha: ")
            gotoxy(81,4);print("TOTAL: ")
            gotoxy(81,5);print("SALDO: ")
            gotoxy(81,6);print("ESTADO: ")
            gotoxy(15,6);print("id: ")
            gotoxy(33,6);print("Cédula: ")
        
            date=validar.date(22,5)
            id_invoice:str=int(validar.solo_numeros("Id inválido",19,6,14))
            invoice_found=json_file_invoices.find("invoice",id_invoice)
            
            if not invoice_found:
                show_error_and_clear(23,6,'No existe',red_color,blue_color,)
                continue
            invoice=invoice_found[0]
            if invoice["payment_method"]!="credito":
                gotoxy(33,6);print(" "*20)
                show_error_and_clear(19,6,'Cliente Regular no puede pagar por crédito',red_color,blue_color,70)
                time.sleep(2)
                continue
            break


        credito_found=json_file_creditos.find("id_invoice",id_invoice)
        total=invoice["total"]
        estado="Pendiente"
        saldo_saved=total
        if credito_found:
            saldo_saved=credito_found[0]["saldo"]
            total=saldo_saved
            estado=credito_found[0]["state"]
            
        total_actual=total
        

        if saldo_saved==0:
            borrarPantalla()
            print(reset_color+"Ya haz pagado todo")
            input("\nPresiona una tecla para continuar...")
            return 
        
        print(reset_color)
        gotoxy(25,4);print(f"{invoice['invoice']:04d}")
        gotoxy(89,4);print(invoice['total'])
        gotoxy(89,5);print(saldo_saved)
        gotoxy(89,6);print(estado)
        gotoxy(41,6);print(invoice['dni'])
        gotoxy(55,6);print(invoice['client'])
        print(blue_color)
        gotoxy(2,8);print(green_color+"*"*98+reset_color) 
        gotoxy(5,9);print(purple_color+"Linea") 
        gotoxy(14,9);print("Valor") #12
        gotoxy(30,9);print("Estado") #24
        gotoxy(50,9);print("n->Terminar Venta)"+reset_color)

        
        list_creditos=json_file_creditos.read()
        if not list_creditos:
            last_id=1
        else:
            last_id=list_creditos[-1]['id']+1

        name,last_name=invoice['client'].split(" ")
        client=VipClient(name,last_name,invoice["dni"])
        sales=Sale(invoice['invoice'],client)
        sales.iva=invoice['iva']
        sales.subtotal=invoice['subtotal']
        sales.total=invoice['total']
        sales.discount=invoice["discount"]
        credito=CreditoVenta(last_id,sales,invoice['total'])
        follow :str="s"
        line:int=1
        is_newpay=True
        is_allpay=False
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line)
            if is_allpay:
                show_error_and_clear(2,9+line,"Ya haz pagado todo",green_color,reset_color)
                break
            valor=validar.solo_decimales("","Error: Solo numeros",15,9+line)
            saldo=round(total_actual-valor,2)
            total_actual=saldo
        
            if saldo<0:
                total_actual+=valor
                show_error_and_clear(15,9+line,f"Tu deuda es {round(total_actual,2)} y el valor debe ser menor o igual",red_color,reset_color,100)
                continue
            
            if total!=saldo:
                estado="Parcial"
            if saldo==0:
                estado="Pagado"
                is_allpay=True
                
            gotoxy(30,9+line);print(estado)  
            gotoxy(89,5);print(" "*10)
            gotoxy(89,6);print(" "*10)
            gotoxy(89,5);print(saldo) 
            gotoxy(89,6);print(estado)  
                    
            if credito_found:
                if is_newpay:
                    last_idpay=credito_found[0]['details_pays'][-1]['id']+1
                    is_newpay=False
                else:
                    last_idpay+=1
            else:
                last_idpay=1
            credito.add_pay(last_idpay,date,valor)
            gotoxy(54,9+line);follow=input() or "s"  
            gotoxy(57,9+line);print(green_color+"✔"+reset_color)
            line += 1       

        gotoxy(15,9+line);print(red_color+"Esta seguro de grabar el pago(s/n):")
        gotoxy(54,9+line);procesar = input().lower()
        if procesar == "s":
            data:Dict[str,Any] = credito.getJson()
            if credito_found:
                details=data['details_pays']
                credito_found[0].update({
                'state':estado,
                'saldo':saldo
                })
                for item in details:
                    credito_found[0]['details_pays'].append(item)
                for i,credito in enumerate(list_creditos):
                    if credito['id_invoice']==id_invoice:
                        list_creditos[i]=credito_found[0]
            else:
                data.update({
                'state':estado,
                'saldo':saldo
                })
                list_creditos.append(data)
            
            json_file_creditos.save(list_creditos)

            gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
           
        else:
            gotoxy(20,10+line);print(red_color+"Venta Cancelada"+reset_color)       
        time.sleep(2)

    def update(self)->None: 
        validar=Valida()
        while True:
            print('\033c', end='')
            gotoxy(2,1);print(green_color+"█"*90)
            gotoxy(2,2);print("██"+" "*34+"Modificar Venta"+" "*37+"██")
            gotoxy(2,4);print("Ingrese id credito: ")
            gotoxy(2,4);id_credito:int=int(validar.solo_numeros(red_color+"Error: solo número"+green_color,22,4))
            json_file:JsonFile = JsonFile(path+'/archivos/pago_creditos.json')
            list_creditos:List[Any]=json_file.read()
            credito_found:List[Any]= json_file.find("id", id_credito)
                
            if not credito_found:
                show_error_and_clear(22,4,"No existe",red_color,green_color)
                continue
            break

        opc:str=''
        while opc!='3':
            borrarPantalla()
            menu_clients:Menu = Menu("Menu Productos",["1) Modificar fecha de abono","2) Modificar abono","3) Salir"],2,5)
            opc = menu_clients.menu()
            borrarPantalla()
            
            if opc in ['1','2']:
                gotoxy(2,4);print("Id de detalle compra: ")
                id_detail=gotoxy(2,4);id_detail:int=int(validar.solo_numeros(red_color+"Error: solo número"+green_color,24,4))
                details_found=[detail for detail in credito_found[0]['details_pays'] if detail['id']==id_detail ]
                if not details_found:
                    show_error_and_clear(24,4,"No existe",red_color,green_color)
                    continue
                gotoxy(2,4);print(''*50)
                key="date_pay"
                new_value=''
                if opc=='1':
                    gotoxy(2,5);print("Nueva Fecha: ")
                    new_value=validar.date(15,5)
                
                elif opc=='2':
                    saldo_saved=credito_found[0]['saldo']
                    if saldo_saved==0:
                        show_error_and_clear(2,5,"No se puede moficar el saldo porque ya ha sido pagado",red_color,reset_color)
                        continue

                    while True:
                        credito_found:List[Any]= json_file.find("id", id_credito)
                        gotoxy(2,5);print("Nueva abono: ")
                        new_value=validar.solo_decimales("","Error: Solo numeros",15,5)
                        key="value"
                        value_saved=credito_found[0]['details_pays'][id_detail-1]['value']
                        saldo_saved=credito_found[0]['saldo']
                        saldo_now=saldo_saved-new_value
                        state=credito_found[0]['state']
                        if saldo_now<0:
                            show_error_and_clear(15,5,f"Debe {round(saldo_saved,2)} no puede ser mayor la cantidad a abonar",red_color,green_color,70)
                            continue
                        elif saldo_now==0:
                            state="Pagado"
                        new_value+=value_saved
                        break
                    credito_found[0].update({
                        "saldo":saldo_now,
                        "state":state
                    })
                credito_found[0]['details_pays'][id_detail-1].update({
                    key:new_value
                })
                for i,credito in enumerate(list_creditos):
                    if credito['id']==id_credito:
                        list_creditos[i]=credito_found[0]
                json_file.save(list_creditos)
                print(green_color+"Se cambió correctamente"+reset_color)
            input(reset_color+"\nPresione Enter para continuar")


                

    def delete(self)->None:
        validar = Valida()
        while True:
            print('\033c', end='')
            gotoxy(2,1);print(green_color+"█"*90)
            gotoxy(2,2);print("██"+" "*34+"Eliminar pago a Crédito"+" "*29+"██")
            gotoxy(2,4);print("Ingrese id crédito: ")
            gotoxy(2,4);id_credito:int=int(validar.solo_numeros(red_color+"Error: solo número"+green_color,22,4))
            json_file:JsonFile = JsonFile(path+'/archivos/pago_creditos.json')
            list_invoices:List[Any]=json_file.read()
            credito_found:List[Any]= json_file.find("id", id_credito)
            if not credito_found:
                show_error_and_clear(22,4,"Factura no existe",red_color,green_color)
                continue
            filter_creditos:List[Dict[str,Any]]=[item for item in list_invoices if id_credito!=item['id']]

            json_file.save(filter_creditos)
            print(green_color+"😊 Venta eliminada correctamente 😊"+reset_color)
            break

        input("presione una tecla para continuar...")

    def consult(self)->None:
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Pago a Crédito"+" "*35+"██")
        json_file:JsonFile= JsonFile(path+'/archivos/pago_creditos.json')
        json_file_invoices:JsonFile= JsonFile(path+'/archivos/invoices.json')
        list_sales_vip=json_file_invoices.find("payment_method","credito")
        list_creditos:List[Any]=json_file.read()
        opc:str=''
        while opc!='4':
            borrarPantalla()
            menu_clients:Menu = Menu("Menu Cientes",["1) Ver total","2) Ver por estado","3) Por adeudor","4) Salir"],2,5)
            opc = menu_clients.menu()
            borrarPantalla()
            if opc=='1':
                total_credito=sum([credito['total'] for credito in list_creditos])
                total_rest=sum([credito['saldo'] for credito in list_creditos if credito['state']=='Parcial' or credito["state"]=="Pendiente"])
                all_total=sum([invoice['total'] for invoice in list_sales_vip])
                print("                    TOTAL                            \n")
                print(f"Total esperado de créditos iniciados: {total_credito}")
                print(f"Suma de saldos que faltan por pagar: {total_rest}")
                print(f"Total general de ventas a crédito: {all_total}")
                
            elif opc=='2':
                opc1:str=''
                while opc1!='4':
                    borrarPantalla()
                    menu_clients:Menu = Menu("Menu Cientes",["1) Pendiente","2) Parcial","3) Pagado","4) Salir"],2,5)
                    opc1 = menu_clients.menu()
                    borrarPantalla()
                    if opc1 in ['1','2','3']:
                        list_state=["Pendiente","Parcial","Pagado"]
                        list_filter=[(credito['id'],credito['dni'],credito['client'],credito['total'],credito['saldo']) 
                                     for credito in list_creditos if credito['state']==list_state[int(opc1)-1]]
                        if not list_filter:
                            show_error_and_clear(5,2,"No hay pagos pendientes",red_color,reset_color,25)
                            break
                        show_tabulate(list_filter,['Id','DNI','Cliente','Total','Saldo'])
                        total=sum([credito[3] for credito in list_filter])
                        saldo_total=sum([credito[4] for credito in list_filter])
                        print(f"Saldo total por pagar: ${saldo_total}")
                        print(f"Total: ${total}")
                        input(reset_color+'\nPresiona Enter para continuar...')
            elif opc=='3':
                opc2:str=''
                while opc2!='3':
                    borrarPantalla()
                    menu_clients:Menu = Menu("Menu Cientes",["1) Adeudor menor","2) Adeudor mayor","3) Salir"],2,5)
                    opc2 = menu_clients.menu()
                    borrarPantalla()
                    if opc2 in ['1','2']:
                        list_filter=json_file.find("state","Parcial")
                        if not list_filter:
                            show_error_and_clear(5,2,"No adeudores",red_color,reset_color,25)
                            break

                        
                        pay=min(list_filter, key=lambda x: x['saldo']) if opc2=='1' else max(list_filter, key=lambda x: x['saldo'])

                        print(blue_color)
                        print(f"Cédula: {pay["dni"]}")    
                        print(f"Cliente: {pay["client"]}")
                        print(f"TOTAL: {pay["total"]}")
                        print(f"SALDO: {red_color}{pay["saldo"]}{blue_color}")
                        print(f"ABONADO: {red_color}{round(pay["total"]-pay["saldo"],2)}")

                        input(reset_color+'\nPresiona Enter para continuar...')

            
            input(reset_color+'\nPresiona Enter para continuar...')
