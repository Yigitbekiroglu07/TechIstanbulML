#Logistic Regression
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

df = pd.read_csv("diabetes.csv")

df.head()

df.describe()

df.info()

df['Outcome'].value_counts()
#Kolonlar arasındaki korelasyonu görmek için seaborn'ün heatmap fonksiyonu kullanılır.

df.corr()
plt.figure()
sns.heatmap(df.corr(), annot=True, cmap = 'coolwarm')
plt.show()

#Feature Engineering

#Bu kolonları, mantıksız olacağı için 0 olmasını istemiyoruz.
coltofix = ['Glucose','BloodPressure','SkinThickness','Insulin','BMI'] #column to fix (coltofix)

for c in coltofix:
    df[c] = df[c].replace(0,df[c].mean())

#Elimizdeki data frame'i X ve y şeklinde 2'ye ayırıyoruz.
X = df.drop('Outcome', axis=1)
y = df['Outcome']

#Veriyi train ve test olarak ayıracağız.
X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=42)

#Kolonlar arasındaki artış aynı şeyi ifade etmez. Aralarındaki artış standartize edilmelidir çübkü kolonların etkisi biribirinden fazla olmamalıdır..
#Örneğin, hamile kalmakla kan basıncındaki artış aynı değildir.

#StandardScaler bir class olduğu için nesne türetmek zorundayız, scaler nesnesini türetiyoruz.
scaler = StandardScaler()

# Gönderdiğimiz datayı içerisine fit etmek için fit_transform kullanılır.
# Modeli eğitmek için kullandığımız datayı scale edeceğiz. Kolonlar arasındaki farkı gidermek için eğitim datasını gönderiyoruz.
X_train_scalaed = scaler.fit_transform(X_train)

# test datasını transform fonksiyonu ile scaler yapacağız. Test datası cevap anahtarı olduğu için onu fit_transform ile yapmamıza gerek yoktur.
X_test_scaled = scaler.transform(X_test)


#Modeli yaratmak
model = LogisticRegression(C=1, solver='liblinear', random_state=42)

#Modeli Eğitmek
#Modeli hangi data ile eğitmek istiyorsak onu parametre olarak veriyoruz, (X_train_scaled) ve bir de cevap anahtarı vermeliyiz (y_train)
# X_train vermedik çünkü standardize işlemi uyguladık en son hangi X_train'i kullandıysak onu vermeliyiz.
model.fit(X_train_scalaed, y_train)

#Modele tahmin yaptırtmak
#X_test_scaled içindeki değerleri tahmin yapmasını istiyoruz.
#Buradaki sonuçlar, y_test nesnesi ile aynı olmalıdır.
y_pred = model.predict(X_test_scaled)

#Başarıyı ölçen metrikler
print(classification_report(y_test, y_pred))

# Precision: TP / (TP + FP)
# Recall: TP / (TP + FN)
# F1 score: Precision + Recall'un harmonik ortalamasıdır.
# Support: Test datası içerisinde kaç tane 0 ve 1 değerinin olduğunu verir.