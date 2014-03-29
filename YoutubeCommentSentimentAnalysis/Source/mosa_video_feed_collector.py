#oggpnosn
#hkhr

#mosa video feed collector

#converts the search term to the format in which it has to be supplied
SEARCH_TERM='tv ads commercial india'
SEARCH_TERM=SEARCH_TERM.replace(' ','+')


#
import json
import pymongo as pym
c=pym.Connection()
db=c['youtube']
import ast
import bson.errors

from urllib import urlopen
for start_index in range(1,1000,50):
	url='http://gdata.youtube.com/feeds/api/videos?&alt=json&q='+SEARCH_TERM+'&start-index='+str(start_index)+'&max-results=50&v=2&orderby=relevance&uploader=partner&genre=11&paid_content=true&time=this_month&duration=short&license=youtube&region=IN'
	feed=urlopen(url)
	feed=json.loads(feed.read().replace('$','s'))	
	try:
		db.videos.insert(feed);print start_index
	except bson.errors.InvalidDocument:
		continue	
	

