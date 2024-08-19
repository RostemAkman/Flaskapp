from flask import Flask, render_template, request, url_for
import urllib.request
import ssl
import json
import pandas as pd
from werkzeug.utils import redirect

app = Flask(__name__)

@app.route("/") #Första endpointen.
def index():
    return render_template('index.html')

# Visar formuläret för att mata in datum och pris.
@app.route("/form")
def form():
    return render_template('form.html')

#Endpoint för att hämta elprisinformation baserat på användarens inmatade datum och pris.
@app.post("/api")
def api_post():
    try:
        # Hämta datum och pris från formuläret.
        kalender = request.form['kalender']
        year, month, day = kalender.split('-')
        price = request.form["price"]

        # Skapa URL för att hämta elprisinformation från API:t.
        context = ssl._create_unverified_context()
        data_url = f"https://www.elprisetjustnu.se/api/v1/prices/{year}/{month}-{day}_{price}.json"
        try:
            # Försök hämta JSON-data från API.
            json_data = urllib.request.urlopen(data_url, context=context).read()
        except urllib.error.HTTPError as e:
            # Om det är en HTTP 404-fel, visa felmeddelande.
            if e.code == 404:
                error_message = 'Ingen elprisinformation tillgänglig för det det datumet'
                return render_template('form.html', error_message=error_message)
            else:
                raise
        # Ladda JSON-data till en pandas DataFrame.
        data = json.loads(json_data)
        df = pd.DataFrame(data)

        # Omvandla och formatera DataFrame för att visas i HTML.
        # ändrar namn och lite siffror för att det ska bli tydligt och snyggt
        df.rename(columns={"time_end": "Tid", "EUR_per_kWh": "Euro", "SEK_per_kWh": "Ören per kWh"}, inplace=True)
        df['Tid'] = df['Tid'].apply(lambda x: pd.to_datetime(x).strftime('%H:%M'))
        df['Ören per kWh'] = df['Ören per kWh'].apply(lambda x: "{:.0f}".format(round(x * 100)))

        # Konvertera DataFrame till HTML-tabell
        table_data = df.to_html(columns=["Ören per kWh","Euro","Tid"], classes="table p-5", justify="left")
        return render_template('index.html', data=table_data)

    # Felhantering för ogiltigt datumformat.
    except ValueError as e:
        error_message = 'Felaktigt datumformat, försök igen.'
        return render_template('form.html', error_message=error_message)

# Felhantering för 404-fel, omdirigera till index.
@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)