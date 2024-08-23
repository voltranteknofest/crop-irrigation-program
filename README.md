# Bilimsel Prensipler Işığında Sulama İhtiyaçlarının  Optimizasyonu

Bu repo, 2024 yılının tarım teknolojileri kapsamındaki teknofest yarışması için hazırlanmıştır. Projemize ait orijinal makalenin linki: (yüklenecek)

## Projenin Şematik Görünümü

![image](https://github.com/user-attachments/assets/5f3f5590-15d8-42fd-ac73-4d6a9ab284f4)

Üç temel soru:
1. Veri toplama (mahsullerin su ihtiyacını hesaplama) görevi nasıl gerçekleştirilecek?
2. Toplanan veriler nasıl iletilecek?
3. Vana sistemi nasıl çalışacak?

### Bahçe Düzeyinde Sensör Tabanlı Sulamaya Dair Örnek Görüntü

![image](https://github.com/user-attachments/assets/511c4666-15f4-4ca5-8304-0c36dad35cdb)

## Penmann-Monteith Denklemi

Penman-Monteith denklemi, mahsullerin referans evapotranspirasyon ($ET0$) değerini hesaplamak için kullanılır. Bu değeri mahsulün türü ve yetişme dönemine göre belirlenen mahsul katsayısı ($Kc$) ile çarpmak bize o mahsulün net evapotranspirasyon değerini verir.

$ET_0 = \frac{0.408 \Delta (R_n - G) + \frac{900}{T + 273} \gamma u_2 \delta e}{\Delta + \gamma (1 + 0.34 u_2)}$

$Kc=1.15$; varsaydığımız durumda net evapotranspirasyon: $ETc= ET0 \times Kc$; olarak hesaplanır. Bu işlemin sonucunda bir bitkinin günde $ET0$ kadar milimetre su kaybına uğradığı hesabını yapmış oluruz.

## Fiziksel Sulama Prensipleri

![soil-resevoir-components](https://github.com/user-attachments/assets/1046fbe3-8906-4c77-b64b-e54c7e99bc06)

---

![image](https://github.com/user-attachments/assets/caaa74c6-3340-4470-b6b9-dc89bd3a7212)

## Canlı Sunum Performansı

### Matematiksel Olarak Bir Vanadan Saniyede ne kadar Su Akacağını Hesaplamak

#### Genel Formül
Boru çapı ve basınç farkına bağlı olarak belirli bir sürede akacak su miktarını hesaplamak için:

$V = \left(\pi \times \left(\frac{d}{2}\right)^2 \times \sqrt{\frac{2 \times \Delta P}{\rho}}\right) \times t$

Bu formül, bir vanadan ne kadar su akacağını hesaplamak için temel matematiksel denklemdir. Daha karmaşık durumlar için akışkan dinamiği prensipleri, kayıplar, sürtünme faktörleri gibi diğer faktörler de göz önüne alınmalıdır.

### Birden Fazla Vana Kullanımının Avantajları

* Bölgesel Sulama Kontrolü => Ürün çeşitliğiline yönelik oluşacak mahsul katsayısı farklılıklarını sulama ihtiyacında hesaba katmak için kontrol sağlar
* Sistem Arızaları ve Bakım => Farklı vanalar kullanıldığında, bir vanada sorun çıktığında tüm tarlanın sulama sistemi etkilenmez. 
* Esneklik ve Özelleştirme => Gelecekte tarlaya yeni mahsul eklemek isterseniz, zaten mevcut olan vana sistemi ile bu bölgeyi kolayca entegre edebilirsiniz.

### Robotun GPS Tabanlı Rotasyonu
https://www.sciencedirect.com/science/article/pii/S1110016818301091

![image](https://github.com/user-attachments/assets/a8cb7e29-1196-4ade-9949-20fb7c828fed)

