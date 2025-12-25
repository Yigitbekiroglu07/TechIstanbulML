import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

#2 : Veri Analizi

df = pd.read_csv("insurance.csv")
#İlk 5 satıra göz atma
df.head()
#data frame hakkında null değer ve data türleri hakkında blgi alma
df.info()
#data frame hakkında istatistiki bilgi alma
df.describe()

plt.figure()
sns.barplot(data = df, x="smoker",y="charges")
plt.show()

plt.figure()
sns.boxplot(data = df, x="smoker",y="charges")
plt.show()

#3 : Veri Analizi

#Feature Engineering - Encoding - One Hot Encoding
df_encoded = pd.get_dummies(df,columns=["sex","smoker","region"], drop_first=True)

X = df_encoded.drop('charges', axis = 1)
y = df_encoded['charges']

X_train, X_test, y_train ,y_test = train_test_split(X, y, test_size=0.2)

# 4. Model Geliştirme

model = LinearRegression()
#Eğitmek için LinearRegression sınıfındaki fit fonksiyonu kullanılır.
#X_train ve y_train gönderilir çünkü eğitim için o datalar tercih edildi.
model.fit(X_train, y_train) #OOP gereği, LinearRegression sınıfını model'e atama yaptığımız için özelliklerini kullanabiliriz.
y_pred = model.predict(X_test) #cevabını bilmediği soruları sormak istiyoruz, o yüzden X_test gönderilir. Tahmin yaptırmış oluyoruz. Tahmin göndereceğinden atama yapmamız gerek.

# 5. Aşama: Değerlendirme
r2 = r2_score(y_test, y_pred) # Gerçek cevaplar (y_test) ve makinenin tahmin ettiği cevaplar (y_pred) arasındaki başarı oranı
mse = mean_squared_error(y_test, y_pred)

print("Modelin r2 skoru: ", r2)
print(f"Modelin MSE değeri : {mse : .2f}")

#6. Aşama : Deployment

new_customer = pd. DataFrame([[25,30,1,0,0,1,0,0]], columns = X_train.columns)

new_customer_predicton = model.predict(new_customer)

print("Tahmini sigorta police değeriniz: ", new_customer_predicton)

#r2 skorunu arttırmak için yeni kolonlar ekliyoruz.

df_encoded_new = pd.get_dummies(df,columns=["sex","smoker","region"], drop_first=True)

df_encoded_new['bmi_smoker'] = df_encoded_new['bmi'] * df_encoded_new["smoker_yes"]

df_encoded_new['is_obese'] = df_encoded_new['bmi'].apply(lambda x:1 if x>30 else 0)

X_new = df_encoded_new.drop('charges', axis = 1)
y_new = df_encoded_new['charges']

X_train_new, X_test_new, y_train_new, y_test_new = train_test_split(X_new, y_new, test_size=0.2)

# 4. Model Geliştirme

model_new = LinearRegression()
#Eğitmek için LinearRegression sınıfındaki fit fonksiyonu kullanılır.
#X_train ve y_train gönderilir çünkü eğitim için o datalar tercih edildi.
model_new.fit(X_train_new, y_train_new) #OOP gereği, LinearRegression sınıfını model'e atama yaptığımız için özelliklerini kullanabiliriz.
y_pred_new = model_new.predict(X_test_new) #cevabını bilmediği soruları sormak istiyoruz, o yüzden X_test gönderilir. Tahmin yaptırmış oluyoruz. Tahmin göndereceğinden atama yapmamız gerek.

# 5. Aşama: Değerlendirme
r2_new = r2_score(y_test_new, y_pred_new) # Gerçek cevaplar (y_test) ve makinenin tahmin ettiği cevaplar (y_pred) arasındaki başarı oranı
mse_new = mean_squared_error(y_test_new, y_pred_new)