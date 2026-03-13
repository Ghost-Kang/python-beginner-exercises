"""
通过 request获取天气情况

"""

__author__ = 'wangxukang'
__date__ = '2026-03-11'

import requests
import json
import os
from datetime import datetime

API_KEY = 'ae1b77bb21db65b47eab412699e2cc25'
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

Cities = ['Beijing', 'Shanghai', 'Shenzhen','Xian','Chengdu','Qingdao']

def fetch_weather(city:str):
    params = {
        'appid': API_KEY,
        'q': city,
        'units': 'metric',
        'lang': 'zh_CN',
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    weathers = {
        'city': data['name'],
        'country': data['sys']['country'],
        'fetch_time': datetime.now().isoformat(),
        'weather': data['weather'][0]['description'],
        'temperature': data['main']['temp'],
        'feels_like': data['main']['feels_like'],
        'humidity': data['main']['humidity'],
        'pressure': data['main']['pressure'],
        'wind_speed': data['wind']['speed'],
        'wind_deg': data['wind']['deg'],
        'visibility': data.get('visibility',None),
        'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
        'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
    }
    return weathers
def main():
    result = []
    for city in Cities:
        try:
            result.append(fetch_weather(city))
            print(f"获取城市{city}成功！")
        except Exception as e:
            print(f"获取{city}失败-{e}")


    out_path = f"weather_date/weather_{datetime.now():%Y%m%d_%H%M%S}.json"
    os.makedirs('weather_date', exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    print(f"\n保存的文件：{out_path}")

if __name__ == '__main__':
    main()
