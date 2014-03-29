#oggpnosn
#hkhr


#tf idf delta feature

import pymongo as pym #importing essential library for accessing mongo db
c=pym.Connection(host='localhost') #establishing connection to local host
db=c['misspell_words'] #creating database handle


fob=open('missp.dat.txt','r') #creating file object to aCESS misspell.dat.txt which is corpus of misspelled word
misspell={} #dictionary that store misspell word maped to correct word

for line in fob: #accessing individual line
	if line[0]=='$':  #because correct word start with $ for ex $america
		correct_word=line[1:] #this tells the word that follows dollar sign is the correct word
	else:
		incorrect_word=line #this tells that the word that doesnt has dollar sign at start is incorrect for ex americo
		misspell[incorrect_word]=correct_word #inserts americo:america into dictionary

print misspell
