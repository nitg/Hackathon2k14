# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

#oggpnosn
#hkhr

from IPython.core.display import Image,display
#display(Image(filename="DSC_0272.JPG"))
import matplotlib.pyplot as plot

# <codecell>

from sklearn.datasets import load_digits
digits=load_digits()

# <codecell>

fig=plot.figure(figsize=(6,6))
fig.subplots_adjust(left=0,right=1,bottom=0,top=1,hspace=.05,wspace=.05)
for i in range(64):                   
    ax=fig.add_subplot(8,8,i+1,xticks=[],yticks=[])
    ax.imshow(digits.images[i],cmap=plot.cm.binary)
    ax.text(0,7,str(digits.target[i]))

# <codecell>

plot.show()

# <codecell>

from sklearn.datasets import load_boston
bos=load_boston()

# <codecell>

fig=plot.figure(figsize=(4,6))
for i in range(10):                   
    ax=fig.add_subplot(4,6,i+1,xticks=[],yticks=[])
    ax.scatter(bos.data[:,i],bos.target)
    

# <codecell>

from sklearn import linear_model
clf=linear_model.LinearRegression()
#clf.fit(bos.data,bos.target)

# <codecell>

clf.fit(bos.data,bos.target)

# <codecell>

predicted=clf.predict(bos.data)
plot.scatter(predicted,bos.target)
plot.show()

# <codecell>

clf=linear_model.LogisticRegression()

# <codecell>

clf.fit(bos.data,bos.target)

# <codecell>

clf.predict_proba(bos.target)

# <codecell>


