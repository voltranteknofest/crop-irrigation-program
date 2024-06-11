from irrigationtools import get_results_all, calc_median_moisture_for_result

if __name__ == '__main__':
    get_results_all()
    
    print("See db/results.txt")
    
    print('\n', end='')
    
    overall_moisture_median__tomatoes = calc_median_moisture_for_result("tomato")
    print("Moisture median for tomatoes:", overall_moisture_median__tomatoes)
    
    overall_moisture_median__tomatoes = calc_median_moisture_for_result("potato")
    print("Moisture median for potatoes:", overall_moisture_median__tomatoes)