from irrigationtools import get_results_all, calc_average_moisture_for_result

if __name__ == '__main__':
    get_results_all()
    
    print("db/results.txt dosyasına göz atınız")
    
    print('\n', end='')
    
    overall_moisture_average__tomatoes = calc_average_moisture_for_result("tomato")
    print("Tarladaki domateslerin nem ortalamaları:", overall_moisture_average__tomatoes, end="\n\n")
    
    overall_moisture_average__tomatoes = calc_average_moisture_for_result("potato")
    print("Tarladaki patateslerin nem ortalamaları:", overall_moisture_average__tomatoes, end="\n\n")
    
    overall_moisture_average__carrots = calc_average_moisture_for_result("carrot")
    print("Tarladaki havuçlarin nem ortalamaları:", overall_moisture_average__carrots, end="\n\n")
    
    overall_moisture_average__corns = calc_average_moisture_for_result("corn")
    print("Tarladaki misirlarin nem ortalamaları:", overall_moisture_average__corns, end="\n\n")