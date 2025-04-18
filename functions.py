from models import Partner, Gyumolcsok, Kisszallitasok
from db import db_connect
from tkinter import END, messagebox

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

def ujpartnerfelvitel(nev_entry, telepules_entry):
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
      
def KiszallitasBeszur(datum_entry,nev_listbox,katronSz_entry, gyumolcsnev_listbox, trv):
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