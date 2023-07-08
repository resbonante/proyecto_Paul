from tkinter import ttk
from tkinter import *
import sqlite3

class Productos:
    base = 'productos.db'# BASE DE DATOS

    def __init__(self, root):#creacion de la ventana
        self.wind = root
        self.wind.title("Los mejores productos ") # nombre de la ventana
        self.wind.geometry("850x600") # tamaño de la ventana

        frame1 = LabelFrame(self.wind, text="Repote  Del Producto", font=("Calibri", 14)) #cuadro 1  de la ventana
        frame2 = LabelFrame(self.wind, text="Referencia  Del Producto", font=("Calibri", 14))#cuadro 2

        frame1.pack(fill="both", expand="yes", padx=20, pady=10)# descripcion del cuadro 1
        frame2.pack(fill="both", expand="yes", padx=20, pady=10)# descripcion del cuadro 2


        self.trv = ttk.Treeview(frame1, columns=(1,2,3,4), show="headings", height="5")# para crear la tabla del cuadro 1
        self.trv.pack()

        # descripcion de las columnas de la tabla

        self.trv.heading(1, text="ID ")
        self.trv.heading(2, text="Nombre ")
        self.trv.heading(3, text="Precio ")
        self.trv.heading(4, text="Cantidad ")
        self.consulta()

        #creacion para el segundo recuadro (cuadro de referencias del producto)

        lbl1 = Label(frame2, text="ID ", width=20) #width para la creacion del cuadro pequeño del lado de id (ancho)
        lbl1.grid(row=0, column=0, padx=5, pady=3)
        self.ent1 = Entry(frame2)
        self.ent1.grid(row=0, column=1, padx=5, pady=3)

        lbl2 = Label(frame2, text="Nombre ", width=20)
        lbl2.grid(row=1, column=0, padx=5, pady=3)
        self.ent2 = Entry(frame2)
        self.ent2.grid(row=1, column=1, padx=5, pady=3)

        lbl3 = Label(frame2, text="Precio ", width=20)
        lbl3.grid(row=2, column=0, padx=5, pady=3)
        self.ent3 = Entry(frame2)
        self.ent3.grid(row=2, column=1, padx=5, pady=3)

        lbl4 = Label(frame2, text="Cantidad ", width=20)
        lbl4.grid(row=3, column=0, padx=5, pady=3)
        self.ent4 = Entry(frame2)
        self.ent4.grid(row=3, column=1, padx=5, pady=3)

# para crear los botones
        btn1 = Button(frame2, text="Agregar", command=self.Agregar, width=12, height=2)
        btn1.grid(row=5, column=0)

        btn2 = Button(frame2, text="Eliminar", command=self.Eliminar, width=12, height=2)
        btn2.grid(row=5, column=1)

        btn3 = Button(frame2, text="Actualizar", command=self.Actualizar, width=12, height=2)
        btn3.grid(row=5, column=2 )


# para conectarse con el documento
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.base) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
            return result

    def consulta(self):
        book = self.trv.get_children()# para interactuar con la tabla del documento
        for element in book:
            self.trv.delete(element)  
        query = 'SELECT id, nombre, precio, cantidad FROM articulos'    # para que se cojan los datos de la base de datos
        rows = self.run_query(query)
        for row in rows:
            self.trv.insert('', 0, text=row[1], values=row)    


        # validacion de datos que se quieren introducir

    def validar(self):  
        return len(self.ent1.get()) != 0 and len(self.ent2.get()) != 0 and len(self.ent3.get()) != 0 and len(self.ent4.get()) != 0

    # PARA EL BOTON AGREGAR
    def Agregar(self):
        if self.validar():
            query = 'INSERT INTO articulos VALUES(?,?,?,?)'
            parameters = (self.ent1.get(), self.ent2.get(), self.ent3.get(), self.ent4.get())      
            self.run_query(query, parameters)
            self.ent1.delete(0, END)#para introducir informacion dentro de la tabla
            self.ent2.delete(0, END)
            self.ent3.delete(0, END)
            self.ent4.delete(0, END)    
        else:
            print("no salvado")
        self.consulta()   # perimite interactuar con la tabla productos (articulos )  

# PARA EL BOTON ELIMINAR

    def Eliminar(self):
        try:
          self.trv.item(self.trv.selection())['text']
        except IndexError as e:
            return
        nombre = self.trv.item(self.trv.selection())['text']
        query = 'DELETE FROM articulos WHERE nombre = ?'
        self.run_query(query, (nombre,))
        self.consulta()

    # para el boton actualizar  
    def Actualizar(self):  
        try:
          self.trv.item(self.trv.selection())['text']
        except IndexError as e:
            return
        precio = self.trv.item(self.trv.selection())['values'][2]
        cantidad = self.trv.item(self.trv.selection())['values'][3]
        self.edit_wind = Toplevel()
        self.edit_wind.title("Actualizar")
        self.edit_wind.geometry("400x300")


        frame = LabelFrame(self.edit_wind, text="Actualizar Producto",  font=("Calibri", 12))
        frame.pack(fill="both", expand="yes", padx=20, pady=10)  

        Label(frame, text="Antiguo Precio:", width=15, font=("Calibri", 10)).grid(row=2, column=1, padx=10, pady=20)
        Entry(frame, textvariable = StringVar(frame, value = precio), state = 'readonly').grid(row=2, column=2)

        Label(frame, text="Nuevo Precio", width=15, font=("Calibri", 10)).grid(row=3, column=1)
        nue_vo = Entry(frame)
        nue_vo.grid(row=3, column=2)

        Label(frame, text="Antigua Cantidad:", width=15, font=("Calibri", 10)).grid(row=4, column=1, padx=10, pady=20)
        Entry(frame, textvariable = StringVar(frame, value = cantidad), state = 'readonly').grid(row=4, column=2)


        Label(frame, text="Nueva Cantidad", width=15, font=("Calibri", 10)).grid(row=5, column=1)
        nueva = Entry(frame)
        nueva.grid(row=5, column=2)

        Button(frame, text="Actualizar", command = lambda: self.edit_record(nue_vo.get(), precio, nueva.get(), cantidad), width=12, height=2).grid(row=7, column=2, pady=20)


    def edit_record(self, nue_vo, precio, nueva, cantidad):
        query = 'UPDATE articulos SET precio = ?, cantidad = ? WHERE precio = ? AND cantidad = ?'
        parameters = (nue_vo, nueva, precio, cantidad)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.consulta()    


if __name__ == '__main__':
    root = Tk()
    product = Productos(root)  
    root.mainloop()
