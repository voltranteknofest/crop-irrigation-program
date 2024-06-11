# Crop Evapotanspiration Program

## Metric System Explained

### Units of Measurement

1. **MJ/m²/day** - **Megajoules per square meter per day**
    
    - **MJ**: Megajoules, a unit of energy. 1 MJ = 1,000,000 joules.
    - **m²**: Square meters, a unit of area.
    - **day**: Time period of one day.
    - **Usage**: Used for measuring net radiation (R<sub>n</sub>) and soil heat flux density (G).
2. **°C** - **Degrees Celsius**
    
    - **°C**: Degrees Celsius, a unit of temperature.
    - **Usage**: Used for mean daily air temperature (T).
3. **kPa** - **Kilopascals**
    
    - **kPa**: Kilopascals, a unit of pressure. 1 kPa = 1,000 pascals.
    - **Usage**: Used for atmospheric pressure (P), saturation vapor pressure (e<sub>s</sub>), and actual vapor pressure (e<sub>a</sub>).
4. **m/s** - **Meters per second**
    
    - **m/s**: Meters per second, a unit of speed.
    - **m**: Meter, a unit of length.
    - **s**: Second, a unit of time.
    - **Usage**: Used for wind speed at 2 meters height (u<sub>2</sub>).
5. **Dimensionless**
    
    - **K<sub>c</sub>**: Crop coefficient, a dimensionless number.
    - **Usage**: Multiplies the reference evapotranspiration (ET<sub>0</sub>) to calculate the crop evapotranspiration (ET<sub>c</sub>).
6. **m** - **Meters**
    
    - **m**: Meter, a unit of length.
    - **Usage**: Used for altitude.

### Summary of Each Unit

- **MJ**: Megajoule, measures energy.
- **m²**: Square meter, measures area.
- **day**: Day, measures time.
- **°C**: Degree Celsius, measures temperature.
- **kPa**: Kilopascal, measures pressure.
- **m/s**: Meters per second, measures speed.
- **m**: Meter, measures length.
- **Dimensionless**: No units, just a numerical value.

By understanding these units, you can correctly interpret the inputs and outputs of the Penman-Monteith method. Here's the context of how they are used in the program:

- **Net Radiation (R<sub>n</sub>)**: Energy per unit area per day (MJ/m²/day).
- **Soil Heat Flux Density (G)**: Energy per unit area per day (MJ/m²/day).
- **Mean Daily Temperature (T)**: Temperature in degrees Celsius (°C).
- **Wind Speed at 2 m Height (u<sub>2</sub>)**: Speed in meters per second (m/s).
- **Saturation Vapor Pressure (e<sub>s</sub>)**: Pressure in kilopascals (kPa).
- **Actual Vapor Pressure (e<sub>a</sub>)**: Pressure in kilopascals (kPa).
- **Crop Coefficient (K<sub>c</sub>)**: Dimensionless number.
- **Altitude**: Length in meters (m).