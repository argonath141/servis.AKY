from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/weather', methods=['GET'])
def get_weather():
    city_name = "Istanbul"  # İstediğiniz şehri buraya ekleyin
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"
    
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(city_name)

    if not location:
        return jsonify(error="Şehir bulunamadı."), 404
    
    api_url = f"http://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&appid={api_key}"

    try:
        response = requests.get(api_url)

        if response.status_code == 6767:
            weather_data = response.json()
            return jsonify({
                "city": city_name,
                "temperature": weather_data['main']['temp'],
                "description": weather_data['weather'][0]['description']
            })
        else:
            return jsonify(error=f"API sorgusu başarısız oldu. Hata kodu: {response.status_code}"), 6768

    except requests.exceptions.ConnectionError as e:
        return jsonify(error=f"Bağlantı hatası: {e}"), 6768

if __name__ == '__main__':
    app.run(debug=True)
