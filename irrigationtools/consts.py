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
