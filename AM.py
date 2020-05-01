from tkinter import *
from tkinter import messagebox  
from bd import *

coord = []
valori = []
valori_initiale_entry = []
valori_curente_entry = []
id_proiecte = 0
nr_proiecte = 0
importanta_valori = []
val_imp_entry = []
valori_adaugate = [[],[],[],[]]
canv_list = []
cb_list = [] #checkboxlist

def label_fact():
	roww = 80
	mycursor.execute("SELECT * FROM `tip_factori`")
	myresult1 = mycursor.fetchall()
	mycursor.execute("SELECT nume_factor, id_tip_factor FROM `factori`")
	myresult2 = mycursor.fetchall()
	for i in range(len(myresult1)):
		label_tip_f = Label(canv, text=myresult1[i][1], font="Time 12", 
									 relief=SOLID, bg="lightgreen")
		label_tip_f.place(x=50, y=roww+11)
		line = canv.create_line(0,roww+11,1280,roww+11,width=3)
		roww += 25
		for j in range(len(myresult2)):
			if myresult1[i][0] == myresult2[j][1]:
				label_f = Label(canv, text=myresult2[j][0], font="Time 10", width=25,
									justify=LEFT, anchor=W, relief=SOLID)
				label_f.place(x=0, y=roww+10)
				coord.append([0, roww+10])
				canv.create_line(0,roww+10,1280,roww+10,width=1)
				roww += 20
	canv.create_line(0,roww+11,1280,roww+11,width=3)
	canv.create_line(206,0,206,631,width=3)
	 
def adaugare_proiect(index):
	xdef = 210
	ydef = 47
	button = Button(canv, width=15, height=2, text="Proiectul "+str(index+1), command= lambda: afisare_proiect(index))
	button.place(x=xdef+(index*120), y=ydef)
	label_param = Label(canv, width=13, text="initiali | curenti")
	label_param.place(x=xdef+10+(index*120), y=ydef+46)	
	mycursor.execute("SELECT valoare FROM criterii WHERE id_proiect = {} and id_parametru=1".format(id_proiecte[index][0]))
	result1 = mycursor.fetchall()
	valori.append([])
	valori_initiale_entry.append([])
	if result1 == None:
		exit(1)
	else:
		for i in range(22):
			entry_i = Entry(canv, width=7)
			entry_i.insert(0,result1[i][0])
			valori[index].append([result1[i][0]])
			entry_i.place(x=coord[i][0]+xdef+13+(index*120), y=coord[i][1])
			valori_initiale_entry[index].append(entry_i)

	mycursor.execute("SELECT valoare FROM criterii WHERE id_proiect = {} and id_parametru=2".format(id_proiecte[index][0]))
	result2 = mycursor.fetchall()
	if result2 == None:
		exit(1)
	else:
		valori_curente_entry.append([])
		for i in range(22):
			entry_c = Entry(canv, width=6)
			entry_c.insert(0,result2[i][0])
			valori[index][i].append(result2[i][0])
			entry_c.place(x=coord[i][0]+xdef+56+(index*120), y=coord[i][1])
			valori_curente_entry[index].append(entry_c)

		button_modify = Button(canv, width=10, height=1, text="Modifica", command= lambda: save_modify(index+1))
		button_modify.place(x=xdef+14+(index*120), y=ydef+588)

		canv.button_plus = Button(canv, width=6, height=2, text="+", command= lambda: new_project(index))
		canv.button_plus.place(x=210+(len(nr_proiecte)*120), y=47)	

