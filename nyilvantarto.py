from tkinter import *
from tkinter import ttk, Menu
import mysql.connector
from mysql.connector import Error
import customtkinter as ctk
import os
from tkinter import messagebox

#comment teszt
os.chdir('G:/05_adatbáziskezelés/Julcsi/gyumolcs')

class Gyumolcsok:
    def __init__(self, id, nev):
        self.id = id
        self.nev = nev

class Partner:
   def __init__(self, az, neve, telepules):
      self.az = az
      self.neve = neve
      self.telepules = telepules
       

class Kisszallitasok:
   def __init__(self, datum, Partner, karton, gynev):
      self.datum = datum
      self.kontakt = Partner
      self.karton = karton
      self.gynev = gynev
   

def db_connect():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="nyilvantartas"
        )
        if conn.is_connected():
            print("Sikeresen csatlakoztál az adatbázishoz!")
            return conn
        else:
            print("Nem sikerült csatlakozni az adatbázishoz.")
            return None
    except Error as e:
        print(f"Hiba a kapcsolódáskor: {e}")
        return None

def kiszallitasok_listaz():
   # adatbázis kapcsolat létrehozása
   conn = db_connect()
   # lehetővő teszti az sql parancsok lefuttatását
   cursor = conn.cursor()
   query = "SELECT k.datum, p.kontakt, k.karton, gy.gynev \
      from kiszallitasok k JOIN partnerek p ON k.partnerid = p.partnerid\
         JOIN gyumolcslevek gy ON gy.gyumolcsleId = k.gyumleid \
            ORDER BY k.datum DESC;"
   cursor.execute(query)

   kiszallitasok = []
   for i in cursor.fetchall(): #  [2025-11-10 , Pál Pál ,  100 , bodzalé]
       k = Kisszallitasok(i[0],i[1],i[2],i[3])
       kiszallitasok.append(k)

   cursor.close()
   conn.close()   
   return kiszallitasok

def partnerekListaz():
   # adatbázis kapcsolat létrehozása
   conn = db_connect()
   # lehetővő teszti az sql parancsok lefuttatását
   partnerek = []
   cursor = conn.cursor()
   query = "select * from partnerek"
   cursor.execute(query)
   for i in cursor.fetchall():
      p = Partner(i[0],i[1],i[2])
      partnerek.append(p)

   cursor.close()
   conn.close()  
   return partnerek

def partnerekfelvitel():
   conn = db_connect()
   cursor = conn.cursor()


def gyumolcsokListaz():
   # adatbázis kapcsolat létrehozása
   conn = db_connect()
   # lehetővő teszti az sql parancsok lefuttatását
   gyumolcsok = []
   cursor = conn.cursor()
   query = "select * from gyumolcslevek"
   cursor.execute(query)
   for i in cursor.fetchall():
      p = Gyumolcsok(i[0],i[1])
      gyumolcsok.append(p)

   cursor.close()
   conn.close()  
   return gyumolcsok

def ujpartnerfelvitel():
   conn = db_connect()
   cursor = conn.cursor()
   try:
      nev =nev_entry.get()
      telepules = telepules_entry.get()
      query =  f"INSERT INTO partnerek (partnerid, kontakt, telepules) VALUES('', '{nev}', '{telepules}')"
      cursor.execute(query)
      conn.commit()
      messagebox.showinfo("Ok", "Sikeres beszúrás")
   except:
       messagebox.showerror("Hiba", "Valami hiba van")
   conn.close()      
      
