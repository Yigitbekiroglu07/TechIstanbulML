#KMeans
import pandas as pd 
from sklearn.cluster import KMeans 
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

#Cluster'da train_test_split yapılmaz. Çünkü train_test_split'te olay cevapları ezberle ve ezberlediğin şeyleri test etmektir.
#Burada tüm data modele verilir ve tüm data üstünden grup oluşturulmaya çalışılır.

#Datasetteki amacımız şarkı türlerini gruplamak

df = pd.read_csv("data.csv")

df.info() #Seçeceğimiz kolonları görmek için

#Biz bu kolonalra bakarak tahmin yapmaya çalışacağızz Yani bu kolonlarımız X kolonlarımız olacak, y kolonumuz olmayacak.
col = ['danceability','energy','liveness','loudness','tempo']
X = df[col]

#Kolonlar arasındaki sayısal değerleri standart hale getirmeliyiz.
scaler = StandardScaler()

X_scaled = scaler.fit_transform(X) 



kmeans = KMeans(n_clusters=4, init="k-means++",n_init=10) #n_init=10 --> Orta noktayı bulmak için kaç deneme yapsın

y_kmeans = kmeans.fit_predict(X_scaled)

df['Şarkının türü'] = y_kmeans