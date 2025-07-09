from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# 네 API 키를 여기에 입력
API_KEY = '2a59d6751a25e1e71e373c42a9a2dd84'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None

    if request.method == 'POST':
        city = request.form.get('city')

        if city:
            params = {
                'q': city,
                'appid': API_KEY,
                'units': 'metric',
                'lang': 'kr'
            }
            response = requests.get(BASE_URL, params=params)

            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    'city': data['name'],
                    'temp': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon']
                }
            else:
                weather_data = {'error': '도시를 찾을 수 없습니다.'}

    return render_template('index.html', weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
