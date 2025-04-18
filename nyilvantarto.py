from tkinter import *
from tkinter import ttk, messagebox
import customtkinter as ctk
import os
from models import Partner, Gyumolcsok, Kisszallitasok
from functions import kiszallitasok_listaz, partnerekListaz, gyumolcsokListaz, ujpartnerfelvitel, KiszallitasBeszur

#G:/01_python_maganorak/Julcsi/nyilvantarto/nyilvantarto

os.chdir('G:/01_python_maganorak/Julcsi/nyilvantarto/nyilvantarto')
#Új üzilala
class NyilvantartoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin felület")
        self.root.geometry("750x320")
        self.setup_gui()
        self.update_listak()

    def setup_gui(self):
        #alap ablak
        self.tab = ttk.Notebook(self.root)
        self.panel1 = ttk.Frame(self.tab)
        self.panel2 = ttk.Frame(self.tab)

        self.icon1 = PhotoImage(file="icon1.png")

        self.tab.add(self.panel1, text="Kiszállítások listázása", image=self.icon1, compound="left")
        self.tab.add(self.panel2, text=" Partnerek felvitele", image=self.icon1, compound="left")
        self.tab.pack(expand=1, fill='both')

        # Panel2: Partnerek felvitele
        
        Label(self.panel2, text="Név:").grid(row=0, column=0, pady=(20, 5))
        self.nev_entry = Entry(self.panel2)
        self.nev_entry.grid(row=0, column=1, pady=(20, 5))

        Label(self.panel2, text="Település:").grid(row=1, column=0, pady=(20, 5))
        self.telepules_entry = Entry(self.panel2)
        self.telepules_entry.grid(row=1, column=1, pady=(20, 5))

        self.gombpartnerek = ctk.CTkButton(self.panel2, text="Új partner mentése",
                                           command=self.ujpartnerfelvitel)
        self.gombpartnerek.grid(row=2, column=0, columnspan=2, pady=10)

        # Panel1: Kiszállítás felvitel
        Label(self.panel1,width="20", text="Kiszállítások listája", bg="#36719F", fg="white", font=("Arial", 12, "bold")).grid(row=0, columnspan=2, column=2, pady=(10, 10), padx=(20, 20))
        Label(self.panel1,width="20", text="Kiszállítások felvitele", bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).grid(row=0, columnspan=2, column=0, pady=(10, 10), padx=(20, 20))
        
        Label(self.panel1, text="Dátum:").grid(row=1, column=0, pady=(20, 5))
        self.datum_entry = Entry(self.panel1)
        self.datum_entry.grid(row=1, column=1, pady=(20, 5))

        Label(self.panel1, text="Partner név:").grid(row=2, column=0, pady=(20, 5))
        self.nev_listbox = ttk.Combobox(self.panel1, state="readonly",width="17")
        self.nev_listbox.grid(row=2, column=1, pady=(20, 5))

        Label(self.panel1, text="Kartonszám:").grid(row=3, column=0, pady=(20, 5))
        self.katronSz_entry = Entry(self.panel1)
        self.katronSz_entry.grid(row=3, column=1, pady=(20, 5))

        Label(self.panel1, text="Gyümölcs név:").grid(row=4, column=0, pady=(20, 5))
        self.gyumolcsnev_listbox = ttk.Combobox(self.panel1, state="readonly", width="17")
        self.gyumolcsnev_listbox.grid(row=4, column=1, pady=(20, 5))

        self.gomb = ctk.CTkButton(self.panel1, text="Adatok mentése", command=self.kiszallitas_beszur)
        self.gomb.grid(row=5, column=0, columnspan=2, pady=10)

        self.trv = ttk.Treeview(self.panel1, columns=("1", "2", "3", "4"), show='headings')
        self.trv.heading("1", text="Dátum")
        self.trv.heading("2", text="Partner név")
        self.trv.heading("3", text="Kartonszám")
        self.trv.heading("4", text="Gyümölcs név")
        self.trv.grid(row=1, column=2, rowspan=5, padx=10)
        
        self.trv.column("1", width=100, anchor="center")
        self.trv.column("2", width=140, anchor="w")
        self.trv.column("3", width=80, anchor="center")
        self.trv.column("4", width=120, anchor="w") 
        


        self.frissit_kiszallitasok()

    def update_listak(self):
        self.nev_listbox['values'] = [p.neve for p in partnerekListaz()]
        self.gyumolcsnev_listbox['values'] = [g.nev for g in gyumolcsokListaz()]

    def frissit_kiszallitasok(self):
        for item in self.trv.get_children():
            self.trv.delete(item)
        for i in kiszallitasok_listaz():
            self.trv.insert("", END, values=(i.datum, i.kontakt, i.karton, i.gynev))

   
    def ujpartnerfelvitel(self):
        ujpartnerfelvitel(self.nev_entry, self.telepules_entry)
        self.update_listak()

    def kiszallitas_beszur(self):
        KiszallitasBeszur(self.datum_entry, self.nev_listbox, self.katronSz_entry,
                          self.gyumolcsnev_listbox, self.trv)
        self.frissit_kiszallitasok()


root = Tk()
app = NyilvantartoApp(root)
root.mainloop()
