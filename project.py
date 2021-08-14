from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import socket
import requests
import bs4


def create():
	con = None
	try:
		con = connect("st_records.db")
		sql = "create table student(rno int primary key, name text, marks int)"
		con.execute(sql)
	
	except Exception as e:
		showerror("Table Creation Issue ",e)

	finally:
		if con is not None:
			con.close()

def f1():
	adst.deiconify()
	root.withdraw()

def f2():
	root.deiconify()
	adst.withdraw()

def f3():
	con = None
	try:
		con = connect("st_records.db")
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		msg= ""
		for d in data:
			msg=msg+"Rollno: "+str(d[0])+"   Name: "+str(d[1])+"   Marks: "+str(d[2])+"\n"
		vist_stdata.delete(1.0,END)
		vist_stdata.insert(INSERT,msg)
	except Exception as e:
		showerror("Issue ",e)
	finally:
		if con is not None:
			con.close()
	vist.deiconify()
	root.withdraw()

def f4():
	root.deiconify()
	vist.withdraw()

def f5():
	con = None
	try:
		con = connect("st_records.db")
		cursor = con.cursor()
		sql = "insert into student values('%d','%s','%d')"
		rno = int(adst_entrno.get())
		name = adst_entname.get()
		marks = int(adst_entmarks.get())
		if rno>0:
			if len(name)>=2:
				if 0<= marks <=100:
					cursor.execute(sql % (rno,name,marks))
					showinfo("Success","Record Added")
					con.commit()
				else:
					showerror("Invalid Input","Marks Range:(0-100)")
					con.rollback()
					adst_entmarks.delete(0,END)
					adst_entmarks.focus()
			
			else:		
				showerror("Invalid Input","Enter a valid name")	
				con.rollback()
				adst_entname.delete(0,END)
				adst_entname.focus()
		else:
			showerror("Invalid Input","Roll No should be positive")
			con.rollback()
			adst_entrno.delete(0,END)
			adst_entrno.focus()
	except Exception as e:
		showerror("Failure","Record not added " + str(e))
		con.rollback()
		adst_entrno.delete(0,END)
		adst_entname.delete(0,END)
		adst_entmarks.delete(0,END)
	finally:
		if con is not None:
			con.close()

def f6():
	upst.deiconify()
	root.withdraw()

def f7():
	root.deiconify()
	upst.withdraw()

def f8():
	con = None
	try:
		con = connect("st_records.db")
		cursor = con.cursor()
		sql = "update student set name = '%s',marks='%d' where rno = '%d' "	
		rno = int(upst_entrno.get())
		name = upst_entname.get()
		marks = int(upst_entmarks.get())
		cursor.execute(sql % (name,marks,rno))
		if cursor.rowcount > 0:
			showinfo("Success","Record updated")
			con.commit()
		else:
			showerror("Failure","Record does not exist")
			con.rollback()
			upst_entrno.delete(0,END)
			upst_entname.delete(0,END)
			upst_entmarks.delete(0,END)
	except Exception as e:
		showerror("Failure","Updation Issue "+str(e))
		con.rollback()
		upst_entrno.delete(0,END)
		upst_entname.delete(0,END)
		upst_entmarks.delete(0,END)
	finally:
		if con is not None:
			con.close()	
		
def f9():
	dtst.deiconify()
	root.withdraw()

def f10():
	root.deiconify()
	dtst.withdraw()

def f11():
	con = None
	try:
		con = connect("st_records.db")
		cursor = con.cursor()
		sql = "delete from student where rno = '%d' "	
		rno = int(dtst_entrno.get())
		cursor.execute(sql % (rno))
		if cursor.rowcount > 0:
			showinfo("Success","Record Deleted")
			con.commit()
		else:
			showerror("Failure","Record does not exist")
			con.rollback()
			dtst_entrno.delete(0,END)
			dtst_entrno.focus()
	except Exception as e:
		showerror("Record Deletion Issue",e)
		con.rollback()
		dtst_entrno.delete(0,END)
		dtst_entrno.focus()
	finally:
		if con is not None:
			con.close()
	
def f12():
	con = None
	try:
		con = connect("st_records.db")
		cursor = con.cursor()
		data = pd.read_sql('select * from student', con)
		data.to_csv('st_data.csv')
		data = data.head()
		name = data['name'].tolist()
		marks = data['marks'].tolist()
		x = np.arange(len(name))
		plt.bar(name,marks,color=[ 'blue', 'orange', 'chartreuse', 'yellow', 'red' ])
		plt.title("Batch Information")
		plt.xlabel("Names")
		plt.ylabel("Marks")
		fig=plt.gcf()
		fig.set_size_inches(6,5)
		plt.show()
	except Exception as e:
		showerror("Issue: ",e)
	finally:
		if con is not None:
			con.close()		

def loc():
	try:
		web_address = "https://ipinfo.io/"
		res = requests.get(web_address)		
		data = res.json()	
		location=data['city']
		return location
	except OSError as e:
		showerror("Connection Issue ",e)		

def temp(city):
	try:
		a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
		a2 = "&q=" + city
		a3 = "&appid=c6e315d09197cec231495138183954bd"
		web_address = a1 + a2 + a3
		res = requests.get(web_address)
		data = res.json()	
		main = data['main']
		city_temp = main['temp']
		return city_temp
	except OSError as e:
		showerror("Connection Issue ",e)

