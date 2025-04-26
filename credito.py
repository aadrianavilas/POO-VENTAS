class CreditoVenta:

    def __init__(self, id, cabecera_venta, total_credito,estado="Pendiente"):
        self.id = id
        self.cabecera_venta = cabecera_venta  # Objeto tipo CabVenta
        self.total_credito = total_credito
        self.saldo_credito = total_credito
        self.estado = estado  # "Pendiente", "Parcial", "Pagado"
        self.pagos = []  # Lista de PagosCredito


    def add_pay(self,id,date,value):
        pago=PagoCredito(id,date,value)
        self.pagos.append(pago)

    def getJson(self):
        # Método especial para representar la clase venta como diccionario
        credito= {"id":self.id,"id_invoice":self.cabecera_venta.invoice,"date":self.cabecera_venta.date.strftime("%Y-%m-%d"),"dni":self.cabecera_venta.dni
        ,"client":self.cabecera_venta.client.fullName(),"payment_method":self.cabecera_venta.payment_method,
        "subtotal":self.cabecera_venta.subtotal,"discount": self.cabecera_venta.discount,
        "iva": self.cabecera_venta.iva,"total": self.cabecera_venta.total,"saldo": self.saldo_credito,"state": self.estado,"details_pays":[]}
        for det in self.pagos:
            credito["details_pays"].append(
                {"id":det.id,
                "date_pay": det.fecha_pago,
                "value": det.valor}
            )  
        return credito

class PagoCredito:

    def __init__(self, id, fecha_pago, valor):
        self.id = id
        self.fecha_pago = fecha_pago
        self.valor = valor