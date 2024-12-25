from flask import Flask, request, jsonify
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Inițializare aplicație Flask
app = Flask(__name__)

# Încărcare dataset
data = pd.DataFrame({
    'Track': ['Track1', 'Track2', 'Track3', 'Track4', 'Track5'],
    'BPM': [120, 125, 122, 130, 127],
    'Key': [1, 5, 3, 6, 8],
    'Genre': ['House', 'Techno', 'House', 'Techno', 'Minimal']
})

# Ruta principală
@app.route("/")
def home():
    return "Serverul este online!"

# Endpoint pentru a obține toate piesele
@app.route("/tracks", methods=["GET"])
def get_tracks():
    return jsonify(data.to_dict(orient="records"))

# Endpoint pentru recomandări
@app.route("/recommend", methods=["POST"])
def recommend():
    input_track = request.json.get("track")
    if not input_track:
        return jsonify({"error": "Track-ul lipseste."}), 400

    if input_track not in data['Track'].values:
        return jsonify({"error": "Track-ul nu a fost găsit în baza de date."}), 404

    input_data = data[data['Track'] == input_track]
    similarity_scores = cosine_similarity(data[['BPM', 'Key']], input_data[['BPM', 'Key']])
    data['Similarity'] = similarity_scores
    recommendations = data.sort_values(by="Similarity", ascending=False).iloc[1:4]
    return jsonify(recommendations.to_dict(orient="records"))

# Endpoint pentru filtrare după gen
@app.route("/filter", methods=["GET"])
def filter_tracks():
    genre = request.args.get("genre")
    if not genre:
        return jsonify({"error": "Parametrul 'genre' lipseste."}), 400

    filtered_tracks = data[data['Genre'].str.lower() == genre.lower()]
    if filtered_tracks.empty:
        return jsonify({"error": f"Nicio piesă nu a fost găsită pentru genul '{genre}'"}), 404

    return jsonify(filtered_tracks.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)