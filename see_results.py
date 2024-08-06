from irrigationtools import get_results_all, calc_average_moisture_for_result

if __name__ == '__main__':
    get_results_all()
    
    print("db/results.txt dosyasına göz atınız")
    
    print('\n', end='')
    
    overall_moisture_average__tomatoes = calc_average_moisture_for_result("tomato")
    print("Tarladaki domateslerin nem ortalamaları:", overall_moisture_average__tomatoes)
    
    overall_moisture_average__tomatoes = calc_average_moisture_for_result("potato")
    print("Tarladaki patateslerin nem ortalamaları:", overall_moisture_average__tomatoes)