import requests


def get_weather_data(city_name="İzmir"): # gelişmiş bir versiyonda coğrafi koordinatlar da kullanılabilir
    api_key = API_KEY
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = \ 
    base_url + "appid=" + api_key + "&q=" + city_name + "&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    altitude      = data['main']['alt']
    temperature   = data['main']['temp']
    wind_speed    = data['wind']['speed']
    humidity      = data['main']['humidity']
    net_radiation = data['main']['raditation']
    
    return altitude, temperature, wind_speed, humidity, net_radiation
    # rakım, sıcaklık, rüzgar hızı, bağıl nem, net radyasyon