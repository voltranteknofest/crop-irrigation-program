import sqlite3
import datetime
import numpy as np
import math

DB_PATH = "irrigationtools/db/irrigation_data.db"

SQL_INSERT = \
    """
INSERT INTO irrigation_results (date, crop_type, altitude, T, u2, RH, R_n, G, Kc, ET0, ETc, moisture, deep_percolation, irrigation_needed, days)
  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

SQL_TABLE = \
    """
CREATE TABLE IF NOT EXISTS irrigation_results (
id INTEGER PRIMARY KEY,
date TEXT,
crop_type STR,
altitude REAL,
T REAL,
u2 REAL,
RH REAL,
R_n REAL,
G REAL,
Kc REAL,
ET0 REAL,
ETc REAL,
moisture REAL,
deep_percolation REAL,
irrigation_needed REAL,
days INTEGER
)
"""

PARAMS_MAPPING = {
    1: "Date",
    2: "Crop Type",
    3: "Altitude",
    4: "Temperature (T)",
    5: "Wind Speed (u2)",
    6: "Relative Humidity (RH)",
    7: "Net Radiation (R_n)",
    8: "Soil Heat Flux (G)",
    9: "Crop Coefficient (Kc)",
    10: "Reference Evapotranspiration (ET0)",
    11: "Crop Evapotranspiration (ETc)",
    12: "Soil Moisture",
    13: "Deep Percolation",
    14: "Irrigation Needed (amount)",
    15: "Days"
}

CROP_MAPPING = \
    {
        "tomato":   {"init-season": 0.7, "mid-season": 1.5, "late-season": 0.8},
        "potato":   {"init-season": 0.5, "mid-season": 1.15, "late-season": 0.75},
        "cherries": {"init-season": 0.5, "mid-season": 1.2, "late-season": 0.85},
        # rest
    }

RESULTS_PATH = "irrigationtools/db/results.txt"


def get_results_all():
    """
    Fetch all results ever saved and write them to db/results.txt
    """
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM irrigation_results")

    rows = cursor.fetchall()
    count = 1
    
    f = open(RESULTS_PATH, "w")

    for r in rows:
        print(f"\n--- {count} ---\n", file=f)
        for i, value in enumerate(r):
            if i != 0:
                print(f"{PARAMS_MAPPING.get(i, "Unknown")}: {value}", file=f)
        count += 1
        
    f.close()
    conn.close()

def calc_median_moisture_for_result(crop_type):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM irrigation_results WHERE crop_type = ?", (crop_type,))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return None

    inverted_params = {v: k for k, v in PARAMS_MAPPING.items()}
    soil_moisture_values = [r[inverted_params["Soil Moisture"]] for r in rows]
    median_soil_moisture = np.median(soil_moisture_values)
    
    print(soil_moisture_values)

    return median_soil_moisture


def save_to_sqlite(crop_type, altitude, T, u2, RH, R_n, G, Kc, ET0, ETc, moisture, deep_percolation, amount, days):
    """
    Save results to sqlite db
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(SQL_TABLE)
    conn.commit()

    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(SQL_INSERT, (date, crop_type, altitude, T, u2, RH, R_n,
                   G, Kc, ET0, ETc, moisture, deep_percolation, amount, days))

    conn.commit()
    conn.close()


def delete_by_id(id):
    """
    Deletes a specific irrigation result by its ID
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM irrigation_results WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def calc_saturation_vapor_pressure(T):
    """
    Calculate the saturation vapor pressure (es) for a given temperature (T)
    """
    return 0.6108 * math.exp((17.27 * T) / (T + 237.3))

def calc_actual_vapor_pressure(es, RH):
    """
    Calculate the actual vapor pressure (ea) based on es and relative humidity (RH)
    """
    return RH * es

def calc_ref_evapotranspiration(R_n, G, T, u2, es, ea, altitude):
    """
    Calculate the reference evapotranspiration (ET0) using the Penman-Monteith equation
    """

    # constants
    cp = 1.013 * 10**-3  # MJ/kg/°C
    lambda_ = 2.45  # MJ/kg
    epsilon = 0.622

    # calculate atmospheric pressure (P) in kPa
    P = 101.3 * ((293 - 0.0065 * altitude) / 293)**5.26

    # psychrometric constant (gamma) in kPa/°C
    gamma = cp * P / (epsilon * lambda_)

    # slope of the saturation vapor pressure curve (delta) in kPa/°C
    delta = (4098 * (0.6108 * math.exp((17.27 * T) / (T + 237.3)))) / ((T + 237.3) ** 2)

    # reference evapotranspiration (ET0) in mm/day
    ET0 = (0.408 * delta * (R_n - G) + gamma * (900 / (T + 273)) * u2 * (es - ea)) / (delta + gamma * (1 + 0.34 * u2))

    return ET0

def get_crop_coefficient(crop_type, growth_season):
    return CROP_MAPPING[crop_type][growth_season]

def calc_crop_evapotranspiration(ET0, Kc):
    """
    Calculate the crop evapotranspiration (ETc) in mm/day
    """
    
    # crop evapotranspiration (ETc) in mm/day
    ETc = ET0 * Kc
    return ETc

def calc_soil_props(moisture, field_capacity, wilting_point):
    """
    Update soil moisture and calculate deep percolation
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
    Calculate irrigation need and days until irrigation is required
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
    moisture         = 140                      #float(input("Enter soil moisture value in mm: "))
    
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
