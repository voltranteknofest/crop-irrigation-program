# Bilimsel Prensipler Işığında Sulama İhtiyaçlarının  Optimizasyonu

Bu repo, 2024 yılının tarım teknolojileri kapsamındaki teknofest yarışması için hazırlanmıştır. Projemize ait orijinal makalenin linki: (yüklenecek)

## Projenin Şematik Görünümü

![image](https://github.com/user-attachments/assets/5f3f5590-15d8-42fd-ac73-4d6a9ab284f4)

### Bahçe Düzeyinde Sensör Tabanlı Sulamaya Dair Örnek Görüntü

![image](https://github.com/user-attachments/assets/511c4666-15f4-4ca5-8304-0c36dad35cdb)

### Veri toplayan tarım robotu prototip:

![tarim_robotu](https://github.com/user-attachments/assets/d49b5342-98e1-4288-8ba5-7c9816592f87)

### Basit devre düzeyinde vana sistemi prototip:
(yüklenecek)

## Penmann-Monteith Denklemi

Penman-Monteith denklemi, mahsullerin referans evapotranspirasyon ($ET0$) değerini hesaplamak için kullanılır. Bu değeri mahsulün türü ve yetişme dönemine göre belirlenen mahsul katsayısı ($Kc$) ile çarpmak bize o mahsulün net evapotranspirasyon değerini verir.

$ET_0 = \frac{0.408 \Delta (R_n - G) + \frac{900}{T + 273} \gamma u_2 \delta e}{\Delta + \gamma (1 + 0.34 u_2)}$

$Kc=1.15$; varsaydığımız durumda net evapotranspirasyon: $ETc= ET0 \times Kc$; olarak hesaplanır. Bu işlemin sonucunda bir bitkinin günde $ET0$ kadar milimetre su kaybına uğradığı hesabını yapmış oluruz.

## Fiziksel Sulama Prensipleri

![soil-resevoir-components](https://github.com/user-attachments/assets/1046fbe3-8906-4c77-b64b-e54c7e99bc06)

---

![plant-soil-water-relations](https://github.com/user-attachments/assets/cfbc174e-c9a7-4ac2-a7b0-c85b8d5b813e)

## Matematiksel ve Fiziksel Prensiplerin Programlanması

```python
# irrigationtools/utils.py

import math
from .consts import CROP_MAPPING

def calc_saturation_vapor_pressure(T):
    """
    Belirli bir sıcaklık (T) için doymuş buhar basıncını (es) hesaplar.
    """
    return 0.6108 * math.exp((17.27 * T) / (T + 237.3))

def calc_actual_vapor_pressure(es, RH):
    """
    Doymuş buhar basıncı (es) ve bağıl nem (RH) değerlerine göre gerçek buhar basıncını (ea) hesaplar.
    """
    return RH * es

def calc_ref_evapotranspiration(R_n, G, T, u2, es, ea, altitude):
    """
    Penman-Monteith denklemini kullanarak referans evapotranspirasyonu (ET0) hesaplar.
    """

    # denklem sabitleri
    cp = 1.013 * 10**-3  # MJ/kg/°C
    lambda_ = 2.45       # MJ/kg
    epsilon = 0.622

    # atmosfer basıncını (P) kPa cinsinden hesaplar
    P = 101.3 * ((293 - 0.0065 * altitude) / 293)**5.26

    # psikrometrik sabiti (gamma) kPa/°C cinsinden hesaplar
    gamma = cp * P / (epsilon * lambda_)

    # doymuş buhar basıncı eğrisinin eğimi (delta) kPa/°C cinsinden hesaplar
    delta = (4098 * (0.6108 * math.exp((17.27 * T) / (T + 237.3)))) / ((T + 237.3) ** 2)

    # referans evapotranspirasyonu (ET0) mm/gün cinsinden hesaplar
    ET0 = (0.408 * delta * (R_n - G) + gamma * (900 / (T + 273)) * u2 * (es - ea)) / (delta + gamma * (1 + 0.34 * u2))

    return ET0

def get_crop_coefficient(crop_type, growth_season):
    return CROP_MAPPING[crop_type][growth_season]

def calc_crop_evapotranspiration(ET0, Kc):
    """
    Referans evapotranspirasyon (ET0) ve mahsul katsayısı (Kc) değerlerine göre 
    mahsule özgü evapotranspirasyonu (ETc) hesaplar.
    """
    # mm/gün
    ETc = ET0 * Kc
    return ETc

def calc_soil_props(moisture, field_capacity, wilting_point):
    """
    Toprak nemini günceller ve drenajı hesaplar.
    Toprak neminin güncellenmesi suyun bazen tarla kapasitesinin dahi
    üstünde olabileceği nedeniyle gereklidir. 200 milimetrelik bir tarla kapasitesinde
    250 milimetrelik bir su birikiminden söz ediyorsak bu nemin aslında 200 milimetre olduğunu,
    kalan 50 milimetrenin ise derinlerde kaybolduğu, yani drenaj anlamına gelir.
    """
    
    if moisture > field_capacity:
        deep_percolation = moisture - field_capacity
        moisture = field_capacity
    else:
        deep_percolation = 0

    if moisture < wilting_point:
        moisture = wilting_point

    return moisture, deep_percolation

def calc_irrigation_need(moisture, ETc, field_capacity, wilting_point, MAD):
    """
    Sulama ihtiyacını ve bir sonraki sulamaya kadar olan gün sayısını hesaplar.
    """
    
    available_water      = field_capacity - wilting_point
    irrigation_threshold = wilting_point + available_water * (1 - MAD)
    irrigation_needed    = 0
    days                 = 0
    
    if moisture <= irrigation_threshold:
        irrigation_needed = field_capacity - moisture
        return irrigation_needed, days
    
    while moisture > irrigation_threshold:
        moisture -= ETc
        days += 1
    return irrigation_needed, days
```

## Örnek Sonuç

![image](https://github.com/user-attachments/assets/0fec580a-b33c-4984-87b8-ee9c7833e3f6)

Tabloda bulunmayan rakım **50m**, rüzgar hızı **2.8 m/s**, net radyasyon **18 MJ/m²**, toprak ısı akısı (G) **0**, tarla kapasitesi (FC) **160mm**, solma noktası (WP) **40mm’de** sabittir. Sıcaklık, bağıl nem, toprak nemi ve MAD değerlerine tabloda değişken olarak yer verilmiştir. Programda sıcaklık ve bağıl nemin değişkenliğine bağlı olarak evapotranspirasyon çıktısı, toprak nemi ve MAD eşiğinin değişkenliğine bağlı olarak zaman ve gereken sulamanın çıktısı hesaplanmış ve tabloda sunulmuştur.

## Matematiksel Olarak Bir Vanadan Saniyede ne kadar Su Akacağını Hesaplamak

Bu, projemizin hayata geçirildiği aşamada önem taşıyacak bir bilgidir. Teknofest'te canlı bir şekilde sunum yaparken göstermek amaçlı burada bulunuyor.

### Temel Akış Hızı Formülü
Akış hızı `Q` birimi `hacim/saniye` (örneğin, `litre/saniye`) olarak ifade edilir ve aşağıdaki şekilde hesaplanır:

$Q = A \times v$;

Burada:
- $Q$ : Akış hızı ($m^3/s$ veya $L/s$)
- $A$ : Borunun kesit alanı ($m^2$)
- $v$ : Sıvının hızı ($m/s$)

### Boru Kesit Alanı
Borunun kesit alanı, borunun çapına bağlı olarak aşağıdaki formülle hesaplanır:

$A = \pi \times \left(\frac{d}{2}\right)^2$;

Burada:
- $A$ : Borunun kesit alanı ($m^2$)
- $d$ : Borunun iç çapı ($m$)
- $\pi$ : Yaklaşık olarak $3.14159$

### Akış Hızı ($v$)
Akış hızı, basınca ve sıvının yoğunluğuna bağlı olarak aşağıdaki formülle hesaplanabilir:

$v = \sqrt{\frac{2 \times \Delta P}{\rho}}$;

Burada:
- $v$ : Sıvının hızı ($m/s$)
- $\Delta P$ : Basınç farkı ($Pa$)
- $\rho$ : Sıvının yoğunluğu ($kg/m^3$)

Su için yoğunluk ($\rho$) genellikle 1000 $kg/m^3$ olarak alınır.

### Akış Miktarının Hesaplanması
Belirli bir süre boyunca akacak su miktarı ($V$) aşağıdaki formülle hesaplanır:

$V = Q \times t$;

Burada:
- $V$ : Akacak toplam su hacmi ($m^3$ veya $L$)
- $Q$ : Akış hızı ($m^3/s$ veya $L/s$)
- $t$ : Akış süresi (saniye)

### Genel Formül
Eğer tüm parametreler biliniyorsa boru çapı ve basınç farkına bağlı olarak belirli bir sürede akacak su miktarını hesaplamak için:

$V = \left(\pi \times \left(\frac{d}{2}\right)^2 \times \sqrt{\frac{2 \times \Delta P}{\rho}}\right) \times t$

Bu formül, bir vanadan ne kadar su akacağını hesaplamak için temel matematiksel denklemdir. Daha karmaşık durumlar için akışkan dinamiği prensipleri, kayıplar, sürtünme faktörleri gibi diğer faktörler de göz önüne alınmalıdır.