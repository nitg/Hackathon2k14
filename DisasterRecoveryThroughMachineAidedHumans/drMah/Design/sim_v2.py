#oggpnosn
#hkhr

#A simple simulation of diasater scenario
import copy
import random
import pylab as pl
from Tkinter import *
from math import fabs
import time
from pymongo import Connection

#establishing connection with data base 
c=Connection("localhost",port=27017)

#creating a database handle
try:
    dbh=c["drMah"]
except:
    print "Could not connect to database"

#removing any logs if any
dbh.log.drop()


#unique identity of a person
Uid=10000

#volunteer and Survivor color in simulation
VOLUNTEER_COLOR="Red"
SURVIVOR_COLOR="Black"

#creating Visualization for disaster

class Visualize(object):
    def __init__(self,max_x,max_y,survivorList,volunteerList):
        self.master=Tk()
        self.width=max_x
        self.height=max_y
        self.max_dim=max(self.width,self.height)
        self.w=Canvas(self.master,width=self.width,height=self.height)
        self.w.pack()
        x1, y1 = self._map_coords(0, 0)
        x2, y2 = self._map_coords(max_x, max_y)
        self.w.create_rectangle(x1, y1, x2, y2, fill = "white")
        self.survivorList=[]
        self.volunteerList=[]
        self.time=0
        self.text=self.w.create_text(25, 0, anchor=NW,text="Time:0  Score:0")
        for survivor in survivorList:
            pos=survivor.position
            x,y=pos.x,pos.y
            x1, y1 = self._map_coords(x - 2, y - 2)
            x2, y2 = self._map_coords(x + 2, y + 2)            
            self.survivorList.append(self.w.create_oval(x1, y1, x2, y2,fill = SURVIVOR_COLOR))
        for volunteer in volunteerList:
            pos=volunteer.position
            x,y=pos.x,pos.y
            x1, y1 = self._map_coords(x - 2, y - 2)
            x2, y2 = self._map_coords(x + 2, y + 2)            
            self.volunteerList.append(self.w.create_oval(x1, y1, x2, y2,fill = VOLUNTEER_COLOR))    
        self.master.update() 
   
    def update(self,survivorList,volunteerList,score,delay=.1):
        time.sleep(delay)
        self.time+=1
        if self.survivorList:
            for survivor in self.survivorList:
                self.w.delete(survivor)
                self.master.update_idletasks()
        if self.volunteerList:
            for volunteer in self.volunteerList:
                self.w.delete(volunteer)
                self.master.update_idletasks()
        self.w.delete(self.text)
        self.master.update_idletasks()
        self.survivorList=[]
        self.volunteerList=[]
        for survivor in survivorList:
            pos=survivor.position
            x,y=pos.x,pos.y
            x1, y1 = self._map_coords(x - 2, y - 2)
            x2, y2 = self._map_coords(x + 2, y + 2)            
            self.survivorList.append(self.w.create_oval(x1, y1, x2, y2,fill = SURVIVOR_COLOR))
        for volunteer in volunteerList:
           pos=volunteer.position
           x,y=pos.x,pos.y
           x1, y1 = self._map_coords(x - 2, y - 2)
           x2, y2 = self._map_coords(x + 2, y + 2)            
           self.volunteerList.append(self.w.create_oval(x1, y1, x2, y2,fill = VOLUNTEER_COLOR))    
        self.text = self.w.create_text(25, 0, anchor=NW,text="Time:"+str(self.time)+"  Score:"+str(score)+"        drMah:Disaster Recovery through Machine Aided Human")
        self.master.update()    
         

    def _map_coords(self, x, y):
        "Maps grid positions to window positions (in pixels)."
        return (250 + 450 * ((x - self.width / 2.0) / self.max_dim),
                250 + 450 * ((self.height / 2.0 - y) / self.max_dim))




