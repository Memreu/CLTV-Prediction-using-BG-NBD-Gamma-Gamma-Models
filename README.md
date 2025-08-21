# 📌 BG-NBD ve Gamma-Gamma ile CLTV Prediction

## 💼 İş Problemi (Business Problem)

FLO satış ve pazarlama faaliyetleri için orta ve uzun vadeli bir yol
haritası belirlemek istemektedir.\
Bunun için mevcut müşterilerin gelecekte şirkete sağlayacakları
potansiyel değerin (CLTV) tahmin edilmesi gerekmektedir.

------------------------------------------------------------------------

## 📊 Veri Seti Hikayesi

Veri seti, son alışverişlerini 2020 - 2021 yıllarında **OmniChannel**
(hem online hem offline alışveriş yapan) olarak yapan müşterilerin
geçmiş alışveriş davranışlarından elde edilen bilgilerden oluşmaktadır.

**Değişkenler:** - `master_id` : Eşsiz müşteri numarası\
- `order_channel` : Alışveriş yapılan kanal (Android, iOS, Desktop,
Mobile, Offline)\
- `last_order_channel` : En son alışverişin yapıldığı kanal\
- `first_order_date` : Müşterinin yaptığı ilk alışveriş tarihi\
- `last_order_date` : Müşterinin yaptığı son alışveriş tarihi\
- `last_order_date_online` : Online platformdaki son alışveriş tarihi\
- `last_order_date_offline` : Offline platformdaki son alışveriş tarihi\
- `order_num_total_ever_online` : Online toplam alışveriş sayısı\
- `order_num_total_ever_offline` : Offline toplam alışveriş sayısı\
- `customer_value_total_ever_online` : Online toplam harcama\
- `customer_value_total_ever_offline` : Offline toplam harcama\
- `interested_in_categories_12` : Son 12 ayda alışveriş yapılan
kategoriler listesi

------------------------------------------------------------------------

## ⚙️ Kurulum

1.  Gerekli kütüphaneleri yükleyin:

``` bash
pip install pandas numpy lifetimes matplotlib seaborn jupyter
```

2.  Projeyi indirin veya klonlayın:

``` bash
git clone https://github.com/kullanici/cltv-prediction.git
cd cltv-prediction
```

3.  Jupyter Notebook ortamında açın:

``` bash
jupyter notebook Flo.ipynb
```

------------------------------------------------------------------------

## ▶️ Kullanım

1.  `Flo.ipynb` dosyasını Jupyter Notebook ile açın.\
2.  Kod hücrelerini sırasıyla çalıştırarak veri ön işleme, modelleme ve
    tahmin aşamalarını inceleyin.\
3.  Kendi veri setinizi kullanmak için Notebook içindeki **veri yükleme
    kısmını** değiştirin.

Örnek kod parçası:

``` python
import pandas as pd

df = pd.read_csv("data.csv")
# CLTV analizi adımları burada çalıştırılır
```

------------------------------------------------------------------------

## 🌟 Özellikler

-   📊 BG-NBD ve Gamma-Gamma modelleri ile CLTV tahmini\
-   🔍 Müşteri bazlı değer analizi\
-   📈 Görselleştirme desteği (Matplotlib / Seaborn)\
-   🛠 Jupyter Notebook ortamında adım adım çalıştırılabilir\
-   🔗 Farklı veri setlerine kolay uyarlanabilir\
-   📑 CLTV bazlı segment oluşturma ve raporlama

------------------------------------------------------------------------

## 📊 Çıktılar

-   Her müşteri için beklenen satın alma sayısı ve tahmini gelir\
-   CLTV skorlarının hesaplanması ve sıralanması\
-   Segment bazlı müşteri değer dağılımı ve görselleştirme

Örnek görselleştirme:

``` python
import seaborn as sns
import matplotlib.pyplot as plt

sns.histplot(cltv_df["cltv"])
plt.title("Müşteri CLTV Dağılımı")
plt.show()
```

------------------------------------------------------------------------

## 📈 Çalışma Akışı

``` mermaid
flowchart TD
    A[Veri Yükleme] --> B[Veri Ön İşleme]
    B --> C[BG-NBD Modeli ile Beklenen Satın Alma]
    C --> D[Gamma-Gamma Modeli ile Ortalama Harcama]
    D --> E[CLTV Hesaplama]
    E --> F[Segmentasyon ve Raporlama]
```
