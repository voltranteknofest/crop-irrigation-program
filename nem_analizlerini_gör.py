from irrigationtools import get_results_all, calc_average_moisture_for_result


FIELD_CAPACITY = 160
WILTING_POINT  = 40
SENSOR_MIN     = 0
SENSOR_MAX     = 1023


def scale_value(value, old_min, old_max, new_min, new_max):
    old_range = old_max - old_min
    new_range = new_max - new_min
    scaled_value = (((value - old_min) * new_range) / old_range) + new_min
    return scaled_value


if __name__ == '__main__':
    get_results_all()
    
    print("=>> Veritabaninin okunabilir versiyonu db/results.txt dosyasina yazildi.", end="\n\n")
    print("=>> Ornek bölgesel nem ortalamalari:")
    
    overall_moisture_average__tomatoes = calc_average_moisture_for_result("tomato")
    print(f"Tarladaki domateslerin nem ortalamalari: {overall_moisture_average__tomatoes} mm", end="\n\n")
    
    overall_moisture_average__potatoes = calc_average_moisture_for_result("potato")
    print(f"Tarladaki patateslerin nem ortalamalari: {overall_moisture_average__potatoes} mm", end="\n\n")
    
    overall_moisture_average__carrots = calc_average_moisture_for_result("carrot")
    print(f"Tarladaki havuçlarin nem ortalamalari: {overall_moisture_average__carrots} mm", end="\n\n")
    
    overall_moisture_average__corns = calc_average_moisture_for_result("corn")
    print(f"Tarladaki misirlarin nem ortalamalari: {overall_moisture_average__corns} mm", end="\n\n")
    
    print("Milimetrik nem verilerinin nem sensoru verisine olarak gorunumu:")
#                                                                         40              160            0           1023
    sensorized_tomatoes = scale_value(overall_moisture_average__tomatoes, WILTING_POINT, FIELD_CAPACITY, SENSOR_MIN, SENSOR_MAX)
    print(f"Domateslerin nem sensorundeki karsiligi: {int(sensorized_tomatoes)}")
    
    sensorized_potatoes = scale_value(overall_moisture_average__potatoes, WILTING_POINT, FIELD_CAPACITY, SENSOR_MIN, SENSOR_MAX)
    print(f"Patateslerin nem sensorundeki karsiligi: {int(sensorized_potatoes)}")

    sensorized_carrots = scale_value(overall_moisture_average__carrots,   WILTING_POINT, FIELD_CAPACITY, SENSOR_MIN, SENSOR_MAX)
    print(f"Havuclarin   nem sensorundeki karsiligi: {int(sensorized_carrots)}")
    
    sensorized_corns = scale_value(overall_moisture_average__corns,       WILTING_POINT, FIELD_CAPACITY, SENSOR_MIN, SENSOR_MAX)
    print(f"Misirlarin   nem sensorundeki karsiligi: {int(sensorized_corns)}")