#a point in the field
class Point(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def checkForSurvivor(self,survivorList,width,height,radius):
        for i in range(1,radius+1):
            chkList=[Point(self.x,self.y)]       
            if self.x+i<width:
                chkList.append(Point(self.x+i,self.y))
                if self.y+i<height:
                    chkList.append(Point(self.x+i,self.y+i))
                if self.y-i>=0:
                    chkList.append(Point(self.x+i,self.y-i))
            
            if self.y+i<height: 
                chkList.append(Point(self.x,self.y+i))

            if self.y-i>=0:
                chkList.append(Point(self.x,self.y-i))

            if self.x-i>=0:
                chkList.append(Point(self.x-i,self.y))
                if self.y+i<height:
                    chkList.append(Point(self.x-i,self.y+i))
                if self.y-i>=0:
                    chkList.append(Point(self.x-i,self.y-i))
            for survivor in survivorList:
                for chk in chkList:
#                                                    print chk,"vs",survivor.position
                    if survivor.position.__eq__(chk):
                        self.x=survivor.position.x
                        self.y=survivor.position.y
                        survivorList.remove(survivor)
                        return True
                
        return False   
        
    def __str__(self):
        return "("+str(self.x)+" "+str(self.y)+")"

    def __eq__(self,other):
        return (self.x==other.x and self.y==other.y)
#representing field

class Field(object):
    def __init__(self,width,height,pSpop,survivorList=[],volunteerList=[]):
        self.ppop=pSpop
        self.pVpop=(.1)*pSpop
        self.width=width
        self.height=height
        self.survivorList=survivorList
        self.volunteerList=volunteerList
        self.score=0
    def update(self):
        #checking whether survivor is still their in data base
        survivorListTemp=copy.deepcopy(self.survivorList)
        for survivor in survivorListTemp:
            if dbh.log.find({"Name":survivor.name})[0]==None:
                self.survivorList.remove(survivor)
        #assigning new  position to volunteer
        for volunteer in self.volunteerList:
            vol=dbh.log.find({"Name":volunteer.name})[0];
            volunteer.position.x=vol["LocationX"]
            volunteer.position.y=vol["LocationY"]
            
        for volunteer in self.volunteerList:
            if volunteer.position.checkForSurvivor(self.survivorList,self.width,self.height,10)==True:
                self.score+=1
        #adding new survivor and volunteer to database        
        if random.random()<=self.ppop:
            pt=Point(random.randrange(1,self.width),random.randrange(1,self.height))
            name="me"+str(len(self.survivorList)+1)
            print "SURVIVOR "+name+" "+str(pt)
            self.survivorList.append(Survivor(name,pt))
            doc={"Name":name,"LocationX":pt.x,"LocationY":pt.y}    
            dbh.log.insert(doc,safe=True)
        if random.random()<=self.pVpop:
            pt=Point(random.randrange(1,self.width),random.randrange(1,self.height))
            name="meV"+str(len(self.volunteerList)+1)
            print "Volunteer "+name+" "+str(pt)
            self.volunteerList.append(Volunteer(name,pt))
            doc={"Name":name,"LocationX":pt.x,"LocationY":pt.y}    
            dbh.log.insert(doc,safe=True)
        return self.score    
    def numOfSurvivor(self):
        return len(self.survivorList)

#representing a person

class Person(object):
    
    def __init__(self,name):
        global Uid
        self.name=name
        Uid+=1
        self.id=Uid

#writing a survivor class    
class Survivor(Person):
    def __init__(self,name,position):
        Person.__init__(self,name) 
        self.position=position

#volunteer class that inherits from person

class Volunteer(Person):
    def __init__(self,name,position):
        Person.__init__(self,name)
        self.position=position


   
def plot1(delay):
    width=400
    height=400
    #survivorList=[Survivor("n"+str(i),Point(random.randrange(1,width),random.randrange(1,height))) for i in range(1,10)]
    ppop=.9
    v1=Visualize(500,500,[],[])
    kuru=Field(width,height,ppop,[],[])
    TIME_STEP=10000
    lol=[]
    for i in range(TIME_STEP):
        time.sleep(delay)
        score=kuru.update()
        v1.update(kuru.survivorList,kuru.volunteerList,score)
#        lol.append(kuru.numOfSurvivor())
#    pl.plot(lol)    
 #   pl.show()

plot1(.1)

#survivor and volunteer
def plot2():
    width=400
    height=400
    #survivorList=[Survivor("n"+str(i),Point(random.randrange(1,width),random.randrange(1,height))) for i in range(1,10)]
    ppop=.1
    v1=Visualize(500,500,survivorList)
    kuru=Field(width,height,ppop,[])
    TIME_STEP=10000
    lol=[]
    for i in range(TIME_STEP):
        kuru.update()
        v1.update(kuru.survivorList)
        lol.append(kuru.numOfSurvivor())


