
# coding: utf-8

# In[1]:


from sklearn.feature_extraction.text import CountVectorizer
import sklearn.datasets
import scipy as sp
import nltk.stem
import numpy as np
import os
import wx
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
english_stemmer = nltk.stem.SnowballStemmer('english')

class StemmedTfidfVectorizer(TfidfVectorizer):
   def build_analyzer(self):
        analyzer = super(TfidfVectorizer,self).build_analyzer()
        return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))

vectorizer = StemmedTfidfVectorizer(min_df=1,max_df=0.5,stop_words='english', decode_error='ignore')
all_data = sklearn.datasets.fetch_20newsgroups(subset='all')
groups = ['comp.graphics', 'comp.os.ms-windows.misc',
'comp.sys.ibm.pc.hardware', 'comp.sys.mac.hardware',
'comp.windows.x', 'sci.space']
train_data = sklearn.datasets.fetch_20newsgroups(subset='train',categories=groups)
test_data = sklearn.datasets.fetch_20newsgroups(subset='test')
vectorized = vectorizer.fit_transform(train_data.data)
num_clusters = 50
km = KMeans(n_clusters=num_clusters, init='random', n_init=1,verbose=1, random_state=3)
km.fit(vectorized)
similar = []

def load(event):
  file = open(filename.GetValue())
  contents.SetValue(file.read())
  posts =contents.GetValue()
  new_post_vec = vectorizer.transform([posts])
  new_post_label = km.predict(new_post_vec)[0]
  similar_indices = (km.labels_==new_post_label).nonzero()[0]
  similar=[]
  for i in similar_indices:
              dist = sp.linalg.norm((new_post_vec-vectorized[i]).toarray())
              similar.append((dist,train_data.data[i]))
             
  similar = sorted(similar)
  print(len(similar))
  show_at_1 =similar[0]
  print(show_at_1)
  results.SetValue(''.join(show_at_1[1]))
      
    
def save(event):
  file = open(filename.GetValue(), 'w')
  file.write(contents.GetValue())
  file.close()

app = wx.App()
win = wx.Frame(None, title="Related Posts Engine", size=(410, 335))
bkg = wx.Panel(win)
loadButton = wx.Button(bkg, label='Open')
loadButton.Bind(wx.EVT_BUTTON, load)
saveButton = wx.Button(bkg, label='Save')
saveButton.Bind(wx.EVT_BUTTON, save)
filename = wx.TextCtrl(bkg)
contents = wx.TextCtrl(bkg, style=wx.TE_MULTILINE | wx.HSCROLL)
results  = wx.TextCtrl(bkg, style=wx.TE_MULTILINE | wx.HSCROLL)
hbox = wx.BoxSizer()
hbox.Add(filename, proportion=1, flag=wx.EXPAND)
hbox.Add(loadButton, proportion=0, flag=wx.LEFT, border=5)
hbox.Add(saveButton, proportion=0, flag=wx.LEFT, border=5)
vbox = wx.BoxSizer(wx.VERTICAL)
vbox.Add(hbox, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
vbox.Add(contents, proportion=1,
flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)
vbox.Add(results, proportion=1,
flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=5)
bkg.SetSizer(vbox)
win.Show()
app.MainLoop()






      




