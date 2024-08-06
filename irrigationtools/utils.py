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