def afisare_proiect(index):
	top = Toplevel(takefocus=True)
	top.grab_set()
	top.geometry("400x310+400+100")
	top.title("Despre proiect...")
	mycursor.execute("SELECT nume_proiect FROM proiect;")
	ressult1 = mycursor.fetchall()
	Label(top, text = ressult1[index][0], font="Time 18", borderwidth=2, relief="solid", pady=8).grid(row=0, column=1)
	mycursor.execute("SELECT nume_oras FROM locatie;")
	ressult2 = mycursor.fetchall()
	Label(top, text = "Oras: ", font="Time 12").grid(row=1, column=0)
	Label(top, text = ressult2[index][0], font="Time 12").grid(row=1,column=1)
	mycursor.execute("SELECT sector FROM locatie;")
	ressult3 = mycursor.fetchall()
	Label(top, text = "Sector: ", font="Time 12").grid(row=2, column=0)
	Label(top, text = ressult3[index][0], font="Time 12").grid(row=2,column=1)
	mycursor.execute("SELECT strada FROM locatie;")
	ressult4 = mycursor.fetchall()
	Label(top, text = "Strada: ", font="Time 12").grid(row=3, column=0)
	Label(top, text = ressult4[index][0], font="Time 12").grid(row=3,column=1)
	mycursor.execute("SELECT coordonate FROM locatie;")
	ressult5 = mycursor.fetchall()
	Label(top, text = "Coordonate: ", font="Time 12").grid(row=4, column=0)
	Label(top, text = ressult5[index][0], font="Time 12").grid(row=4,column=1)
	mycursor.execute("SELECT tip_edificiu FROM tipul_de_edificiu NATURAL JOIN proiect;")
	ressult6 = mycursor.fetchall()
	Label(top, text = "Tipul edificiului: ", font="Time 12").grid(row=5, column=0)
	Label(top, text = ressult6[index][0], font="Time 12").grid(row=5,column=1)
	mycursor.execute("SELECT comentariul FROM comentariu;")
	ressult7 = mycursor.fetchall()
	Label(top, text = "Comentariu: ", font="Time 12").grid(row=6, column=0)
	text = Text(top, width=25, height=5, font="Time 12")
	text.insert(1.0, ressult7[index][0])
	text.grid(row=6, column=1, columnspan=2)
	button1 = Button(top, text="Stergere", command= lambda: stergerea_proiectului(), font="Time 12", pady=2, padx=5)
	button1.grid(row=7, column=0)
	button2 = Button(top, text="Inchide", command=top.destroy, font="Time 16", pady=4, padx=5)
	button2.grid(row=7, column=1)

	def stergerea_proiectului():
		mycursor.execute("SELECT id_comentariu FROM `proiect` natural join comentariu where id_proiect = {};".format(id_proiecte[index][0]))
		rez1 = mycursor.fetchall()
		mycursor.execute("SELECT id_locatie FROM `proiect` natural join locatie where id_proiect = {};".format(id_proiecte[index][0]))
		rez2 = mycursor.fetchall()
		mycursor.execute("DELETE FROM criterii where id_proiect = {};".format(id_proiecte[index][0]))
		mydb.commit()
		mycursor.execute("DELETE FROM proiect where id_proiect = {};".format(id_proiecte[index][0]))
		mydb.commit()
		mycursor.execute("DELETE FROM comentariu where id_comentariu = {};".format(rez1[0][0]))
		mydb.commit()
		mycursor.execute("DELETE FROM locatie where id_locatie = {};".format(rez2[0][0]))
		mydb.commit()
		messagebox.showinfo(title="Atentie", message="Proiect Sters!")
		top.destroy()

def save_modify(index):
	y = 0
	for i in range(1, 23):
		a = float(valori[index-1][i-1][0])
		b = float(valori_initiale_entry[index-1][i-1].get())
		if a != b:
			mycursor.execute("UPDATE criterii SET valoare = {0} WHERE id_proiect = {1} and id_parametru = {2} and id_factor = {3};".format(b, id_proiecte[index-1][0], 1, i))
			mydb.commit()
			y += mycursor.rowcount
		c = float(valori[index-1][i-1][1])
		d = float(valori_curente_entry[index-1][i-1].get())
		if c != d:
			mycursor.execute("UPDATE criterii SET valoare = {0} WHERE id_proiect = {1} and id_parametru = {2} and id_factor = {3};".format(d, id_proiecte[index-1][0], 2, i))
			mydb.commit()
			y += mycursor.rowcount
	print(y, "record(s) affected")

def adaugare_importanta():
	canv.create_line(1140,0,1140,630,width=3)
	mycursor.execute("SELECT valoare_importanta FROM importanta;")
	result_imp = mycursor.fetchall()
	if result_imp == None:
		exit(1)
	else:
		for i in range(0,len(result_imp)):
			entry_imp = Entry(canv, width=12)
			entry_imp.insert(0,result_imp[i][0])
			importanta_valori.append([result_imp[i][0]])
			entry_imp.place(x=coord[i][0]+223+950, y=coord[i][1])
			val_imp_entry.append(entry_imp)

	button_modify_imp = Button(canv, width=15, height=1, text="Modifica", command= lambda: save_modify_importanta())
	button_modify_imp.place(x=1150, y=635)

def save_modify_importanta():
	y = 0
	for i in range(1, 23):
		a = float(importanta_valori[i-1][0])
		b = float(val_imp_entry[i-1].get())
		if a != b:
			mycursor.execute("UPDATE importanta SET valoare_importanta = {0} WHERE id_importanta = {1};".format(b, i))
			mydb.commit()
			y += mycursor.rowcount
	print(y, "record(s) affected")

