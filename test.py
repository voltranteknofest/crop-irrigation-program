from enum import Enum


def scale_value(value, old_min, old_max, new_min, new_max):
    old_range = old_max - old_min
    new_range = new_max - new_min
    scaled_value = (((value - old_min) * new_range) / old_range) + new_min
    return scaled_value


class Button(Enum):
    AREA_1 = ("Nem Ölç Bölge 1", 0)
    AREA_2 = ("Nem Ölç Bölge 2", 1)
    AREA_3 = ("Nem Ölç Bölge 3", 2)
    AREA_4 = ("Nem Ölç Bölge 4", 3)

    def __init__(self, label, relay_index):
        self.label = label
        self.relay_index = relay_index


if __name__ == '__main__':
    value = 921
    old_min = 0     # Eski aralığın minimum değeri
    old_max = 1023  # Eski aralığın maksimum değeri
    new_min = 5     # Yeni aralığın minimum değeri
    new_max = 20    # Yeni aralığın maksimum değeri

    scaled_value = scale_value(value, old_min, old_max, new_min, new_max)
    print(f"{value} sayısının 5 ile 20 arasındaki karşılığı: {scaled_value}")
    
    print("----------------")

    for btn in Button:
        print(btn)
        print(btn.label)
        print(btn.relay_index)
