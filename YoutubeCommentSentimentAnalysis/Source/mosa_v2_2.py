#oggpnosn
#hkhr

# MOSA V2

import nltk
import math
#getting data to configure training set for the classifier

import pymongo as pym #importing library pymongo to get essential 
c=pym.Connection(host='localhost') #Making Connection to database train_set
db=c['train_set'] #database handle top train set
comments=db.comment.find() # Cursor to train set
label_comment=[] #list in which training set will be stored as collection of tuple in the format [(comment,comment_label)....]

for comment in comments:  #acess to individual document in train_set
	label_comment.append((comment['comment'],comment['comment_class'])) #appends data to label_class a list of tuple 

#fetching data from misspell_words to implement spell checker
 
	
db=c['misspell_words'] #opening mispell word dictionary stored in database
cursor=db.words.find() #opens cursor to the document
misspell=cursor[0] #stores the dictionary which maps incorrect word to correct word


def spell_check(words): #function to check the words and replace incorrect word with a correct one
	for word in words:	#goes through all the words
		if word in misspell: #checks whether the word is correctly spelled
			words.remove(word) #removes incorrect word
			words.append(misspell[word]) # with correct one :)
	return words #returns the corrected words set back


#getting fdist of words in trainset
P=0
N=0
word_label=[]

for comment in label_comment:
	for word in comment[0].split():
		word_label.append((word,comment[1]))
	if comment[1]=='positive':
		P+=1
	else:
		N+=1

fdist=nltk.FreqDist(word_label)

	

#tf idf delta feature

def tf_idf_delta(comment):
	words=comment.split()
	words=spell_check(words)
	word_count={}
	su=0
	count=0
	for word in words:
		if word in word_count:
			word_count[word]+=1
		else:
			word_count[word]=1
	for word in words:
		pt=fdist[(word,'positive')]
		nt=fdist[(word,'negative')]
		if pt==0:pt=1
		if nt==0:nt=1
		score=float(pt)/nt
		score*=N
		score/=P
		score=math.log(score)
		score*=word_count[word]
		su+=score;
	su=round(su)		
	return {'tf_idf_score':su}
	
	

#preparing Training set

train_set=[(tf_idf_delta(n),g) for (n,g) in label_comment]
classifier=nltk.NaiveBayesClassifier.train(train_set)

#getting comments from youtube


db=c['youtube']
from datetime import datetime
cursor=db.comments.find()
cursor_length=cursor.count()

#get_title() to fetch title for a given video_id

def get_title(video_id):
	cur=db.videos.find()
	for videos in cur:
		if 'entry' in videos['feed']:
			for i in range(0,50):
				try:
					if video_id==videos['feed']['entry'][i]['mediasgroup']['ytsvideoid']['st']:
						return videos['feed']['entry'][i]['mediasgroup']['mediastitle']['st']
				except IndexError:
					break



for start_index in range(0,cursor_length,40):
	total_result=cursor[start_index]['feed']['openSearchstotalResults']['st'];print '------------------';print total_result
	cycles=total_result/25	#no of cycles of 25 comment to be executed
	if cycles==0:cycles=1;	#if less than 25 comments
	if cycles>40:cycles=40	#if cycles are greater than 40 
	to_be_inserted={};ce='terminal'
	if 'entry'  in cursor[start_index]['feed']:			#to avoid cases in which there arent any comment
		video_id=cursor[start_index]['feed']['entry'][0]['ytsvideoid']['st'];
		title=get_title(video_id);print title
		score=0;count=0
		for index in range(start_index,start_index+cycles):	#going through all cycle 
			if 'entry'  in cursor[index]['feed']:
				for i in range(0,49):
					try:
						if cursor[index]['feed']['entry'][i]['ytsvideoid']['st']!=video_id:ce='exit';break
						comment=cursor[index]['feed']['entry'][i]['content']['st'];
						if title=="How I Met Your Mother - Ted's House":print comment
						comment_class=classifier.classify(tf_idf_delta(comment));
						if comment_class=='positive':
							score+=1
						count+=1
					except IndexError or KeyError:
						break
				if ce=='exit':break
		score=float(score)/count;
		score*=100;print score;print count
		to_be_inserted['title']=title
		to_be_inserted['score']=score; 
		to_be_inserted['time']=datetime.now().isoformat()
		to_be_inserted['video_id']=video_id
		to_be_inserted['comments_evaluated']=count
		db.results.insert(to_be_inserted);print '-------------------------'
	
			



	