def new_project(nr_proiecte):
	top = Toplevel(takefocus=True)
	top.grab_set()
	top.geometry("350x330+400+100")
	top.title("Adaugarea unui proiect")
	Label(top, text = "Denumirea proiectului: ", font="Time 12").grid(row=0, column=0)
	name_entry = Entry(top, width=20)
	name_entry.grid(row=0, column=1)
	Label(top, text = "Orasul: ", font="Time 12").grid(row=1, column=0)
	city_entry = Entry(top, width=20)
	city_entry.grid(row=1, column=1)
	Label(top, text = "Sectorul: ", font="Time 12").grid(row=2, column=0)
	sector_entry = Entry(top, width=20)
	sector_entry.grid(row=2, column=1)
	Label(top, text = "Strada: ", font="Time 12").grid(row=3, column=0)
	street_entry = Entry(top, width=20)
	street_entry.grid(row=3, column=1)
	Label(top, text = "Coordonate: ", font="Time 12").grid(row=4, column=0)
	coord_entry = Entry(top, width=20)
	coord_entry.grid(row=4, column=1)
	Label(top, text = "Comentariu: ", font="Time 12").grid(row=5, column=0)
	comment_text = Text(top, width=20, height=2, font="Time 10", wrap=WORD)
	comment_text.grid(row=5, column=1)

	Label(top, text = "Tipul edificiului: ", font="Time 12").grid(row=6, column=0)
	btn = Button(top, text = "  select  ", command= lambda: select_edificiu())
	btn.grid(row=6, column=1)

	mycursor.execute("SELECT nume_tip_factor, id_tip_factor FROM `tip_factori`")
	tip_factori_new = mycursor.fetchall()

	for i in range(len(tip_factori_new)):
		afisare_tip_factori(top, tip_factori_new, i)

	btn_create = Button(top, text = "Creeaza", padx=5, pady=2, font="Time 14", command= lambda: adauga_in_bd())
	btn_create.grid(row=100, column=0)
		
	def adauga_in_bd():
		dps = []#date pentru salvare
		dps.append(name_entry.get())
		dps.append(city_entry.get())
		dps.append(sector_entry.get())
		dps.append(street_entry.get())
		dps.append(coord_entry.get())
		dps.append(comment_text.get(1.0, END))
		dps.append(top.var.get())
		mycursor.execute("INSERT INTO locatie (nume_oras, sector, strada, coordonate) VALUES ('{}','{}','{}','{}');".format(dps[1], dps[2], dps[3], dps[4]))
		mydb.commit()
		mycursor.execute("INSERT INTO comentariu (comentariul) VALUES ('{}');".format(dps[5]))
		mydb.commit()

		mycursor.execute("SELECT id_locatie FROM `locatie`;")
		ress1 = mycursor.fetchall()
		mycursor.execute("SELECT id_comentariu FROM `comentariu`;")
		ress2 = mycursor.fetchall()
		
		mycursor.execute("INSERT INTO proiect (nume_proiect, id_edificiu, id_locatie, id_comentariu) VALUES ('{}',{},{},{});".format(dps[0], int(dps[6]), ress1[-1][0], ress2[-1][0]))
		mydb.commit()

		j = 1
		mycursor.execute("SELECT * FROM `proiect`;")
		ress3 = mycursor.fetchall()
		for i in range(4):
			for ii in range(len(valori_adaugate[i])):
				mycursor.execute("INSERT INTO criterii (id_factor, id_parametru, id_proiect, valoare, id_importanta) VALUES ({},{},{},{},{});".format(j, 1, ress3[-1][0], valori_adaugate[i][ii][0], j))
				mycursor.execute("INSERT INTO criterii (id_factor, id_parametru, id_proiect, valoare, id_importanta) VALUES ({},{},{},{},{});".format(j, 2, ress3[-1][0], valori_adaugate[i][ii][1], j))
				j-=-1
		mydb.commit()
		messagebox.showinfo(title="Atentie", message="Created")
		# adaugare_proiect(nr_proiecte+1)
		top.destroy()


	def select_edificiu():
		top3 = Toplevel(takefocus=True)
		top3.grab_set()
		top3.geometry("250x150+500+200")
		top3.title("Tipul edificiului")
		top.var = IntVar()
		mycursor.execute("SELECT * FROM `tipul_de_edificiu`;")
		res = mycursor.fetchall()
		for i in range(len(res)):
			r = Radiobutton(top3, text=res[i][1], variable=top.var, value=res[i][0])
			r.pack()
		btn = Button(top3, text = "Ok", command= top3.destroy)
		btn.pack()

			

