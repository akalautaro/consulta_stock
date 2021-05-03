from hdbcli import dbapi


class Productos:

    conn = dbapi.Connection
    user = '********'
    passwd = '********'
    schema = '********'
    host = '***.**.**.*'
    port = ********

    def __init__(self, user, passwd, schema):

        self.user = user
        self.passwd = passwd
        self.schema = schema
        self.conn = dbapi.connect(address=self.host, port=self.port, user=self.user, password=self.passwd)

        sql = "set schema " + self.schema
        cursor = self.conn.cursor()
        cursor.execute(sql)

    @staticmethod
    def list_to_dict(cursor: dbapi.Connection.cursor):
        dict_rows = [dict(zip(list(zip(*cursor.description))[0], row)) for row in cursor.fetchall()]
        return dict_rows

    def busca_producto(self, produc):

        sql = (f"""
                select distinct oitm."ItemCode" as "Codigo Externo", "ItemName" as "Descripcion", 
                case when oitm."CodeBars" is null then '' else oitm."CodeBars" end as "Codigo de barras",
                --"SalUnitMsr" as "Unidad de venta", cast(oitm."NumInSale" as integer) as "Unidad x bulto",
                (SELECT (cast("OnHand" as integer)-cast("IsCommited" as integer)) from staging.oitw where "ItemCode" = oitm."ItemCode" and oitw."WhsCode" = '01') as "Stock 01"
                --(SELECT (cast("OnHand" as integer)-cast("IsCommited" as integer)) from staging.oitw where "ItemCode" = oitm."ItemCode" and oitw."WhsCode" = 'MAX') as "Stock MAX",
                --(SELECT (cast("OnHand" as integer)-cast("IsCommited" as integer)) from staging.oitw where "ItemCode" = oitm."ItemCode" and oitw."WhsCode" = 'NOCADM') as "Stock NOCADM",
                --(SELECT (cast("OnHand" as integer)-cast("IsCommited" as integer)) from staging.oitw where "ItemCode" = oitm."ItemCode" and oitw."WhsCode" = 'RSPENA') as "Stock RSPENA"
                from staging.oitm inner join staging.oitw on oitm."ItemCode" = oitw."ItemCode"
                where oitm."SellItem" = 'Y' and oitm."InvntItem" = 'Y' 
                and contains(oitm."ItemCode" , '%{produc}%', FUZZY(0.5)) or contains(oitm."ItemName" , '%{produc}%', FUZZY(0.5)) or contains(oitm."CodeBars" , '%{produc}%', FUZZY(0.5))
                """)

        cur = self.conn.cursor()
        cur.execute(sql)
        prod = self.list_to_dict(cur)
        cur.close()
        return prod
