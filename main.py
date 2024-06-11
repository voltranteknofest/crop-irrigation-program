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
    crop_type          = "tomato"               #input("Enter crop type (e.g., carrot, potato): ")
    crop_growth_season = "mid-season"           #input("Enter crop growth season (e.g., late-season, init-season): ")
    
    # penman-monteith params
    altitude = 50                               #float(input("Enter altitude of the location in meters: "))
    T        = 24                               #float(input("Enter mean daily air temperature (T) in °C: "))
    u2       = 2.8                              #float(input("Enter wind speed at 2 m height (u2) in m/s: "))
    RH       = 56/100                           #float(input("Enter relative humidity (RH) in percentage: ")) / 100
    R_n      = 18                               #float(input("Enter net radiation (R_n) in MJ/m²/day: "))
    G        = 0                                #float(input("Enter soil heat flux density (G) in MJ/m²/day: "))
    Kc       = get_crop_coefficient(crop_type, crop_growth_season)
    
    es = calc_saturation_vapor_pressure(T)
    ea = calc_actual_vapor_pressure(es, RH)

    ET0 = calc_ref_evapotranspiration(R_n, G, T, u2, es, ea, altitude)
    ETc = calc_crop_evapotranspiration(ET0, Kc)

    # parameters related to the soil worked on
    MAD              = 0.5                      #float(input("Enter management allowable depletion (MAD) as a fraction (e.g., 0.5 for 50%): "))
    field_capacity   = 160                      #float(input("Enter field capacity (FC) in mm: "))
    wilting_point    = 40                       #float(input("Enter wilting point (WP) in mm: "))
    moisture         = 70                       #float(input("Enter soil moisture value in mm: "))
    
    moisture, deep_percolation = calc_soil_props(moisture, field_capacity, wilting_point)
    amount, days = calc_irrigation_need(moisture, ETc, field_capacity, wilting_point, MAD)
    
    print(
        f"""
        
        Reference Evapotranspiration (ET0): {ET0:.2f} mm/day
        Crop Evapotranspiration (ETc): {ETc:.2f} mm/day
        Deep Percolation: {deep_percolation:.2f} mm

        Soil Moisture: {moisture:.2f} mm
        Irrigation needed: {amount:.2f} mm
        Days: {days}
        
        """
    )
    
    #save_to_sqlite(crop_type, altitude, T, u2, RH, R_n, G, Kc, ET0, ETc, moisture, deep_percolation, amount, days)


if __name__ == '__main__':
    main()
