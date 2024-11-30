from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Ruta para la página principal
@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None

    if request.method == "POST":
        ciudad = request.form.get("ciudad")
        if ciudad:
            # API de OpenWeatherMap
            api_key = "a760a4c49bba3a70eb69ef902c930efd"  
            url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric&lang=es"

            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    "ciudad": data["name"],
                    "temperatura": round(data["main"]["temp"], 1),  # Redondeo a un decimal
                    "descripcion": data["weather"][0]["description"].capitalize(),
                    "latitud": abs(data["coord"]["lat"]),  # Convertir valores negativos a positivos
                    "longitud": abs(data["coord"]["lon"]),  # Convertir valores negativos a positivos
                    "icono": data["weather"][0]["icon"],
                }
            else:
                weather_data = {"error": "No se pudo encontrar la ciudad. Intenta nuevamente."}

    return render_template("index.html", weather_data=weather_data)

# Ruta para la hoja de vida (opcional, en caso de que sigas usando)
@app.route("/cv.html")
def cv():
    return render_template("cv.html")

if __name__ == "__main__":
    app.run(debug=True)
