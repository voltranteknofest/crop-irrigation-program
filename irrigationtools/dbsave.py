import sqlite3
import datetime
import numpy as np
from .consts import DB_PATH, SQL_INSERT, SQL_TABLE, PARAMS_MAPPING


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


__all__ = ["get_results_all", "calc_median_moisture_for_result",
           "save_to_sqlite", "delete_by_id"]
