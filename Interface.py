# -*- coding: utf-8 -*-
"""
Fichier permettant de gérer l'interface

@author: Sarah CE-OUGNA
"""
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter
#import tkinter.ttk as ttk

####################################### INTERFACE ###################################################

class MyApplication(tkinter.Tk):

    def __init__(self, theData, *args, **kwargs):
        
        self.theData = theData
        tkinter.Tk.__init__(self, *args, **kwargs)
        tkinter.Tk.iconbitmap(self,default='questhead')
        tkinter.Tk.wm_title(self, "Projet Python")
        tkinter.Tk.geometry(self, "900x600")
                 
        self.container = tkinter.Frame(self)

        self.container.pack(side="top", fill="both", expand = True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        frame = PageAccueil(self.container, self, self.theData)

        self.frames[PageAccueil] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PageAccueil, self.theData)

    def show_frame(self, pageName, theData):
        frame = pageName(self.container, self, self.theData)
        self.frames[pageName] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
        
class PageAccueil(tkinter.Frame):

    def __init__(self, parent, controller, theData):
        self.theData = theData
        tkinter.Frame.__init__(self,parent)
        label = tkinter.Label(self, text="Accueil", font=("Arial", 18))

        label.pack(pady=10,padx=10)
        
        histoButton = tkinter.Button(self, text ="Histogrammes", command=lambda:controller.show_frame(PageHistogrammes, self.theData))
        mapButton = tkinter.Button(self, text ="Cartes", command=lambda:controller.show_frame(PageCartes, self.theData))
        histoButton.pack()
        mapButton.pack()
        
class PageHistogrammes(tkinter.Frame):

    def __init__(self, parent, controller, theData):
        self.theData = theData
        tkinter.Frame.__init__(self, parent)
        label = tkinter.Label(self, text="HISTOGRAMMES", font=("Arial", 18))
        label.pack(pady=10,padx=10)

        button1 = tkinter.Button(self, text="Retour à la page d'accueil",
                            command=lambda: controller.show_frame(PageAccueil, self.theData))
        button1.pack()
        
        f= theData.plotData(Figure(figsize=(10,10), dpi=100, tight_layout=True))

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

class PageCartes(tkinter.Frame):

    def __init__(self, parent, controller, theData):
        self.theData = theData
        tkinter.Frame.__init__(self, parent)
        label = tkinter.Label(self, text="CARTES", font=("Arial", 18))
        label.pack(pady=10,padx=10)
        button1 = tkinter.Button(self, text="Retour à la page d'accueil",
                            command=lambda: controller.show_frame(PageAccueil, self.theData))
        button1.pack()
        
        button2 = tkinter.Button(self, text="Positions individuelles",
                            command=theData.individual_geolocalisation)
        button3 = tkinter.Button(self, text="Fréquences par pays",
                            command=theData.frequency_geolocalisation)
        button4 = tkinter.Button(self, text="Zoom sur les Etats-Unis",
                            command=theData.usa_geolocalisation)
        
        button2.pack()
        button3.pack()
        button4.pack()
