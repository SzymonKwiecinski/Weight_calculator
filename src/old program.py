import pandas as pd
import tkinter
import os

file = 'Przelicznik.xlsx'
xl = pd.ExcelFile(file)
sheet_name = xl.sheet_names
Sheet_DIN = xl.parse()

din = str()
srednica = str()
dlugosc = str()
napis = str()
waga_1000szt = float()

def Prze_kg_na_100szt(value):
    new_value = format(value/10,'.3f')
    return new_value

def Prze_100szt_na_kg(value):
    new_value = format(10/value,'.3f')
    return new_value

def select_din():
    global Sheet_DIN
    global sheet_name_now
    listbox_srednica.delete(0,'end')
    listbox_dlugosc.delete(0, 'end')
    index = listbox_norma.curselection()[0]
    my_sheet = listbox_norma.get(index)
    sheet_name_now = my_sheet
    if my_sheet == 'Nakretki_Podkladki':
        buton_select_srednica.configure(text='Wybierz norme')
        buton_select_dlugosc.configure(text='Wybierz Średnice')
    if my_sheet != 'Nakretki_Podkladki':
        buton_select_srednica.configure(text='Wybierz Średnice')
        buton_select_dlugosc.configure(text='Wybierz Długość')
    Sheet_DIN = xl.parse(my_sheet,index_col=0)
    for x in Sheet_DIN.columns.values:
        listbox_srednica.insert('end',x)
    global din
    din = str(my_sheet)
    label_dane.configure(text=din)



def select_srednice():
    listbox_dlugosc.delete(0,'end')
    index = listbox_srednica.curselection()[0]
    my_sheet = listbox_srednica.get(index)
    for x in Sheet_DIN.index.values:
        if Sheet_DIN.loc[x,str(my_sheet)] != 'None':
            listbox_dlugosc.insert('end', x)
    global srednica
    srednica = str(my_sheet)
    if sheet_name_now == 'Nakretki_Podkladki':
        label_dane.configure(text=srednica)
    if sheet_name_now != 'Nakretki_Podkladki':
        label_dane.configure(text=(din + ' ' + srednica))

def select_dlugosc():
    index = listbox_dlugosc.curselection()[0]
    my_sheet = listbox_dlugosc.get(index)
    global dlugosc
    global waga_1000szt
    dlugosc = str(my_sheet)
    if sheet_name_now == 'Nakretki_Podkladki':
        label_dane.configure(text=(srednica + '  ' + str(dlugosc)))
        var = Sheet_DIN.loc[dlugosc, srednica]
        label_dane_z_tab_wyp.configure(text=' '+str(var)+' kg.'+'\n '+str(Prze_100szt_na_kg(var)+'\n '+str(Prze_kg_na_100szt(var))) )
        waga_1000szt = float(var)
    if sheet_name_now != 'Nakretki_Podkladki':
        label_dane.configure(text=(din + ' ' + srednica + 'x' + str(dlugosc)))
        var = Sheet_DIN.loc[float(dlugosc),srednica]
        label_dane_z_tab_wyp.configure(text=' '+str(var)+' kg.'+'\n '+str(Prze_100szt_na_kg(var)+'\n '+str(Prze_kg_na_100szt(var))) )
        waga_1000szt = float(var)

def oblicz_ile_to_kg():
    if entry_oblicz.get() != '':
        new_sztuki = int(entry_oblicz.get().replace(',','.'))
        kilogramy = (new_sztuki * waga_1000szt) / 1000.0
        label_wynik_obliczen.config(text=str(new_sztuki) + ' szt  =  '+ format(kilogramy,'.2f')+' kg')

def oblicz_ile_to_sztuk():
    if entry_oblicz.get() != '':
        new_kg = float(entry_oblicz.get().replace(',','.'))
        sztuki = (new_kg / waga_1000szt) * 1000
        label_wynik_obliczen.config(text=format(new_kg,'.2f') + ' kg  =  '+ format(sztuki,'.0f')+' szt')

def konwersja_cena_100szt_na_kg():
    cena = float(entry_oblicz_cene.get().replace(',','.'))
    cena_za_1kg = cena / (waga_1000szt / 10)
    label_wynik_obliczen_cena.config(text=format(cena,'.2f') +'zł/100szt = '+ format(cena_za_1kg,'.2f') + 'zł/kg')

def konwersja_cena_kg_na_100szt():
    cena = float(entry_oblicz_cene.get().replace(',','.')) 
    przelicznik = 1000 / waga_1000szt
    cena_100szt = (cena / przelicznik) * 100 
    label_wynik_obliczen_cena.config(text=format(cena,'.2f') +'zł/kg = '+ format(cena_100szt,'.2f') + 'zł/100szt')

def open_exel():
    os.startfile('Przelicznik.xlsx')

def open_pdf_file_program():
    os.startfile('Instrukcja_do_programu.pdf')

def open_pdf_file_exel():
    os.startfile('Instrukcja_do_wstawiania_danych_do_exel.pdf')

def open_pdf_file_subiekt():
    os.startfile('Instrukcja_do_subiekta_gt.pdf')

top = tkinter.Tk()
top.title('Program do konwersji wagowo sztukowej - AREX')

listbox_norma = tkinter.Listbox(top,selectmode = 'SINGLE',yscrollcommand=1,height = 16,width =30)
listbox_norma.grid(row=0,column=2,rowspan=4,padx=1,pady=3)
for x,y in enumerate(sheet_name):
    listbox_norma.insert(x+1,y)