def KiszallitasBeszur():
   # adatbázis kapcsolat létrehozása
   conn = db_connect()
   cursor = conn.cursor()
   # lehetővő teszti az sql parancsok lefuttatását
  
   try:
      datum = datum_entry.get()
      print(datum)
      nev = nev_listbox.get()
      karton = katronSz_entry.get()
      karton = int(karton)
      print(karton)


      p = partnerekListaz()
      partnerID  = ""
      for i in p:
         if i.neve == nev:
            partnerID = i.az
      print(partnerID)     
      gyumneve = gyumolcsnev_listbox.get()   
      gy = gyumolcsokListaz()
      gyumleID = ""
      for i in gy:
         if i.nev == gyumneve:
            gyumleID = i.id
      print(gyumleID)
      query =  f"INSERT INTO kiszallitasok (sorszam,gyumleid,partnerid,datum,karton) VALUES('', {gyumleID}, {partnerID}, '{datum}', {karton} ) "       
      cursor.execute(query)
      conn.commit() # db frissítés!!!!!
      messagebox.showinfo("Figyelmeztetés", "Sikeres beszúrás")
      
   except:
      messagebox.showerror("Figyelmeztetés", "Hiba a beszúrás során!")   

   for item in trv.get_children():
        trv.delete(item)
   for i in kiszallitasok_listaz():
      trv.insert("", END, values=(i.datum, i.kontakt, i.karton, i.gynev))

   cursor.close()
   conn.close()
           
        

ablak = Tk()
ablak.title("Admin felület")
ablak.geometry("750x400")

# Notebook és panelek létrehozása
tab = ttk.Notebook(ablak)
panel1 = ttk.Frame(tab)
panel2 = ttk.Frame(tab)

icon1 = PhotoImage(file="icon1.png")
icon2 = PhotoImage(file="icon2.png")

tab.add(panel1, text="Kiszállítások listázása", image=icon1, compound="left")
tab.add(panel2, text=" Partnerek felvitele", image=icon1, compound="left")
#tab.add(panel2, text="Dolgozók listázása", image=icon2, compound="left")
tab.pack(expand=1, fill='both')

# Panel1 (Adatok felvitele)
# Grid konfiguráció a panel1-ben
panel1.columnconfigure(0, weight=0)  
panel1.columnconfigure(1, weight=0)  
panel1.columnconfigure(2, weight=0)  

panel1.rowconfigure(0, weight=0)  # Név
panel1.rowconfigure(1, weight=0)  # Beosztás
panel1.rowconfigure(2, weight=0)  # További sorok

panel2.columnconfigure(0, weight=0)  
panel2.columnconfigure(1, weight=0)  
panel2.columnconfigure(2, weight=0)  

panel2.rowconfigure(0, weight=0)  # Név
panel2.rowconfigure(1, weight=0)  # Beosztás
panel2.rowconfigure(2, weight=0)  # További sorok

# Partnerek felvitele címke
felvitel_cimkepartnerek = Label(panel1, text="Partnerek felvitele", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
felvitel_cimkepartnerek.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(5, 10))

azlabel = Label(panel2, text="Azonosító:", font=("Arial", 10))
azlabel.grid(row=1, column=0, padx=10, pady=10, sticky="e")
az_entry = Entry(panel2, width=20, font=("Arial", 10))
az_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

nevlabel = Label(panel2, text="Név:", font=("Arial", 10))
nevlabel.grid(row=2, column=0, padx=10, pady=10, sticky="e")
nev_entry = Entry(panel2, width=20, font=("Arial", 10) )
nev_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

telepuleslabel = Label(panel2, text="Település:", font=("Arial", 10))
telepuleslabel.grid(row=3, column=0, padx=10, pady=10, sticky="e")
telepules_entry = Entry (panel2, width=20, font=("Arial", 10) )
telepules_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")


gombpartnerek = ctk.CTkButton(panel2, text="Új parrtner mentése ", command=ujpartnerfelvitel)
gombpartnerek.grid(row=5, column=0, columnspan=2, pady=20)
# Kiszállítások felvitele címke
felvitel_cimke = Label(panel1, text="Kiszállítások felvitele", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
felvitel_cimke.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(5, 10))

datumlabel = Label(panel1, text="Datum:", font=("Arial", 10))
datumlabel.grid(row=1, column=0, padx=10, pady=10, sticky="e")
datum_entry = Entry(panel1, width=20, font=("Arial", 10))
datum_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

