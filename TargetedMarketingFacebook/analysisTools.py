# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <markdowncell>

# //oggpnosn
# //hkhr
# 
# Tools for analysis.

# <codecell>

#importing essential library
import facebook as fb
import networkx as nx 
import matplotlib.pyplot as plot
import random

# <markdowncell>

# Loading my facebook graph. To fetch data from facebook one needs to have authorization code. Code can ne obtained in many ways 
# Simplest of that is Graph Explorer tool available at https://developers.facebook.com/tools/explorer/ .Once this code is obtained it has to be passed to 
# facebook.GraphAPI(), which returns a handle through which request can be passed. Using get_object() function request can be made to 
# facebook graph api. Documentation of type of request and permission required are given in facebook developer website.
# Using "/me/friends" request friends list can be obtained. Json file is returned by this request which is a python dictionary which 
# can be used like a regular dictionary. Finally edge will be added to the graph using add_edge() which takes name of my friend and our mutual friend.
# Finally this graph is written to Seminar.gexf in gexf format.

# <codecell>

g=nx.Graph()#initializing Graph
oAuthKey="CAACEdEose0cBAMElA55FEyDbEK4ZBzVokbjsxZAcpbrfIT0sCmwCHQIdGnjorYOUZCuDRpOlnlUAmfHc5NvlCKHvQtQVWDbzNlbsaV4Av7ByOa4lm8czXdINAOaZAeJK3erUiVOCFkf1ZBWlahVwtx6q1CUqg1Y2hULZAf57ZBpIxYXYhUKSZAHuKxHv3l6u1Ki54V83ZCD4bRwZDZD"#key Here
graph=fb.GraphAPI(oAuthKey)#getting a handle to extract data
friends=graph.get_object("/me/friends")#fetching my friends list
friends=friends["data"]#excluding all background information thats of no use
for friend in friends:#looping through my friends list
    mutFriends=graph.get_object("/"+friend["id"]+"/mutualfriends")["data"]#Making a list of my friends mutual friends list
    for mutFriend in mutFriends:#looping through my friend's mutual friend's list
        g.add_edge(friend["name"],mutFriend["name"])#adding my friend and my other friend who are friends with on another
nx.write_gexf(g,"Seminar.gexf") #Saving Graph as Seminar.gexf       
        

# <markdowncell>

# Calculating Degree Centrality. This helps in calculating popularity of a person. Degree centrality is the fraction of nodes connected
# to it. This will help in identifying people who are popular in YOUR network. degree_centrality() return a dictionary object which is sorted
# using sorted() method which takes lambda key as sorting criteria. Then top 10 people in sorted list is printed out. Finally a histogram 
# plot is created using hist() method.

# <codecell>

deg=nx.degree_centrality(g)#getting a dict object
sorted_deg=sorted(deg,key=lambda x:deg[x])#sorting the dict in ascending order
print "Top 10 Celebrity In your network"
for i in xrange(1,11):#getting top 10
    print sorted_deg[-1*i]#printing the ith famous person
plot.hist(deg.values())    #creating a histogram to get an idea of variance in degree centrality value
plot.show() #to show the Histogram

# <markdowncell>

# Calculating Closeness centrality.This gives an idea of closeness a person maintains in your network. 
# This is calculated using closeness_centrality(). This method returns a dictionary object mapping nodes name to their closeness values.
# Sorted() method sorts the dictionary according to the key lambda function provided. In this case values are sorted according to their 
# closeness. Using "for" loop sorted_closeness top 10 element are printed out to console. Finally a histogram plot of closeness is plotted to
# estimate the variation in closeness value.

# <codecell>

closeness=nx.closeness_centrality(g)#getting a dict object
sorted_closeness=sorted(closeness,key=lambda x:closeness[x])#sorting the dict in ascending order
print "Top 10 GossipMonger In your network"
for i in xrange(1,11):#getting top 10
    print sorted_closeness[-1*i]#printing the ith gossiper
