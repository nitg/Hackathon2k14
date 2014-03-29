# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <markdowncell>

# Analyzing whatsapp cse groups data.
# 
# Extracting Data.Parsing Data 

# <codecell>

import nltk
import copy
import pandas as pd
import matplotlib.pyplot as  plot
import random
chats=[]
message={}
fob=open("CSE.txt","r") 
for line in fob:
    message={}
    index=line.find("-")
    if index!=-1:
        time=line[:index]
        user=line[index+2:line.find(":",index)]
        text=line[line.find(":",index)+1:]
        message={"time":time,"user":user,"text":text}
        chats.append(message)
    else:
        chats[-1]["text"]+=" "+line
        

# <markdowncell>

# Removing Trivial post by me("Tanay Gahlot")

# <codecell>

temp_chats=copy.deepcopy(chats)
for chat in temp_chats:
    if chat["user"]=="Tanay Gahlot":
        chats.remove(chat)

# <markdowncell>

# Calculating the no of posts/user

# <codecell>

noOfPosts={}
for chat in chats:
    if chat["user"] in noOfPosts:
        noOfPosts[chat["user"]]+=1
    else:
        noOfPosts[chat["user"]]=1
      
sorted(noOfPosts,key=lambda x:noOfPosts[x])

# <codecell>

wordCount={}
allText=''
for chat in chats:
    allText+=" "+chat["text"]
fdist=nltk.FreqDist(allText.split())    
for word in fdist:
    if word in wordCount:
        wordCount[word]+=1
    else:
        wordCount[word]=1
sorted(wordCount,key=lambda x:wordCount[x])[-50:-1]        

# <markdowncell>

# Analyzing the chat time. 

# <codecell>

times=[]
for chat in chats:
    times.append(chat["time"])
times_temp=pd.to_datetime(times)    
ts=pd.Series([1 for i in range(len(times))],index=times_temp)
ts2=ts.resample("D",how="sum",fill_method="ffill")
ts2.plot()
plot.show();

# <codecell>

ts[200]

# <codecell>

plot.show();

# <codecell>