nevlabel = Label(panel1, text="Név:", font=("Arial", 10))
nevlabel.grid(row=2, column=0, padx=10, pady=10, sticky="e")
nev_listbox = ttk.Combobox(panel1, width=20, state="readonly" )
nev_listbox.grid(row=2, column=1, padx=10, pady=10, sticky="w")


katronSzlabel = Label(panel1, text="Kartonszám:")
katronSzlabel.grid(row=3, column=0, padx=10, pady=10, sticky="e")
katronSz_entry = Entry(panel1, width=23)
katronSz_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

gyumolcsnevlabel = Label(panel1, text="Gyümölcsnév:")
gyumolcsnevlabel.grid(row=4, column=0, padx=10, pady=10, sticky="e")
gyumolcsnev_listbox = ttk.Combobox(panel1, width=20, state="readonly")
gyumolcsnev_listbox.grid(row=4, column=1, padx=10, pady=10, sticky="w")

gomb = ctk.CTkButton(panel1, text="Adatok mentése", command=KiszallitasBeszur)
gomb.grid(row=5, column=0, columnspan=2, pady=20)

# Elválasztó vonal
separator = ttk.Separator(panel1, orient="vertical")
separator.grid(row=0, column=2,rowspan=6, sticky="ns", padx=10, pady=10)

lista_cimke = Label(panel1, text="Kiszállítások listája", bg="#2196F3", fg="white", font=("Arial", 12, "bold"), width=40)
lista_cimke.grid(row=0, column=3, columnspan=8, sticky="ew", padx=10, pady=(5, 10))

#eredmeny = Listbox(panel1, font="Arial 10", width=55, height=13)
#eredmeny.grid(row=1, column=3, padx=20, pady=20, rowspan=5, columnspan=8)

trv = ttk.Treeview(panel1, selectmode="browse")
trv.grid(row=1, column=3, padx=20, pady=20, rowspan=5, columnspan=8)

# number of columns
trv["columns"] = ("1", "2", "3", "4")

# Defining heading
trv['show'] = 'headings'

# width of columns and alignment
trv.column("1", width=120, anchor='c')
trv.column("2", width=100, anchor='c')
trv.column("3", width=100, anchor='c')
trv.column("4", width=100, anchor='c')


# Headings
# respective columns
trv.heading("1", text="Dátum")
trv.heading("2", text="Partner név")
trv.heading("3", text="Kartonszám")
trv.heading("4", text="Gyümölcs név")



menu = Menu(ablak, tearoff=0)
menu.add_command(label="Módosítás")
menu.add_command(label="Törlés")


def jobb_klikk(event):
    sor_id = trv.identify_row(event.y)
    if sor_id:  # Ha talált sort
        trv.selection_set(sor_id)  # Kijelöljük a sort
        trv.focus(sor_id)  # Fókuszba helyezzük
        # A kiválasztott sor adatai
        values = trv.item(sor_id, "values")
        print(f"Jobb klikk: {values}")
        # Ide jöhet egy helyi menü megjelenítése is (lásd alább).
    # A kurzor helyén levő sor meghatározása
    iid = trv.identify_row(event.y)
    if iid:  # Ha van sor az adott helyen
        trv.selection_set(iid)  # Kiválasztja a sort
        menu.post(event.x_root, event.y_root)  # Kontextusmenü megjelenítése

trv.bind("<Button-3>", jobb_klikk)  # Jobb klikk

# adatok kiíratása
print(kiszallitasok_listaz())


for item in trv.get_children():
        trv.delete(item)
for i in kiszallitasok_listaz():
   trv.insert("", END, values=(i.datum, i.kontakt, i.karton, i.gynev))

p = partnerekListaz()   

pNevek = []
for i in p:
    pNevek.append(i.neve)
print(pNevek)
nev_listbox['values'] = pNevek

gy = gyumolcsokListaz()
gyNevek = []
for i in gy:
    gyNevek.append(i.nev)

gyumolcsnev_listbox['values'] = gyNevek    


ablak.mainloop()

