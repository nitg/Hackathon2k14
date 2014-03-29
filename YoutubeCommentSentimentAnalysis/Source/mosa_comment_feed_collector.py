#oggpnosn
#hkhr


#mosa comment feed collector

#making connection to database to retreive video feeds data
import pymongo as pym
c=pym.Connection(host='localhost')
db=c['youtube']


#making cursor to the get access to individual document
cur=db.videos.find()



#importing urllib to deal with url and json to load the data returned by gdata
from urllib import urlopen
import json




#going through all the document in database,getting video id, which is used to get comments
for entry in cur:
	for video in entry['feed']['entry']:
		video_id=video['mediasgroup']['ytsvideoid']['st']
		print video['mediasgroup']['mediastitle']['st']	
		for start_index in range(1,1000,25):		#to get all the comment
			url='https://gdata.youtube.com/feeds/api/videos/'+video_id+'/comments?&alt=json&start-index='+str(start_index)+'&amp;max-results=25'
			feed=urlopen(url)  #fetching data returned by url
		
			feed_text=feed.read().replace('$','s')		#cant store $ as starting word in key
			try:	
				feed=json.loads(feed_text)	#converts text to json or dictionary
				if 'entry' in feed['feed']:	#to remove all the entries that do not cointan
					db.comments.insert(feed)	
			except ValueError:
				continue
					
						
			