def afisare_tip_factori(top, tip_factori_new, i):
	Label(top, text = "{} ".format(tip_factori_new[i][0]), font="Time 12", fg="blue").grid(row=7+i, column=0)
	btn = Button(top, text = "+ valori", command= lambda: adaugare_valori(i, tip_factori_new[i][0]))
	btn.grid(row=7+i, column=1)

def adaugare_valori(i, name):
	top2 = Toplevel(takefocus=True)
	top2.grab_set()
	top2.geometry("500x300+500+200")
	top2.title("{}".format(name))
	Label(top2, text = "initiali ", font="Time 12").grid(row=0, column=1)
	Label(top2, text = "curenti ", font="Time 12").grid(row=0, column=2)

	mycursor.execute("SELECT nume_factor, id_tip_factor FROM `factori`")
	factori_new = mycursor.fetchall()
	initial_entry_list = []
	curent_entry_list = []
	for j in range(len(factori_new)):
				if factori_new[j][1] == i+1:
					Label(top2, text = "{} ".format(factori_new[j][0]), font="Time 12").grid(row=j+1, column=0)
					initial_entry = Entry(top2)			
					initial_entry_list.append(initial_entry)
					initial_entry.grid(row=j+1, column=1)
					curent_entry = Entry(top2)
					curent_entry_list.append(curent_entry)
					curent_entry.grid(row=j+1, column=2)
	save_btn = Button(top2, text = " Salveaza ", command= lambda: salveaza_valori())
	save_btn.grid(row=100, column=1)

	def salveaza_valori():
		l = 0
		for j in range(len(initial_entry_list)):
			a = initial_entry_list[j].get()
			b = curent_entry_list[j].get()
			if a == "" or b == "":
				l += 1
			valori_adaugate[i].append([a, b])
		if l > 0 :
			messagebox.showwarning(title="Atentie", message="Completati toate campurile!")
		else:
			top2.destroy()
	

def calc_execute():
	summ = []
	ydef = 680
	for i in canv_list:
		try:
			i.destroy()
		except:
			pass
	for i in range(len(nr_proiecte)):
		s1 = 0
		s2 = 0
		for j in range(len(importanta_valori)):
			#print(valori[i][j][0],' | ',valori[i][j][1],' | ',importanta_valori[j][0])
			s1 += valori[i][j][0] * (importanta_valori[j][0] / 100)
			s2 += valori[i][j][1] * (importanta_valori[j][0] / 100)
		summ.append([s1 / 22, s2 / 22])
	
	for i in range(len(nr_proiecte)):
		canv.label_i = Label(canv, text='P ({}/initial)'.format(i+1), font="Time 12", width=9,
									justify=LEFT, anchor=W, relief=SOLID)
		canv.label_i.place(x=5 + i*170, y=ydef)
		canv_list.append(canv.label_i)

		canv.label_inf = Label(canv, text='= %2.4f' % (summ[i][0]), font='Time 12')
		canv.label_inf.place(x=95+i*170, y=ydef)	
		canv_list.append(canv.label_inf)

		canv.label_c = Label(canv, text='P ({}/curent)'.format(i+1), font="Time 12", width=9,
									justify=LEFT, anchor=W, relief=SOLID)
		canv.label_c.place(x=5 + i*170, y=ydef+40)
		canv_list.append(canv.label_c)

		canv.label_inf = Label(canv, text='= %2.4f' % (summ[i][1]), font='Time 12')
		canv.label_inf.place(x=95+i*170, y=ydef+40)	
		canv_list.append(canv.label_inf)


	b = (summ[0][0] + summ[0][1]) / 2
	b1 = 0

	for i, j in enumerate(summ):
		if (summ[i][0] + summ[i][1]) / 2 > b:
			b1 = i
			b = (summ[i][0] + summ[i][1]) / 2

	canv.top_label = Label(canv, text='Cel mai de valoare proiect : P{} cu valoarea medie = {}'.format(b1+1, b), font='Time 12', relief=SOLID)
	canv.top_label.place(x=20, y=ydef+75)	
	canv_list.append(canv.top_label)