def qotd():
	try:
		web_address = "https://www.brainyquote.com/quote_of_the_day"
		res = requests.get(web_address)
		data = bs4.BeautifulSoup(res.text,"html.parser")
		info = data.find('img',{"class":"p-qotd"})
		msg = info['alt']
		return(msg)
	
	except Exception as e:
		showerror("Issue: ",e)
			

create()  

root = Tk()
root.title("S.M.S.")
root.geometry("560x560+360+40")
root.resizable(False,False)
root.configure(background="cyan2")
btnAdd = Button(root,text='ADD',font=('arial',20,'bold'),width=10,command=f1)
btnView = Button(root,text='VIEW',font=('arial',20,'bold'),width=10,command=f3)
btnUpdate = Button(root,text='UPDATE',font=('arial',20,'bold'),width=10,command=f6)
btnDelete = Button(root,text='DELETE',font=('arial',20,'bold'),width=10,command=f9)
btnCharts = Button(root,text='CHARTS',font=('arial',20,'bold'),width=10,command=f12)
text_loc = loc()
root_lblloc = Label(root,text='Location: '+ text_loc ,bd=1,font=('arial',15,'bold'),relief="solid")
city_temp = temp(text_loc)
root_lbltemp = Label(root,text='Temp: ' + str(city_temp) + '°C',bd=1,font=('arial',15,'bold'),relief="solid")
text_qotd = qotd()
root_lblqotd = Label(root,text='QOTD: '+ text_qotd ,bd=1,font=('arial',15,'bold'),relief="solid",wraplength=560)

btnAdd.pack(pady=5)
btnView.pack(pady=5)
btnUpdate.pack(pady=5)
btnDelete.pack(pady=5)
btnCharts.pack(pady=5)
root_lblloc.pack(ipadx=5,ipady=5,padx=5,pady=5,side=LEFT)
root_lbltemp.pack(ipadx=5,ipady=5,padx=5,pady=5,side=RIGHT)
root_lblqotd.place(y=470,width=560)

adst=Toplevel(root)
adst.title("Add Student")
adst.geometry("500x500+400+100")
adst.configure(background="gold")

adst_lblrno = Label(adst,text='Enter Rollno:',font=('arial',20,'bold'))
adst_entrno = Entry(adst,bd=5,font=('arial',20,'bold'))
adst_lblname = Label(adst,text='Enter Name:',font=('arial',20,'bold'))
adst_entname = Entry(adst,bd=5,font=('arial',20,'bold'))
adst_lblmarks = Label(adst,text='Enter Marks:',font=('arial',20,'bold'))
adst_entmarks = Entry(adst,bd=5,font=('arial',20,'bold'))
adst_btnsave = Button(adst,text='SAVE',font=('arial',20,'bold'),command=f5)
adst_btnback = Button(adst,text='BACK',font=('arial',20,'bold'),command=f2)

adst_lblrno.pack(pady=10)
adst_entrno.pack(pady=10)
adst_lblname.pack(pady=10)
adst_entname.pack(pady=10)
adst_lblmarks.pack(pady=10)
adst_entmarks.pack(pady=10)
adst_btnsave.pack(pady=10)
adst_btnback.pack(pady=10)

adst.withdraw()

vist = Toplevel(root)
vist.title("View Student")
vist.geometry("600x400+350+130")
vist.configure(background="gray")

vist_stdata = ScrolledText(vist,width=40,height=10,font=('arial',20,'bold'))
vist_btnback = Button(vist,text='BACK',font=('arial',20,'bold'),command=f4)
vist_stdata.pack(pady=10)
vist_btnback.pack(pady=10)

vist.withdraw()


upst = Toplevel(root)
upst.title("Update Student")
upst.geometry("500x500+400+100")
upst.configure(background="medium spring green")

upst_lblrno = Label(upst,text='Enter Rollno:',font=('arial',20,'bold'))
upst_entrno = Entry(upst,bd=5,font=('arial',20,'bold'))
upst_lblname = Label(upst,text='Enter Name:',font=('arial',20,'bold'))
upst_entname = Entry(upst,bd=5,font=('arial',20,'bold'))
upst_lblmarks = Label(upst,text='Enter Marks:',font=('arial',20,'bold'))
upst_entmarks = Entry(upst,bd=5,font=('arial',20,'bold'))
upst_btnsave = Button(upst,text='SAVE',font=('arial',20,'bold'),command=f8)
upst_btnback = Button(upst,text='BACK',font=('arial',20,'bold'),command=f7)

upst_lblrno.pack(pady=10)
upst_entrno.pack(pady=10)
upst_lblname.pack(pady=10)
upst_entname.pack(pady=10)
upst_lblmarks.pack(pady=10)
upst_entmarks.pack(pady=10)
upst_btnsave.pack(pady=10)
upst_btnback.pack(pady=10)

upst.withdraw()

dtst = Toplevel(root)
dtst.title("Delete Student")
dtst.geometry("500x500+400+100")
dtst.configure(background="orchid1")

dtst_lblrno = Label(dtst,text='Enter Rollno:',font=('arial',20,'bold'))
dtst_entrno = Entry(dtst,bd=5,font=('arial',20,'bold'))
dtst_btnsave = Button(dtst,text='SAVE',font=('arial',20,'bold'),command=f11)
dtst_btnback = Button(dtst,text='BACK',font=('arial',20,'bold'),command=f10)

dtst_lblrno.pack(pady=10)
dtst_entrno.pack(pady=10)
dtst_btnsave.pack(pady=10)
dtst_btnback.pack(pady=10)

dtst.withdraw()

root.mainloop()