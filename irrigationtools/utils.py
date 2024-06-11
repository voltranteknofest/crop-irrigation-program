import math
from .consts import CROP_MAPPING

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
