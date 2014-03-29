#oggpnosn
#hkhr


#company name disambiguation problem

fob=open('','r')

company_name=fob.readline().replace('\n','').split()
fob.seek(0)
company_score={}
for name in fob:
	words_name=name.split()
	score=0
	for word in words_name:
		if word in company_name:
			score+=1
	score=float(score)/len(words_name)
	company_score[name]=score

top10=sorted(company_score,key=company_score.get)[:10]
print top10

