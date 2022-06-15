#!/usr/bin/env python
# coding: utf-8

# # Topic Modelling using LSA

# Algoritma LSA (Latent Semantic Analysis) adalah salah satu algoritma yang dapat digunakan untuk menganalisa hubungan antara sebuah frase/kalimat dengan sekumpulan dokumen.

# Pada program ini akan menggunakan data abstrak dari portal tugas akhir trunojoyo program studi Teknik Informatika (https://pta.trunojoyo.ac.id/c_search/byprod/10), berikut code untuk melakukan crawling data:

# # # Crawling Data

# In[1]:


# install library beautifulsoup4 untuk melakukan crawling data
pip install beautifulsoup4


# In[ ]:


# import library
from bs4 import BeautifulSoup
import requests
import csv

# membuat list, dataAbstract untuk menampung data sementara setelah crawling
# dataFix untuk menampung data yang sudah ditambahkan kolom index dan siap di convert ke csv
dataAbstract = []
dataFix = []

# function crawlAbstract untuk mengambil data judul dan abstract dari halaman detail pta trunojoyo teknik informatika
def crawlAbstract(src):
    # inisialisasi beautifulsoup4     
    global c
    tmp = []
    page = requests.get(src)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # mengambil data judul     
    title = soup.find(class_="title").getText()
    tmp.append(title)
    
    # mengambil data abstract     
    abstractText = soup.p.getText()
    tmp.append(abstractText)
    
    return tmp

# function getLinkToAbstract digunakan untuk mengambil data link menuju halaman detail
# parameter src berisi link halaman daftar tugas akhir
def getLinkToAbstract(src):
    # inisialisasi beautifulsoup4
    global c
    page = requests.get(src)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # mendapatkan semua link menuju halaman detail
    items = soup.find(class_="items").find_all('a')
    # looping setiap link untuk mendapatkan nilai href, 
    # link tersebut digunakan sebagai parameter function crawlAbstract agar mendapat data judul dan abstract
    for item in items:
        if item.get('href') != '#':
            tmp = crawlAbstract(item.get('href'))
            # dataAbstract menampung data sementara hasil crawl
            dataAbstract.append(tmp)


# link halaman pta trunojoyo prodi teknik informatika yang akan di crawl
# halaman ini berisi daftar tugas akhir
link = "https://pta.trunojoyo.ac.id/c_search/byprod/10"
# mengambil data sampai halaman 100
for i in range(1, 101):
    # memindah halaman menuju halaman selanjutnya     
    src = f"https://pta.trunojoyo.ac.id/c_search/byprod/10/{i}"
    # counter untuk melihat progress berapa persen proses crawling
    print(f"Proses-{i}%")
    # memanggil function getLinkToAbstract untuk mendapatkan setiap link ke halaman detail
    getLinkToAbstract(src)

# setelah memperoleh semua data abstract, data tersebut ditampung di list dataAbstract
# data perlu ditambahkan kolom index sebagai id
# looping berikut bertujuan menambahkan kolom index di setiap baris, lalu disimpan di list dataFix
for i in range(1, len(dataAbstract)+1):
    dataAbstract[i-1].insert(0, i)
    dataFix.append(dataAbstract[i-1])

