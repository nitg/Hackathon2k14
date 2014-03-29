#oggpnosn
#hkhr

# MOSA V2


#getting data to configure training set for the classifier

import pymongo as pym #importing library pymongo to get essential 
c=pym.Connection(host='localhost') #Making Connection to database train_set
db=c['train_set_test'] #database handle top train set
comments=db.comment.find() # Cursor to train set
label_comment=[] #list in which training set will be stored as collection of tuple in the format [(comment,comment_label)....]

for comment in comments:  #acess to individual document in train_set
	label_comment.append((comment['comment'],comment['comment_class']))
	