plot.hist(closeness.values())    #creating a histogram to get an idea of variance in closeness centrality value
plot.show() #to show the Histogram

# <markdowncell>

# Calculating Betweeness Centrality.This gives an information about the most resourcefull people in your network.It is the fraction of shortest path between every pair of nodes that passes through that node.
# This gives an idea of amount of information that could pass through that node in information diffusion process. betweeness_centrality() return 
# a dictionary object mapping node name to their betweeness values. This is sorted using sorted() function according to lambda key.
# Top 10 of values are printed to stdout. Finally Histogram plot of betweness values is plotted.

# <codecell>

bet=nx.betweenness_centrality(g)#getting a dict object
sorted_bet=sorted(bet,key=lambda x:bet[x])#sorting the dict in ascending order
print "Top 10 Resourcefull In your network"
for i in range(1,11):#getting top 10
    print sorted_bet[-1*i]#printing the ith resourceful person
plot.hist(bet.values())    #creating a histogram to get an idea of variance in degree centrality value
plot.show() #to show the Histogram

# <markdowncell>

# Calulating Page Rank.This was designed orignally by google to rank web pages. pagerank() method returns a dictionary object mapping
# node name to their page rank score which is sorted using python inbuilt sorted() function. Top 10 scorer are printed out to the console.
# Finally histogram plot of page rank score is plotted.

# <codecell>

pr=nx.pagerank(g)#getting a dict object
sorted_pr=sorted(pr,key=lambda x:pr[x])#sorting the dict in ascending order
print "Top 10 Important people In your network"
for i in range(1,11):#getting top 10
    print sorted_pr[-1*i]#printing the ith important person
plot.hist(pr.values())    #creating a histogram to get an idea of variance in pagerank centrality value
plot.show() #to show the Histogram

# <markdowncell>

# Calculating EigenVector value. This tell about gray cardinal value in my network. Gray cardinal is a person who is connected to most 
# important people in network. Its analogus to Osama Bin Laden who wasn't connected to all people in taliban but few important people.
# Its calculated recursively by associating two paramenter to alpha and beta. Here eigenvector_centrality gives dictionary mapping
# nodes name to their eigenvector value.

# <codecell>

ev=nx.eigenvector_centrality(g)#getting a dict object
sorted_ev=sorted(ev,key=lambda x:ev[x])#sorting the dict in ascending order
print "Top 10 Gray Cardinal In your network"
for i in range(1,11):#getting top 10
    print sorted_ev[-1*i]#printing the ith gray cardinal person
plot.hist(ev.values())    #creating a histogram to get an idea of variance in eigen vector centrality value
plot.show() #to show the Histogram

# <markdowncell>

# Comparing Degree, Closeness, Betweeness, PageRank, EigenVector. 

# <codecell>

name1="Viraj Nayak"
name2="Kethzi Gildona Gilbert"
print "Measure     ",name1,"                ",name2
print "Degree:     ",deg[name1],"\t",deg[name2]
print "Closeness:  ",closeness[name1],"\t",closeness[name2]
print "Betweeness: ",bet[name1],"\t",bet[name2]
print "PageRank:   ",pr[name1],"\t",pr[name2]
print "EigenVector:",ev[name1],"\t",ev[name2]

# <markdowncell>

# Calculating Connected Subcomponent of my social network.

# <codecell>

components=nx.connected_component_subgraphs(g)
print "There are ",len(components),"component"
for component in components:
    print "length:",len(component)

# <markdowncell>

# Plotting Ego Graph of a person.

# <codecell>

name="Abhinav Pandey"
ego=nx.ego_graph(g,name,radius=1)
nx.draw(ego)
plot.show()
print "Clustering:",nx.clustering(g,name)

# <markdowncell>

# Calculating Cliques in Graph. These are closed faternity like terrorist organization.

# <codecell>

clique=nx.find_cliques(g)
clique=list(clique)
sorted_clique=sorted(clique,key=lambda x:len(x))
sorted_clique[-1]

# <codecell>


# <codecell>


