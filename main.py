import tkinter as tk
from tkinter import scrolledtext as st
from tkinter import ttk
from consulta import Productos

# usuario, contraseña, schema
consu = Productos('********', '********', '********')


class ProgramaMain:

    def __init__(self):

        self.producto1 = consu
        self.ventana1 = tk.Tk()
        self.ventana1.title('SWEET S.A.')
        self.ventana1.resizable(0, 0)
        self.cuaderno1 = ttk.Notebook(self.ventana1)
        self.consulta()
        self.listado_completo()
        self.cuaderno1.grid(column=0, row=0, padx=10, pady=10)
        self.ventana1.mainloop()

    def consulta(self):

        self.ventana1.bind('<Return>', self.consultar)
        self.pagina1 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina1, text='Consultar stock')
        self.labelframe1 = ttk.LabelFrame(self.pagina1, text='Ingrese producto')
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)
        self.label1 = ttk.Label(self.labelframe1, text='Externo/Cod. Barras/Descripción')
        self.label1.grid(column=0, row=1, padx=4, pady=4)
        self.produc = tk.StringVar()
        self.entry_produc = ttk.Entry(self.labelframe1, textvariable=self.produc)
        self.entry_produc.grid(column=0, row=2, padx=4, pady=4)
        self.boton1 = ttk.Button(self.labelframe1, text='Consultar stock', command=self.consultar)
        self.boton1.grid(column=0, row=3, padx=4, pady=4)
        self.boton1.bind('<Button-1>', self.consultar)
        self.entry_produc.focus_set()

    def consultar(self, event):

        prod = str(self.produc.get())

        busca_producto = consu.busca_producto(prod)
        self.scrolledtext1.delete("1.0", tk.END)
        for i in busca_producto:
            item_code = str(i.get('Codigo Externo'))
            item_name = str(i.get('Descripcion'))
            item_stock = (i.get('Stock 01'))
            if item_stock < 0:
                item_stock = 0
            self.scrolledtext1.insert(tk.END, f"Ext: {item_code}\t\tDesc: {item_name}\t\t\t\t\t\tStock: {item_stock}\n\n")

        self.produc.set('')
        self.entry_produc.focus_set()

    def listado_completo(self):

        self.labelframe2=ttk.LabelFrame(self.pagina1, text="Listado completo")
        self.labelframe2.grid(column=0, row=5, padx=5, pady=10)
        self.scrolledtext1= st.ScrolledText(self.labelframe2, width=80, height=10)
        self.scrolledtext1.grid(column=0, row=12, padx=5, pady=10)


aplicacion1 = ProgramaMain()
