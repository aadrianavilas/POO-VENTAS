from models.components import Menu
from utilities import borrarPantalla
import time
from crud import crud_clients,crud_credit_pay,crud_products,crud_sales


opc:str=''
while opc !='5':  
    borrarPantalla()      
    menu_main:Menu = Menu("Menu Facturacion",["1) Clientes","2) Productos","3) Ventas","4) Crédito","5) Salir"],20,10)
    opc = menu_main.menu()
    if opc == "1":
        opc1:str = ''
        while opc1 !='5':
            borrarPantalla()   
            client=crud_clients.CrudClients()
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
            product=crud_products.CrudProducts()  
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
            sales = crud_sales.CrudSales()
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
    elif opc == "4":
        opc4:str =''
        while opc4 !='5':
            borrarPantalla()
            credito = crud_credit_pay.CrudCredito()
            menu_credit:Menu = Menu("Menu Crédito",["1) Registro Crédito","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],20,10)
            opc4 = menu_credit.menu()
            if opc4 == "1":
                credito.create()
                
            elif opc4 == "2":
                credito.consult()
                time.sleep(2)

            elif opc4 == "3":
                credito.update()
                time.sleep(2)

            elif opc4 == "4":
                credito.delete()
                time.sleep(2)
     
    print("Regresando al menu Principal...")
    # time.sleep(2)            

borrarPantalla()

input("Presione una tecla para salir...")
borrarPantalla()

