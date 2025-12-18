#mathplotlib : MATLAB çizimlerini Python'a yapmak için
#Seaborn: Modern hali.
#Plotly: Daha gelişmiş çizimler için. JS temellidir.

import matplotlib.pyplot as plt
import seaborn as sns

df = sns.load_dataset("tips")

df.head(50)

#Hesap ve bahşiş arasındaki ilişkiyi grafiğe dökeceğiz.

plt.figure(figsize=(10,8)) #figure, x ve y olan kutucuğu oluşturmak demek. Boş bir kutucuk oluştururuz.

#Scatter Plot örneği : Hesap ve Bahşiş ilişkisi
plt.scatter(df["total_bill"], df["tip"], color = "red", alpha=0.5) #Grafik çizmek için oluşturulur. Scatter, bar, histogram diyerek istediğimiz grafik fonksiyonunu çağırabiliriz.
plt.title("Hesap ve Bahşiş ilişkisi")
plt.xlabel("Hesap Bilgisi")
plt.ylabel("Bahşiş tutarı")
plt.show() #Grafiğin print komutudur.


#Histogram
plt.hist(df["total_bill"], color = "green")
plt.title("Hesap tutarlarının dağılımı")
plt.xlabel("Hesap Tutarı")
plt.ylabel("Hesap tutarının dağılımı")
plt.show() #Grafiğin print komutudur.

#Bar
ozet_veri = df.groupby("day")["total_bill"].mean() #data frame'i daye göre grupla. Ödenen tutarların ortalamasını al.

plt.bar(ozet_veri.index, ozet_veri.values, color = "orange") #df["day"] demedik çünkü df'de günler kolon şeklinde değil index şeklinde
plt.show()

#Line Plot - Çizgi Grafik

plt.plot(df["total_bill"], color = "blue", linestyle = "-",linewidth = 2) #çizgi grafik çizme komutu plottur.
plt.show()

sıralı_df = df.sort_values("total_bill").reset_index() #Total bill kolonunun sıfırıncı indexten son indexe artacak şekilde sıraladık.
plt.plot(sıralı_df["total_bill"], color = "blue", linestyle = "-",linewidth = 2) #çizgi grafik çizme komutu plottur.
plt.show()


#%%Seaborn --> Yaptığımız yöntem aynı olacak. Parametrelerde dataframe'i ister, matplotlib'te bu yok.

#dimension --> boyut yani her bir kolona verilen isim.

kendi_paletim = {
    "Male": "Blue",
    "Female" : "Red"
    }

plt.figure(figsize=(10,10))
sns.scatterplot(data=df,x="total_bill",y="tip",s=100, hue = "sex", palette=kendi_paletim) #Grafiğe,datanın tamamı verilir. Farkı buradadır.
plt.title("Hesap-Bahşiş İlişkisi")
plt.show()

#Bar Plot

#Burada günlerin toplam tutarını hesaplayıp ortalamasını al demedik, (üstte demiştik) ona rağmen kendi kendine yaptı. Bu Seaborn avantajlarından birisidir.
sns.barplot(data=df, x="total_bill",y="day", hue = "day")
plt.show()

# Eğer ortalama almasını değil de başka bir işlem yapmasını istersek estimator parametresini kullanmalıyız.
sns.barplot(data=df, x="total_bill",y="day", hue = "day", estimator="sum")
plt.show()

#%% Plotly --> Burada yapılan grafik tarayıcıda açılır. Matplotlib ve Seaborn statik bir görüntü verir, Plotly ise daha iyi görüntüler çıkarır.


import plotly.express as px #Daha hızlı grafik çözümü
#import plotly.graph_object as pgo --> Daha detaylı grafik çizimi

fig = px.scatter(df,x="total_bill",y="tip",color="sex",size="size") #verinin hepsini(df) bu da ister.
fig.show(renderer="browser") #Tarayıcıda açacağı için renderer parametresini vermek zorunludur.


""" Graph Object ile aynı grafiği çizme

fig.add_trace(go.Scatter(
    x=df[df['sex'] == 'Female']['total_bill'],
    y=df[df['sex'] == 'Female']['tip'],
    mode='markers',
    name='Female'
))

fig.add_trace(go.Scatter(
    x=df[df['sex'] == 'Male']['total_bill'],
    y=df[df['sex'] == 'Male']['tip'],
    mode='markers',
    name='Male'
)) """
