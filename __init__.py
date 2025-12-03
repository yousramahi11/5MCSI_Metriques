from flask import Flask, render_template, jsonify
from urllib.request import urlopen
from collections import Counter
from datetime import datetime
import json


app = Flask(__name__)


# --------- Exercice 2 & 5 : page de contact ----------
@app.route("/contact/")
def contact():
    # renvoie ton fichier contact.html (formulaire joli)
    return render_template("contact.html")


# --------- Accueil ----------
@app.route("/")
def hello_world():
    return render_template("hello.html")


# --------- Exercice 3 : API /tawarano/ ----------
@app.route("/tawarano/")
def meteo():
    response = urlopen(
        "https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx"
    )
    raw_content = response.read()
    json_content = json.loads(raw_content.decode("utf-8"))

    results = []
    for list_element in json_content.get("list", []):
        dt_value = list_element.get("dt")
        temp_day_value = list_element.get("main", {}).get("temp") - 273.15  # Kelvin -> °C
        results.append({"Jour": dt_value, "temp": temp_day_value})

    return jsonify(results=results)


# --------- Exercice 3 bis : page graphique simple ----------
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")


# --------- Exercice 4 : histogramme ----------
@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")


# --------- Exercice 6 : commits GitHub ----------

def extract_minutes_from_string(date_string: str) -> int:
    """Transforme '2024-02-11T11:57:27Z' -> 57 (minute)."""
    date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
    return date_object.minute


@app.route("/commits-data/")
def commits_data():
    # API fournie dans l’énoncé
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = urlopen(url)
    raw_content = response.read()
    commits = json.loads(raw_content.decode("utf-8"))

    minutes_count = {}

    for commit in commits:
        date_string = commit.get("commit", {}).get("author", {}).get("date")
        if not date_string:
            continue

        minute = extract_minutes_from_string(date_string)
        minutes_count[minute] = minutes_count.get(minute, 0) + 1

    # transformation en liste pour le JSON
    results = []
    for minute, count in sorted(minutes_count.items()):
        results.append({"minute": f"{minute:02d}", "count": count})

    return jsonify(results=results)


@app.route("/commits/")
def commits_page():
    return render_template("commits.html")


# --------- Lancement local (pas utilisé sur Alwaysdata) ----------
if __name__ == "__main__":
    app.run(debug=True)
