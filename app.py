from flask import Flask, request, jsonify
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Importă dataset-ul din fișierul CSV
data = pd.read_csv('data.csv')

# Endpoint principal pentru test
@app.route('/')
def home():
    return "Serverul este online!"

# Endpoint pentru a returna toate piesele
@app.route('/tracks', methods=['GET'])
def get_tracks():
    return jsonify(data.to_dict('records'))

# Endpoint pentru recomandări
@app.route('/recommend', methods=['POST'])
def recommend():
    input_track = request.json.get('Track')

    # Verifică dacă track-ul există în dataset
    input_data = data[data['Track'] == input_track]
    if input_data.empty:
        return jsonify({"error": f"Track-ul '{input_track}' nu a fost găsit."}), 404

    # Calculul similarității
    similarities = cosine_similarity(data[['BPM', 'Key']], input_data[['BPM', 'Key']])
    recommendations = data.iloc[similarities.flatten().argsort()[-2:]].to_dict('records')

    return jsonify(recommendations)

# Endpoint pentru adăugarea unei piese noi
@app.route('/filter', methods=['GET'])
def filter_tracks():
    # Preia parametrul "genre" din cererea GET
    genre = request.args.get('genre')
    if not genre:
        return jsonify({"error": "Parametrul 'genre' lipsește."}), 400

    # Filtrează piesele din dataset
    filtered_tracks = data[data['Genre'].str.lower() == genre.lower()]
    if filtered_tracks.empty:
        return jsonify({"error": f"Nicio piesă nu a fost găsită pentru genul '{genre}'."}), 404

    return jsonify(filtered_tracks.to_dict('records'))