scrollbar_dlugosc = tkinter.Scrollbar(top)
scrollbar_dlugosc.grid(row=0,column=7,rowspan=4, sticky='ns')

listbox_dlugosc = tkinter.Listbox(top, yscrollcommand =scrollbar_dlugosc.set,selectmode= 'SINGLE',height = 16)
listbox_dlugosc.grid(row=0,column=6,rowspan=4,pady=3)

scrollbar_dlugosc.config(command = listbox_dlugosc.yview)

scrollbar_srednica = tkinter.Scrollbar(top)
scrollbar_srednica.grid(row=0,column=4,rowspan=4, sticky='ns')

listbox_srednica = tkinter.Listbox(top, yscrollcommand =scrollbar_srednica.set, selectmode= 'SINGLE',height = 16)
listbox_srednica.grid(row=0,column=3,rowspan=4,pady=3)

scrollbar_srednica.config(command = listbox_srednica.yview)

buton_select_din = tkinter.Button(top, text='Wybierz Normę', command=select_din)
buton_select_din.grid(row=4,column=2)

buton_select_srednica = tkinter.Button(top, text='Wybierz Średnice', command=select_srednice)
buton_select_srednica.grid(row=4,column=3)

buton_select_dlugosc = tkinter.Button(top, text='Wybierz Dlugość', command=select_dlugosc)
buton_select_dlugosc.grid(row=4,column=6)

label_dane = tkinter.Label(top)
label_dane.grid(column=8,row=0,columnspan=2)
label_dane.config(font ="Verdena 20 bold",fg='blue')


label_dane_z_tab = tkinter.Label(top)
label_dane_z_tab.grid(column=8,row=1)
label_dane_z_tab.configure(font=15,text='            1000 sztuk waży :\nPrzelicznik 100szt. na kg. :\nPrzelicznik kg. na 100szt. :')

label_dane_z_tab_wyp = tkinter.Label(top)
label_dane_z_tab_wyp.grid(column=9,row=1)
label_dane_z_tab_wyp.config(font=15,fg='blue')

label_oblicz_sam = tkinter.Label(top)
label_oblicz_sam.grid(column=8,row=2,columnspan=2)
label_oblicz_sam.configure(font=15,text='\nWpisz sztuki lub kilogramy aby\n przeliczyć na inną jednostkę')

entry_oblicz = tkinter.Entry(top)
entry_oblicz.grid(row=3,column=8,columnspan=2)

buton_oblicz_kg = tkinter.Button(top,text='Oblicz ile\nto kilogramów',command=oblicz_ile_to_kg)
buton_oblicz_kg.grid(row=4,column=8,padx=3,pady=3)

buton_oblicz_szt = tkinter.Button(top,text="Oblicz ile\nto sztuk",command=oblicz_ile_to_sztuk)
buton_oblicz_szt.grid(row=4,column=9,padx=3,pady=3)

label_wynik_obliczen = tkinter.Label(top)
label_wynik_obliczen.grid(row=5, column=8,columnspan=2)
label_wynik_obliczen.config(font=10,fg='blue')

label_oblicz_cene_tekst = tkinter.Label(top)
label_oblicz_cene_tekst.grid(row=6,column=8,columnspan=2)
label_oblicz_cene_tekst.config(font=15,text='Wpisz cene za 100szt lub za kg')

entry_oblicz_cene = tkinter.Entry(top)
entry_oblicz_cene.grid(row=7,column=8,columnspan=2)

buton_oblicz_kg = tkinter.Button(top,text='Konwersja ceny z\nzł/100szt -> zł/kg',command=konwersja_cena_100szt_na_kg)
buton_oblicz_kg.grid(row=8,column=8,padx=3,pady=3)

buton_oblicz_szt = tkinter.Button(top,text="Konwersja ceny z\nzł/kg -> zł/100szt",command=konwersja_cena_kg_na_100szt)
buton_oblicz_szt.grid(row=8,column=9,padx=3,pady=3)

label_wynik_obliczen_cena = tkinter.Label(top)
label_wynik_obliczen_cena.grid(row=9, column=8,columnspan=2)
label_wynik_obliczen_cena.config(font=10,fg='blue')

buton_instrukcja = tkinter.Button(top,text='EXEL Z DANYMI',font="Verdena 12 bold",fg='black',bg='green',command=open_exel)
buton_instrukcja.grid(row=6,column=2,columnspan=6,padx=3,pady=3)

buton_instrukcja = tkinter.Button(top,text='INSTRUKCJA PROGRAMU',font="Verdena 12 bold",fg='black',bg='red',command=open_pdf_file_program)
buton_instrukcja.grid(row=7,column=2,columnspan=6)

buton_instrukcja_do_exela = tkinter.Button(top,text='INSTRUKCJA DODAWANIA KOLEJNYCH ROZMIARÓW',font="Verdena 12 bold",fg='black',bg='red',command=open_pdf_file_exel)
buton_instrukcja_do_exela.grid(row=8,column=2,columnspan=6)

buton_instrukcja_do_subiekta = tkinter.Button(top,text='INSTRUKCJA DODAWANIA PRZELICZNIKÓW DO SUBIEKTA',font="Verdena 12 bold",fg='black',bg='red',command=open_pdf_file_subiekt)
buton_instrukcja_do_subiekta.grid(row=9,column=2,columnspan=6)





top.mainloop()
