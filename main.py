from irrigationtools import (
    calc_ref_evapotranspiration,
    calc_crop_evapotranspiration,
    calc_saturation_vapor_pressure,
    calc_actual_vapor_pressure,
    calc_soil_props,
    calc_irrigation_need,
    get_crop_coefficient,
    save_to_sqlite,
)

def main():
    crop_type          = "corn"               # mahsul çeşidi (havuç, patates...)
    crop_growth_season = "mid-season"           # mahsul yetişme sezonu (orta sezon...)
    
    # penman-monteith equation (math)
    altitude = 50                                                  # rakım                      (metre cinsinden)
    T        = 24                                                  # sıcaklık                   (°C cinsinden)
    u2       = 2.8                                                 # rüzgar hızı                (2 metre yükseklikte m/s cinsinden)
    RH       = 56/100                                              # bağıl nem                  (% cinsinden)
    R_n      = 18                                                  # net radyasyon              (MJ/m²/gün cinsinden)
    G        = 0                                                   # toprak ısı akısı yoğunluğu (MJ/m²/gün cinsinden)
    Kc       = get_crop_coefficient(crop_type, crop_growth_season) # mahsul katsayısı           (1, 1.12, 0.9 vb.)
    
    es = calc_saturation_vapor_pressure(T)  # doymuş buhar basıncı hesaplaması
    ea = calc_actual_vapor_pressure(es, RH) # gerçek buhar basıncı hesaplaması

    ET0 = calc_ref_evapotranspiration(R_n, G, T, u2, es, ea, altitude) # referans evapotranspiration
    ETc = calc_crop_evapotranspiration(ET0, Kc)                        # mahsul evapotranspiration

    # (physical evaluations)
    MAD              = 0.5   # izin verilen maksimum nem azalması (örn: %50 için 0.5 giriniz)
    field_capacity   = 160   # tarla kapasitesi                   (mm cinsinden)
    wilting_point    = 40    # solma noktası                      (mm cinsinden)
    moisture         = 91.54    # toprak nemi                        (mm cinsinden)
    
    # topraktaki nem durumu ve drenajın hesaplanması
    moisture, deep_percolation = calc_soil_props(moisture, field_capacity, wilting_point)
    
    # ihtiyaç duyulan su miktarı ve ihtiyaç yok ise kaç gün sonra ihtiyaç olacağının hesaplanması
    amount, days = calc_irrigation_need(moisture, ETc, field_capacity, wilting_point, MAD)
    
    print(
        f"""
        
        Referans evapotranspirasyon (ET0): {ET0:.2f} mm/day
        Mahsul evapotranspriasyonu  (ETc): {ETc:.2f} mm/day
        Derin drenaj: {deep_percolation:.2f} mm

        Toprak nemi: {moisture:.2f} mm
        Gerekli sulama: {amount:.2f} mm
        Gün: {days}
        
        """
    )
    
    # veri tabanına kaydetmek
    save_to_sqlite(crop_type, altitude, T, u2, RH, R_n, G, Kc, ET0, ETc, moisture, deep_percolation, amount, days)


if __name__ == '__main__':
    main()
