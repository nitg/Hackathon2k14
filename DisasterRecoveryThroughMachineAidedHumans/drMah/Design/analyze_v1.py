#oggpnosn
#hkhr
#oggpnosn
#hkhr

#importing essential
from pymongo import Connection
import copy
#establishing a connection
c=Connection(host="localhost",port=27017)

#creating a database handle
try:
    dbh=c["drMah"]
except:
    print "Could not connect to database";

def move(name,x,y):
    cur=dbh.log.find({"Name":name})
    record=cur[0]
    copyRecord=copy.deepcopy(record)
    copyRecord["LocationX"]=x
    copyRecord["LocationY"]=y
    dbh.log.update({"Name":name},copyRecord,safe=True)
    print "Moved",name,"to(",x,",",y,")"
def volunteerPosition():
    cur=dbh.log.find()
    for record in cur:
        if record["Name"][:3]=="meV":
            print record["Name"],"  (",record["LocationX"],",",record["LocationY"],")"

def parseIt(inp):
    inp=inp.split()
    if inp[0][0]!="\\":
        print "kindly submit a valid query"
    else:
        if inp[0][1:]=="mov":
            move(inp[1],inp[2].split(",")[0],inp[2].split(",")[1])

        elif inp[0][1:]=="volunteerposition":
            volunteerPosition()
        elif inp[0][1:]=="movnn":
            moveNN(inp[1])
        else:
            print "Type a Valid command"


while True:
    inp=raw_input(">")
    parseIt(inp)
