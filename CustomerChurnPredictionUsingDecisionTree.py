#Decision Tree
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

df = pd.read_csv("TelcoCustomerChurn.csv")

#Gereksiz kolonu siliyoruz.
df = df.drop('customerID', axis = 1)

#String değerleri sayısal değerlere çevireceğiz.
#Replace fonksiyonu da kullanabilirdik ama map kullanıyoruz.
df['Churn'] = df['Churn'].map({'Yes':1,'No':0})

#String olan diğer kolonları da sayısal hale gireceğiz --> Encoding
#Encoding işlemi için pandas'ın getdummies fonkisyonu kullanılır.
#drop_first=True --> Kolondaki True ve False değerlerini ayrı ayrı 2 kolon yapacak. Bir kolona True dediğinde diğer kolon zaten False olacağı için 2 kolon yerine işimizi bir kolonda hallediyoruz.

df.info() #Encoding işlemi yapacağımız kolonları tespit etmek için
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'],errors='coerce') #errors='coerce' --> Dönüştüremediği satır için çözüm

df_encoded = pd.get_dummies(df,drop_first=True)

#Modeli Eğitmek
X= df_encoded.drop('Churn', axis=1)
y= df_encoded['Churn']

#Veriyi ayırma
X_train,X_test,y_train,y_test = train_test_split(X,y, test_size=0.25,random_state=42)

#Model yaratma
model = DecisionTreeClassifier(max_depth=2,min_samples_split=10)

#Modeli fit etme
model.fit(X_train, y_train) #X_train --> Sorular, y_train --> Soruların cevapları


y_pred = model.predict(X_test) #Cevapları olmayan sorular --> X_test

#Model Başarısı test etme
print(accuracy_score(y_test, y_pred)) #y_test --> neleri tahmin etmeliydi, y_pred --> Neleri tahmin etti.


plt.figure()
plot_tree(model)
plt.show()