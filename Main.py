from tkinter import *
from tkinter import scrolledtext
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="database"
)

class NewPerson:
    def __init__(self):
        self.w=Tk()
        self.w.title("New Person")
        self.w.geometry("400x400")

        l=Label(self.w,text="Name:")
        l.grid(column=0,row=0)
        self.n=Entry(self.w)
        self.n.grid(column=1,row=0)
        
        l2=Label(self.w,text="X:")
        l2.grid(column=0,row=1)
        self.X=Entry(self.w)
        self.X.grid(column=1,row=1)
        
        l3=Label(self.w,text="Y:")
        l3.grid(column=0,row=2)
        self.Y=Entry(self.w)
        self.Y.grid(column=1,row=2)
        
        b1=Button(self.w,text="Create",command=self.CreatePerson)
        b1.configure(width=20)
        b1.grid(column=1,row=3)
        
        
        self.w.mainloop()
                
    def CreatePerson(self):
        x=int(self.X.get())
        y=int(self.Y.get())
        name=self.n.get()
        sql="insert into person(name,x,y) values('%s',%d,%d)"%(name,x,y)
        mycursor=mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()
        
        self.w.destroy()
        
   
class ChangePerson:
    def __init__(self):
        self.w=Tk()
        self.w.title("Find Person Based on Name")
        self.w.geometry("600x400")

        l1=Label(self.w,text="NAME:")
        l1.grid(column=0,row=0)
        self.name=Entry(self.w)
        self.name.grid(column=1,row=0)
        
        b1=Button(self.w,text="Submit",command=self.UPPer)
        b1.configure(width=20)
        b1.grid(column=0,row=1)

    def UPPer(self):
        n=self.name.get()
        w3=UpdatePerson(n)
        self.w.destroy()
    
class UpdatePerson:
    def __init__(self,name):
        self.w=Tk()
        self.w.title("Update-Delete Person Based on ID")
        self.w.geometry("600x400")
        
        self.n=name
        sql="select * from person where name like '%%%s%%'"%self.n
        
        l1=Label(self.w,text="ID:")
        l1.grid(column=0,row=0)
        self.idu=Entry(self.w)
        self.idu.grid(column=1,row=0)
        
        b1=Button(self.w,text="Update",command=self.upPer)
        b1.configure(width=20)
        b1.grid(column=2,row=0)
        
        b2=Button(self.w,text="Delete",command=self.DELPer)
        b2.configure(width=20)
        b2.grid(column=2,row=1)
        
        mycursor=mydb.cursor()
        mycursor.execute(sql)
        L=mycursor.fetchall()
        
        txt=scrolledtext.ScrolledText(self.w,width=40,height=10)
        txt.grid(column=0,row=3) 
        
        m="ID NAME X Y\n"
        txt.insert(INSERT,m)
        for s in L:
            txt.insert(INSERT,s)
            txt.insert(INSERT,"\n")        

    def upPer(self):
        iduu=self.idu.get()
        w4=ChangePersonData(iduu)
        self.w.destroy()
    
    def DELPer(self):
        iduu=self.idu.get()
        sql="delete from person where id=%s"%iduu
        mycursor=mydb.cursor()
    
        mycursor.execute(sql)
        mydb.commit()            
        self.w.destroy()
        
class ChangePersonData():
    def __init__(self,iduu):
        self.w=Tk()
        self.w.title("Change DataBase")
        self.w.geometry("400x300")
        
        self.idu=iduu
        
        l1=Label(self.w,text="NAME:")
        l1.grid(column=0,row=0)
        self.name=Entry(self.w)
        self.name.grid(column=1,row=0)
        
        l2=Label(self.w,text="X:")
        l2.grid(column=0,row=1)
        self.x=Entry(self.w)
        self.x.grid(column=1,row=1)
        
        l3=Label(self.w,text="Y:")
        l3.grid(column=0,row=2)
        self.y=Entry(self.w)
        self.y.grid(column=1,row=2)
        
        b1=Button(self.w,text="Save Changes",command=self.SaveUpdate)
        b1.configure(width=30)
        b1.grid(column=2,row=0)
               
    def SaveUpdate(self):
        n=self.name.get()
        X=self.x.get()
        Y=self.y.get()
        sql="update person set name='%s',x=%s,y=%s where id=%s"%(n,X,Y,self.idu)
        mycursor=mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()
        self.w.destroy()
        
class ShowPerson:
    def __init__(self):
        self.w=Tk()
        self.w.title("Show DataBase")
        self.w.geometry("400x300")
            
        sql="select * from person"
        mycursor=mydb.cursor()
        mycursor.execute(sql)
        L=mycursor.fetchall()
        
        txt=scrolledtext.ScrolledText(self.w,width=40,height=10)
        txt.grid(column=0,row=0) 
        m="ID NAME X Y\n"
        txt.insert(INSERT,m)
        for s in L:
            txt.insert(INSERT,s)
            txt.insert(INSERT,"\n")
        
        b1=Button(self.w,text="Exit",command=self.exitShow)
        b1.configure(width=20)
        b1.grid(column=0,row=10)
        
        self.w.mainloop()
        
    def exitShow(self):
        self.w.destroy()

class ShowGraph:
    def __init__(self):
        self.w=Tk()
        self.w.title("Graph")
        self.w.geometry("600x400")
        
        sql="select x,y from person"
        mycursor=mydb.cursor()
        mycursor.execute(sql)
        L=mycursor.fetchall()
        
        X=[]
        Y=[]
        for x in L:
            X.append(x[0])
            Y.append(x[1])
        
        figure=plt.Figure(figsize=(6,5),dpi=100)
        ax=figure.add_subplot(111)
        ax.scatter(X,Y)
        chart_type=FigureCanvasTkAgg(figure,self.w)
        chart_type.get_tk_widget().pack()
    
class MyWinSQL:
    def __init__(self):
        self.w=Tk()
        self.w.title("My DataBase")
        self.w.geometry("600x400")
               
        b1=Button(self.w,text="Insert New Person",command=self.insertPerson)
        b2=Button(self.w,text="Change/Delete/Find Person's Data",command=self.updatePerson)
        b3=Button(self.w,text="Show DataBase",command=self.showPerson)
        b4=Button(self.w,text="Show Graph",command=self.showGraph)
        b5=Button(self.w,text="Exit",command=self.exitPerson)
        
        b1.configure(width=30)
        b2.configure(width=30)
        b3.configure(width=30)
        b4.configure(width=30)
        b5.configure(width=30)
                
        b1.grid(column=0,row=1)
        b2.grid(column=0,row=2)
        b3.grid(column=0,row=3)
        b4.grid(column=0,row=4)
        b5.grid(column=0,row=5)        
        
        self.w.mainloop()
        
    def insertPerson(self):
        w2=NewPerson()
    
    def updatePerson(self):
        w2=ChangePerson()
        
    def showPerson(self):
        w2=ShowPerson()
    
    def showGraph(self):
        w2=ShowGraph()
        
    def exitPerson(self):
        self.w.destroy()
    
        
myFrame=MyWinSQL()
