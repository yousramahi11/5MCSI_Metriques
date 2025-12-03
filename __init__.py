from flask import Flask, render_template, jsonify
from urllib.request import urlopen
import json
from datetime import datetime

app = Flask(__name__)


# ---------------------------
# PAGE D'ACCUEIL
# ---------------------------
@app.route("/")
def index():
    return render_template("hello.html")



# ---------------------------
# EXERCICE 2 : ROUTE CONTACT
# ---------------------------
@app.route("/contact/")
def contact():
    return render_template("contact.html")



# ---------------------------
# EXERCICE 3 : API TAWARANO
# ---------------------------
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []

    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15
        results.append({'Jour': dt_value, 'temp': temp_day_value})

    return jsonify(results=results)



# ---------------------------
# EXERCICE 3 BIS : PAGE RAPPORT
# ---------------------------
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")



# ---------------------------
# EXERCICE 4 : HISTOGRAMME
# ---------------------------
@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")



# ---------------------------
# EXERCICE 5 : PAGE CONTACT AVANCÉE
# (déjà gérée via contact.html)
# ---------------------------



# ---------------------------
# EXERCICE 6 : COMMITS GITHUB
# ---------------------------

# extrait les minutes d’une date ISO
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})


# route commits avec graphique
@app.route("/commits/")
def commits():
    return render_template("commits.html")


# API interne : récupération des commits GitHub
@app.route("/api/commits/")
def api_commits():
    url = "https://api.github.com/repos/yousramahi11/5MCSI_Metriques/commits"
    response = urlopen(url)
    data = json.loads(response.read().decode("utf-8"))

    results = []
    for commit in data:
        date_str = commit.get("commit", {}).get("author", {}).get("date")
        if date_str:
            dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            results.append({
                "minute": dt.minute,
                "date": date_str
            })

    return jsonify(results=results)



# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
