import tkinter 
from tkinter import *
import serial, serial.tools.list_ports
from tkinter import messagebox
from tkinter import ttk
from threading import Thread,Event
from os import path
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Sistema:
    def __init__(self):
    
        self.ventana = Tk()
        self.ventana.geometry("575x400")
        path=resource_path('facu.ico')
        self.ventana.iconbitmap(path)
        self.ventana.title("Programa de Prueba")
        self.color_de_pantalla()
        self.botones()
        self.selecion_puertos_velocidad()
        self.entradas()
        self.etiquetas()
        self.lista=[]
        self.pic = serial.Serial()
        self.pic.timeout=0.5
        self.senal= Event()
        self.hilo = None
        self.ventana.resizable(0,0)
        self.ventana.mainloop()
   
    
    def selecion_puertos_velocidad(self):

        self.puertos =[port.device for port in serial.tools.list_ports.comports()]
         
        self.Combo1 = ttk.Combobox(self.ventana, values = self.puertos,state = "readonly")
        self.Combo1.set("Seleccione un puerto")
        self.Combo1.grid(row=1,column=1)  
        
        velocidades =['1200','2400','4800','9600','19200','38400','115200']
        
        self.Combo2 = ttk.Combobox(self.ventana, values = velocidades,state = "readonly")
        self.Combo2.set('Baudios')
        self.Combo2.place(x=337,y=130)
         
     
    def color_de_pantalla(self):
        path=resource_path('fondo.png')
        self.img = tkinter.PhotoImage(file = path)
        self.lbl_img = tkinter.Label(self.ventana,image = self.img).place(x=1,y=1)
        
    def habilitaciones(self):
        self.boton.config(state='normal')
        self.boton1.config(state='normal')
        self.boton2.config(state='normal')
        self.boton3.config(state='normal') 
        self.boton4.config(state='normal')
        self.boton5.config(state='normal') 
        self.boton6.config(state='normal')
        self.entrada_texto.config(state='normal')
        self.salida_texto.config(state='normal')
        self.botond.config(state='normal')
        self.botonc.config(state='disable')      #'#00fff7')
        

    def funcionA(self):    
        dato = bytes("A",'UTF-8')
        self.pic.write(dato)   
    def funcionB(self): 
        dato = bytes("B",'UTF-8')
        self.pic.write(dato)     
    def funcionC(self):
        dato = bytes("C",'UTF-8')
        self.pic.write(dato)            
    def funcionD(self):  
        dato = bytes("D",'UTF-8')
        self.pic.write(dato) 
    def funcionE(self):
        dato = bytes("E",'UTF-8')
        self.pic.write(dato)          
    def funcionF(self):  
        dato = bytes("F",'UTF-8')
        self.pic.write(dato) 
         
    def Enviar_Texto(self):
        self.dato_entrada=self.entrada_texto.get(0.0,"end")
        self.dato_entrada=self.dato_entrada.replace('\n',"")
        dato = bytes(f"{self.dato_entrada}",'UTF-8')
        self.pic.write(dato)


    def conexion(self):
        try:
            self.pic=serial.Serial(f"{self.Combo1.get()}",f"{self.Combo2.get()}")

        except:
            messagebox.showerror("Problema de conexion","Presione salir y inicie de nuevo \n o desconecte el dispositivo y vuelva a conectarlo")
        
        if self.pic.is_open:
            self.habilitaciones()
            self.iniciar_hilo()

      
        
    def salir(self):
        self.ventana.destroy()
    
    def desconectar(self):
        self.pic.close()      
        self.stop_hilo()
        self.botonc.config(state='normal')  
        self.botond.config(state='enable')
    def leer_datos(self):
        
        while self.senal.isSet() and self.pic.isOpen():
            data=self.pic.readline().decode("UTF-8").strip()
            if len(data)>1:
                self.lista.append(data)
                self.salida_texto.insert(0,self.lista[-1])
            
        
    def iniciar_hilo(self):
        self.hilo=Thread(target=self.leer_datos)
        self.hilo.setDaemon(1)
        self.senal.set()
        self.hilo.start()
    def stop_hilo(self):
        if (self.hilo is not None):
            self.senal.clear()
            self.hilo.join()
            self.hilo = None
    def botones(self):
        
        self.boton = Button(self.ventana,text="Enviar",command=self.Enviar_Texto)
        self.boton.config(state='disable',font=('Arial',12,'bold'),bg='#0083ff',fg='#ffffff')        #'#00fff7')
        self.boton.grid(row=2,column=0)
        

        self.botonc= Button(self.ventana,text="Conectar",command=self.conexion)
        self.botonc.config(state='normal',font=('Arial',12,'bold'),bg='#0083ff',width=10)        #'#00fff7')
        self.botonc.place(x=330,y=180)
        
        self.botond = Button(self.ventana,text="Desconectar",command=self.desconectar)
        self.botond.config(state='disable',font=('Arial',12,'bold'),bg='#0083ff',width=10)        #'#00fff7')
        self.botond.place(x=450,y=180)
        

        self.boton1 = Button(self.ventana,text="A",command=self.funcionA)
        self.boton1.config(state='disable',font=('Arial',12,'bold'),bg='#0083ff',width=10,fg='#ffffff')        #'#00fff7')
        self.boton1.place(x=10,y=250)
        
        self.boton2 = Button(self.ventana,text="B",command=self.funcionB)
        self.boton2.config(state='disable',font=('Arial',12,'bold'),bg='#0083ff',width=10,fg='#ffffff')        #'#00fff7')
        self.boton2.place(x=150,y=250)
        
        self.boton3 = Button(self.ventana,text="C",command=self.funcionC)
        self.boton3.config(state='disable',font=('Arial',12,'bold'),bg='#0083ff',width=10,fg='#ffffff')        #'#00fff7')
        self.boton3.place(x=10,y=300)
        
        self.boton4 = Button(self.ventana,text="D",command=self.funcionD)
        self.boton4.config(state='disable',font=('Arial',12,'bold'),bg='#0083ff',width=10,fg='#ffffff')        #'#00fff7')
        self.boton4.place(x=150,y=300)
        
        self.boton5 = Button(self.ventana,text="E",command=self.funcionE)
        self.boton5.config(state='disable',font=('Arial',12,'bold'),bg='#0083ff',width=10,fg='#ffffff')        #'#00fff7')
        self.boton5.place(x=10,y=350)
        
        self.boton6 = Button(self.ventana,text="F",command=self.funcionF)
        self.boton6.config(state='disable',font=('Arial',12,'bold'),bg='#0083ff',width=10,fg='#ffffff')        #'#00fff7')
        self.boton6.place(x=150,y=350)
        

        self.bsalir = Button(self.ventana,text="Salir",command=self.salir)
        self.bsalir.config(state='normal',font=('Arial',12,'bold'),bg='#ff0400',width=10,fg='#ffffff')        #'#00fff7')
        self.bsalir.place(x=450,y=360)
                      

    def entradas(self):
        
        self.entrada_texto = Text(self.ventana)
        self.entrada_texto.config(state='disable',width=20,height=5,font=('Arial',20),bg='#00b6ff',fg='#ffffff')
        self.entrada_texto.grid(row=1,column=0)

        self.salida_texto=Listbox(self.ventana,width=20,height=4,font=('Arial',15,'bold'))
        self.salida_texto.grid(row=4,column=1,columnspan=2,)
        

    def etiquetas(self):
        
        self.etiqueta = Label(self.ventana,text="LAB. MICROPROCESADORES I")
        self.etiqueta.config(font=('Arial',15,'bold'),bg='#194c6b',fg='#ffffff',width=25)
        self.etiqueta.grid(row=0,column=0) 
        
        self.etiqueta0 = Label(self.ventana,text="PUERTO")
        self.etiqueta0.config(font=('Arial',15,'bold'),bg='#194c6b',fg='#ffffff',width=22,height=1)
        self.etiqueta0.grid(row=0,column=1,columnspan=2,sticky="we")    
 
        self.etiqueta2 = Label(self.ventana,text="SALIDA DE MICROCONTROLADOR")
        self.etiqueta2.config(font=('Arial',10,'bold'),bg='#194c6b',fg='#ffffff',width=20)
        self.etiqueta2.grid(row=3,column=1,sticky="we",columnspan=2)

if __name__=="__main__":    
    objeto=Sistema()





# Aqui creamos el thread.
# El primer argumento es el nombre de la funcion que contiene el codigo.
# El segundo argumento es una lista de argumentos para esa funcion .
# Ojo con la coma al final!