# menyimpan data hasil crawl dengan format csv
header = ['index', 'title','abstract']
with open('dataHasilCrawl.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(header)
    write.writerows(dataFix)
# akan ada file dataHasilCrawl.csv berisi id, judul dan abtrak dari pta trunojoyo teknik informatika sejumlah 500 record
# proses crawling selesai


# # # Preprocessing

# Tahap selanjutnya melakukan pre-processing data dengan tahapan 1.punctuation removal 2.stemming
# 1. punctuation removal adalah proses membersihkan teks dari tanda baca dan angka
# 2. Stemming adalah proses pemetaan dan penguraian bentuk dari suatu kata menjadi bentuk kata dasarnya. Sederhananya, proses mengubah kata berimbuhan menjadi kata dasar, misal kata "membosankan" menjadi "bosan"
# 3. Stopwords merupakan kata yang diabaikan dalam pemrosesan karena termasuk kata umum yang mempunyai fungsi tapi tidak mempunyai arti.Maksud dari kata umum adalah kata yang frekuensi kemunculannya tinggi, misalnya kata penghubung seperti “dan”, “atau”, “tapi”, “akan” dan lainnya

# Install terlebih dahulu library yang akan digunakan:
# Sastrawi digunakan untuk proses stemming dan stopword

# In[ ]:


pip install sastrawi


# In[ ]:


import csv # untuk menyimpan hasil dalam format csv
import string 
import re # re : digunakan untuk proses punctuation removal

# memanggil function yang digunakan
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# membuat list untuk menampung data
dataAbstract = []
dataAfterPreprocessing = []

# inisialisasi library sastrawi untuk stemming
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# inisialisasi library sastrawi untuk proses stopword removal
factory2 = StopWordRemoverFactory()
stopword = factory2.create_stop_word_remover()

# untuk counter proses
count = 1

# membaca data dari proses sebelumnya
with open("dataHasilCrawl.csv", "r") as f:
    reader = csv.reader(f)
    next(reader, None)
    for row in reader:
        if len(row) != 0:
#           data sebelum proses disimpan pada list dataAbstract
            dataAbstract.append(row)

# looping untuk memproses setiap data
for abstract in dataAbstract:
#   ambil data
    tmp = abstract.pop()
#   lakukan case folding (mengubah teks menjadi bentuk standar: huruf kecil)
    tmp = tmp.lower()
#   menghapus angka
    tmp = re.sub(r"\d+", "", tmp)
#   menghapus tanda baca
    tmp = tmp.translate(str.maketrans("","",string.punctuation))
#   menghapus whitespace
    tmp = tmp.strip()
    tmp = re.sub('\s+',' ',tmp)
#   melakukan proses stemming
#     tmp = stemmer.stem(tmp)
#   melakukan proses stopword removal
    tmp = stopword.remove(tmp)
#   menambahkan data ke list dataAfterPreprocessing
    abstract.append(tmp)
    dataAfterPreprocessing.append(abstract)
#   print counter proses
    print(f"Proses:{count}/{len(dataAbstract)}")
    count+=1

# menyimpan data dari list dataAfterPreprocessing ke bentuk csv
header = ['index', 'title','abstract_cleaned']
with open('dataAfterPreprocessing.csv', 'w', encoding="utf-8") as f:
    write = csv.writer(f)
    write.writerow(header)
    write.writerows(dataAfterPreprocessing)
# akan ada file dataAfterPreprocessing.csv berisi id, judul, abtract yang sudah dipreprocessing
# preprocessing sudah selesai


# # # LSA

# Masuk ke tahap penerapan LSA

# install library sklearn, pandas, matplotlib dan seaborn

# In[ ]:


pip install sklearn


# In[ ]:


pip install pandas


# In[ ]:


pip install matplotlib


# In[ ]:


pip install seaborn


# In[8]:


# inisialisasi semua library yg digunakan
import numpy as np
import pandas as pd
import nltk
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns

# mengatur tampilan matplotlib ketika menampilkan data
get_ipython().run_line_magic('matplotlib', 'inline')
style.use('fivethirtyeight')
sns.set(style='whitegrid',color_codes=True)


# In[9]:


# menggunakan library sklearn untuk membuat tfidf, disini baru import function-nya dulu
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer


# In[10]:


from nltk.corpus import stopwords  #stopwords


# In[31]:


stop_words=set(nltk.corpus.stopwords.words('indonesian'))


# In[32]:


# membaca data
df=pd.read_csv('./dataAfterPreprocessing.csv')
# menampilkan data
df.head()


# In[33]:


# menghapus data index dan title karena tidak digunakan
df.drop(['index'],axis=1,inplace=True)
df.drop(['title'],axis=1,inplace=True)


# In[34]:


# menampilkan 10 baris data
df.head(10)


# In[35]:


# menghitung tfidf
vect =TfidfVectorizer(stop_words=stop_words,max_features=1000)
vect_text=vect.fit_transform(df['abstract_cleaned'].values.astype('U'))


# In[40]:


# menampilkan hasil perhitungan tfidf
print(vect_text.shape)
print(vect_text)


# Kita sekarang dapat melihat kata-kata yang paling sering dan langka di abstrak berdasarkan skor idf. Semakin kecil nilainya berarti kata tersebut lebih sering digunakan (umum) dalam abstrak.

# In[42]:


idf=vect.idf_
dd=dict(zip(vect.get_feature_names(), idf))
l=sorted(dd, key=(dd).get)
# print(l)
print(l[0],l[-1])
print(dd['hasil'])
print(dd['telapak'])


# Dapat dilihat kata paling sering digunakan adalah "hasil" sementara kata paling jarang digunakan adalah "telapak"

# In[43]:


from sklearn.decomposition import TruncatedSVD
lsa_model = TruncatedSVD(n_components=10, algorithm='randomized', n_iter=10, random_state=42)

lsa_top=lsa_model.fit_transform(vect_text)


# In[44]:


print(lsa_top)
print(lsa_top.shape)  # (no_of_doc*no_of_topics)


# In[45]:


l=lsa_top[0]
print("Document 0 :")
for i,topic in enumerate(l):
    print("Topic ",i," : ",topic*100)


# In[46]:


print(lsa_model.components_.shape) # (no_of_topics*no_of_words)
print(lsa_model.components_)


# In[30]:


# most important words for each topic
vocab = vect.get_feature_names()

for i, comp in enumerate(lsa_model.components_):
    vocab_comp = zip(vocab, comp)
    sorted_words = sorted(vocab_comp, key= lambda x:x[1], reverse=True)[:10]
    print("Topic "+str(i)+": ")
    for t in sorted_words:
        print(t[0],end=" ")
    print("\n")


# In[ ]:




