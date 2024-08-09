## Projenin Şematik Görünümü

![image](https://github.com/user-attachments/assets/5f3f5590-15d8-42fd-ac73-4d6a9ab284f4)

### Veri toplayan tarım robotu prototip:

![tarim_robotu](https://github.com/user-attachments/assets/d49b5342-98e1-4288-8ba5-7c9816592f87)

## Penmann-Monteith Denklemi

Penman-Monteith denklemi, mahsullerin referans evapotranspirasyon ($ET0$) değerini hesaplamak için kullanılır. Bu değeri mahsulün türü ve yetişme dönemine göre belirlenen mahsul katsayısı ($Kc$) ile çarpmak bize o mahsulün net evapotranspirasyon değerini verir.

$ET_0 = \frac{0.408 \Delta (R_n - G) + \frac{900}{T + 273} \gamma u_2 \delta e}{\Delta + \gamma (1 + 0.34 u_2)}$

$Kc=1.15$; varsaydığımız durumda net evapotranspirasyon: $ETc= ET0 \times Kc$; olarak hesaplanır. Bu işlemin sonucunda bir bitkinin günde $ET0$ kadar milimetre su kaybına uğradığı hesabını yapmış oluruz.

## Fiziksel Sulama Prensipleri

![soil-resevoir-components](https://github.com/user-attachments/assets/1046fbe3-8906-4c77-b64b-e54c7e99bc06)

---

![plant-soil-water-relations](https://github.com/user-attachments/assets/cfbc174e-c9a7-4ac2-a7b0-c85b8d5b813e)

## Matematiksel Olarak Bir Vanadan Saniyede ne kadar Su Akacağını Hesaplamak

### Temel Akış Hızı Formülü
Akış hızı `Q` birimi `hacim/saniye` (örneğin, `litre/saniye`) olarak ifade edilir ve şu şekilde hesaplanır:

$Q = A \times v$;

Burada:
- $Q$ : Akış hızı ($m^3/s$ veya $L/s$)
- $A$ : Borunun kesit alanı ($m^2$)
- $v$ : Sıvının hızı ($m/s$)

### Boru Kesit Alanı
Borunun kesit alanı, borunun çapına bağlı olarak şu formülle hesaplanır:

$A = \pi \times \left(\frac{d}{2}\right)^2$;

Burada:
- $A$ : Borunun kesit alanı ($m^2$)
- $d$ : Borunun iç çapı ($m$)
- $\pi$ : Yaklaşık olarak $3.14159$

### Akış Hızı ($v$)
Akış hızı, basınca ve sıvının yoğunluğuna bağlı olarak şu formülle hesaplanabilir:

$v = \sqrt{\frac{2 \times \Delta P}{\rho}}$;

Burada:
- $v$ : Sıvının hızı ($m/s$)
- $\Delta P$ : Basınç farkı ($Pa$)
- $\rho$ : Sıvının yoğunluğu ($kg/m^3$)

Su için yoğunluk ($\rho$) genellikle 1000 $kg/m^3$ olarak alınır.

### Akış Miktarının Hesaplanması
Belirli bir süre boyunca akacak su miktarı ($V$) şu formülle hesaplanır:

$V = Q \times t$;

Burada:
- $V$ : Akacak toplam su hacmi ($m^3$ veya $L$)
- $Q$ : Akış hızı ($m^3/s$ veya $L/s$)
- $t$ : Akış süresi (saniye)

### Özet Formül
Eğer tüm parametreler biliniyorsa, boru çapı ve basınç farkına bağlı olarak belirli bir sürede akacak su miktarını hesaplamak için kullanılabilecek genel formül:

$V = \left(\pi \times \left(\frac{d}{2}\right)^2 \times \sqrt{\frac{2 \times \Delta P}{\rho}}\right) \times t$

Bu formül, bir vanadan ne kadar su akacağını hesaplamak için temel matematiksel denklemdir.