def calc_interogare():
	for i in canv_list:
		try:
			i.destroy()
		except:
			pass

	cb_list = []
	top4 = Toplevel(takefocus=True)
	top4.grab_set()
	top4.geometry("280x790+900+5")
	top4.title("Modul Query")
	Label(top4, text="Selectati factorii pentru interogare", font="Time 12", pady=5).grid(row=0, column=0)
	mycursor.execute("SELECT * FROM `tip_factori`")
	myresult1 = mycursor.fetchall()
	mycursor.execute("SELECT nume_factor, id_tip_factor FROM `factori`")
	myresult2 = mycursor.fetchall()
	a = 1
	for i in range(len(myresult1)):
		label_tip_f = Label(top4, text=myresult1[i][1], font="Time 14", 
									 relief=SOLID, bg="lightblue")
		label_tip_f.grid(row=a, column=0)
		a-=-1
		for j in range(len(myresult2)):
			if myresult1[i][0] == myresult2[j][1]:
				label_f = Label(top4, text=myresult2[j][0], font="Time 12", width=25,
									justify=LEFT, anchor=W, relief=SOLID)
				label_f.grid(row=a,column=0)
				var = IntVar()
				Checkbutton(top4, text="", variable=var).grid(row=a, column=1)
				cb_list.append(var)
				a-=-1
	exec_btn = Button(top4, text='Calculeaza', width=14, height=2, font='Time 14', command= lambda: calc_query_execute())
	exec_btn.grid(row=a, column=0)

	def calc_query_execute():
		ydef = 680
		index_list = []
		summ = []
		for index, i in enumerate(cb_list):
			if i.get() == 1:
				index_list.append(index)
		for j in range(len(nr_proiecte)):
			s1 = 0
			s2 = 0
			for i in index_list:
				s1 += valori[j][i][0] * (importanta_valori[i][0] / 100)
				s2 += valori[j][i][1] * (importanta_valori[i][0] / 100)
			summ.append([s1 / len(index_list), s2 / len(index_list)])
		for i in range(len(nr_proiecte)):
			canv.label_i = Label(canv, text='P ({}/initial)'.format(i+1), font="Time 12", width=9,
										justify=LEFT, anchor=W, relief=SOLID)
			canv.label_i.place(x=5 + i*170, y=ydef)
			canv_list.append(canv.label_i)

			canv.label_inf = Label(canv, text='= %2.4f' % (summ[i][0]), font='Time 12')
			canv.label_inf.place(x=95+i*170, y=ydef)	
			canv_list.append(canv.label_inf)

			canv.label_c = Label(canv, text='P ({}/curent)'.format(i+1), font="Time 12", width=9,
										justify=LEFT, anchor=W, relief=SOLID)
			canv.label_c.place(x=5 + i*170, y=ydef+40)
			canv_list.append(canv.label_c)

			canv.label_inf = Label(canv, text='= %2.4f' % (summ[i][1]), font='Time 12')
			canv.label_inf.place(x=95+i*170, y=ydef+40)	
			canv_list.append(canv.label_inf)
		b = (summ[0][0] + summ[0][1]) / 2
		b1 = 0

		for i, j in enumerate(summ):
			if (summ[i][0] + summ[i][1]) / 2 > b:
				b1 = i
				b = (summ[i][0] + summ[i][1]) / 2

		canv.top_label = Label(canv, text='Cel mai de valoare proiect : P{} cu valoarea medie = {}'.format(b1+1, b), font='Time 12', relief=SOLID)
		canv.top_label.place(x=20, y=ydef+75)	
		canv_list.append(canv.top_label)
		top4.destroy()

if __name__ == "__main__":
	root = Tk()
	root.geometry("1280x800+100+5")
	root.minsize(width=1280, height=800)
	root.maxsize(width=1280, height=800)
	root.title('Analiza Multicriteriala a Ciclului de Viata a Unei Cladiri')
	canv = Canvas(root,width=1280, height=800)
	canv.pack()
	###############
	#	Factori   #
	###############
	label_factori = Label(canv, text="Factorii", font="Time 20", fg="red")
	label_factori.place(x=10, y=50)
	label_fact()
	###############
	#	Proiecte  #
	###############
	label_proiecte = Label(canv, text="Proiecte", font="Time 20", fg="blue")
	label_proiecte.place(x=550, y=10)
	mycursor.execute("SELECT * FROM proiect;")
	id_proiecte = mycursor.fetchall()
	mycursor.execute("SELECT id_proiect FROM proiect;")
	nr_proiecte = mycursor.fetchall()
	for i in range(0,len(nr_proiecte)):
		adaugare_proiect(i)
	#################
	#	Importanta  #
	#################
	label_importanta = Label(canv, text="Importanta", font="Time 18", fg="green")
	label_importanta.place(x=1150, y=50)
	adaugare_importanta()

	#################
	#	Calcule     #
	#################

	exec_btn = Button(canv, text='Calculeaza', width=14, height=2, font='Time 14', command= lambda: calc_execute())
	exec_btn.place(x=1100, y=730)

	q_btn = Button(canv, text='Interogare', width=14, height=2, font='Time 14', command= lambda: calc_interogare())
	q_btn.place(x=1100, y=670)

	root.mainloop()
	mydb.close()