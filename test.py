def scale_value(value, old_min, old_max, new_min, new_max):
    old_range = old_max - old_min
    new_range = new_max - new_min
    scaled_value = (((value - old_min) * new_range) / old_range) + new_min
    return scaled_value

value = 421
old_min = 0     # Eski aralığın minimum değeri
old_max = 1023  # Eski aralığın maksimum değeri
new_min = 5     # Yeni aralığın minimum değeri
new_max = 20    # Yeni aralığın maksimum değeri

scaled_value = scale_value(value, old_min, old_max, new_min, new_max)
print(f"{value} sayısının 5 ile 20 arasındaki karşılığı: {scaled_value}")
