#API'ye Python'dan istek atmak
#API: Farklı yazılımlar arasındaki iletişimi hızlı bir şekilde sağlamak
#API'ler aracılığıyla farklı hizmetler birbiriyle konuşur.
#İlk önce Python’da bir yere istek atmak için kullanacağımız kütüphane requests kütüphanesidir.
#requests kütüphanesi, örneğin google’a Instagram yazıp enter’a bastığımızda bunu Python’da yapmamızı sağlar.

#Veri Alma (get methodu)

import requests
import pandas as pd
api_url = "https://jsonplaceholder.typicode.com/users"
#API’den Pyhon’a veri dönerse buna get denir.
#Python’dan API’ye istek atılabilir, buna post denir.
#Bu kodu çalıştırmak tarayıcıda aradığımız şeyi yazıp enter'a basmaktır.
#timeout, entera bastıktan sonra eğer site meşgulse beklemedeysek sonuna kadar beklemeyelim diye koyduk.
response = requests.get(api_url, timeout=10)
#200, URL'de issteğin başarılı döndüğü anlamına gelir.
print(response.status_code)
if response.status_code == 200:
    print("Başarıyla okundu", response.status_code)
    response_data = response.json() # response'dan dönen json datası neyse onu yazacak.
else:
    print("İstek başarısız, hata kodu da budur: ",response.status_code)

#Kolon içinde kolon varsa bu tür datalara denormalize data denir.
response_df = pd.DataFrame(response_data) #adress kolonu içinde bir sürü kolon var.
#Normalize etme
normalize_df = pd.json_normalize(response_data)
#Data frame'den excel'e dönüştürme
response_df.to_excel("response_df.xlsx", index=False)
normalize_df.to_excel("normalize_df.xlsx", index=False)

#Veri Gönderme (post methodu)

post_url = "https://jsonplaceholder.typicode.com/posts"

ogrenci = {
    "Ad":"Ali",
    "Yas": 30
    }

post_response = requests.post(post_url,json=ogrenci)

if post_response.status_code == 201: #Post başarlısı ise 201 döner, get 200 döner
    print("Veri insert edildi.")
else:
    print("Veri gönderilmedi, hata kodu: ",post_response.status_code)
    
#WEB Scrapping --> URL'e istek atmak (üstteki gibi)
#Burada da istek atma durumu vardır. 
#API'ye istek atarsak JSON döner, WEB'e istek atarsak başka şey döner. (HTML)
#Bu sefer dönecek şey hazır bir şekilde okunacak data değil(json olmayacak), websitesi olduğundan HTML, CSS, JS kodu dönecek.

from bs4 import BeautifulSoup #dönen datayı parse etmeye yarar.

url = "https://quotes.toscrape.com/"

response_web = requests.get(url)

if response_web.status_code == 200:
    soup = BeautifulSoup(response_web.content,"html.parser") #html kodlarını kod türünde almaya yarar. Yani HTML kodları parse edilebilir şekilde tutulur.
    sayfa_basligi = soup.find("h1").text #Bulduğu h1 taginin içerisindeki text değerini istiyoruz. Sayfanın başlığını okumuş olduk, en temeli. Find fonksiyonu ilk gördüğünü okur.
    sayfa_linki_style = soup.find("h1").find("a") #HTML kodundaki h1 içerisindeki a bulundu.
    sayfa_linki_style["style"] #h1 içerisindeki a içerisindeki style bulundu.
else:
    print("Siteye erişilemedi.")

divs = soup.find_all("div", class_ = "quote") #Soupta bir veriyi find ile okuduk, birden fazla veriyi ise find_all ile okuruz. Amacımız sözü ve sözü söyleyeni okumak olduğu için sadece bu kutucukları alacağımızdan HTML kodunda class'ı quote olanları aldık.

veri_listesi = []

#Söz ve sözü söyleyen 10 tane divimiz var, hepsini tek tek for döngüsü ile gezeceğiz.
for div in divs:
    soz = div.find("span",class_ = "text").text #spani seçip, text değerini okumasını söyledik.
    soyleyen = div.find("small", class_ = "author").text
    veri_listesi.append({"Yazar":soyleyen,"Soz":soz})
    
#Oluştuduğumuz liste dictionary formunda. Biz dataframe şekline döndüreceğiz.
df_sozler = pd.DataFrame(veri_listesi)



#Pagination --> Web sitesinde ilk girdiğimiz sayfada okumak istediğimiz tüm veriler olmayabilir, birden fazla sayfa olabilir.

#Sayfa değiştirdikçe URL değişiyor, her sayfa için istek atacağız.

import time

tum_sayfalar_verisi = []

page_url = "http://quotes.toscrape.com/page/"

for i in range(1,5):
    
    istek_url = f"{page_url}{i}"
    #time.sleep(10) #Siteye art arda istek atıldığında ban yememek için buna delay denir.
    #print(istek_url)
    r = requests.get(istek_url) #istek atıldı.
    s = BeautifulSoup(r.content,"html.parser") #istek beautifulsoup'a döndü. s içindeki HTML kodlarını parse edeceğiz.
    
    sayfa_divs = s.find_all("div", class_ = "quote") # s den tüm divler okunacak.
    
    for sd in sayfa_divs: #Önceki for döngüsü ile aynı kodlar.
        sayfa_soz = sd.find("span", class_="text").text
        sayfa_soyleyen = sd.find("small", class_ = "author").text
        tum_sayfalar_verisi.append({"Yazar":soyleyen,"Soz":soz})

#Bu sefer İBB sitesi ziyaretinde sayfa değiştridkçe URL değişmediğini gözlemleriz. Önceki örnekte sayfa değiştikçe URL değişiyordu. Bu sitenin arkasında JS var.
#Yani Pagination var ama URL değişmiyor, arayüz aracılığıyla sayfalar arasında gezebiliyoruz. Artık başka bir kütüphaneye ihtiyaç var.
#Selenium kütüphanesi sayesinde istek attığımızda kullanıcı sanki tarayıcıda geziyormuş gibi davranmamızı sağlar. Bu sayede tarayıcıda gezerken yaptığımız her şeyi Python içerisinden yapabiliriz.


ibb = "https://ibb.istanbul/gundem/duyurular" #istek atacağımız sayfa


#Bizi ibb sitesine götüren bir içerik olacak, o içeriğin başlığında "header" denilen bölmede bu isteğin Chrome,Opera,Safari'den geldiğini söyleyen bölüm olur. Bu istek sana bir tarayıcıdan geliyor demektir.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


response_ibb = requests.get(ibb,headers=headers)

if response_ibb.status_code == 200:
    ibb_soup = BeautifulSoup(response_ibb.content, "html.parser") # ibb'nin html kodları oluşturuldu.
    time.sleep(10)

#Diğer işlemler de aynı şekilde olacak. Buradaki fark headers bölümüydü.