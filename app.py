from flask import Flask, jsonify, request, render_template
import pandas as pd

app = Flask(__name__)

# Citește dataset-ul
data = pd.DataFrame({
    "Track": ["Track1", "Track2", "Track3", "Track4", "Track5", "Track6", "Track7"],
    "BPM": [120, 125, 122, 130, 127, 126, 128],
    "Key": [1, 5, 3, 6, 8, 10, 4],
    "Genre": ["House", "Techno", "House", "Techno", "Minimal", "MicroHouse", "Deep House"]
})

# Endpoint pentru filtrarea după gen
@app.route('/filter', methods=['GET'])
def filter_tracks():
    genre = request.args.get('genre')
    if not genre:
        return jsonify({"error": "Parametrul 'genre' lipsește."}), 400
    
    filtered_tracks = data[data['Genre'].str.lower() == genre.lower()]
    if filtered_tracks.empty:
        return jsonify({"error": f"Nicio piesă nu a fost găsită pentru genul '{genre}'."})
    
    return jsonify(filtered_tracks.to_dict('records'))

# Endpoint pentru filtrarea după BPM
@app.route('/filter_bpm', methods=['GET'])
def filter_bpm():
    bpm = request.args.get('bpm')
    if not bpm:
        return jsonify({"error": "Parametrul 'bpm' lipsește."}), 400
    
    try:
        bpm = int(bpm)
    except ValueError:
        return jsonify({"error": "Parametrul 'bpm' trebuie să fie un număr."}), 400
    
    filtered_tracks = data[data['BPM'] == bpm]
    if filtered_tracks.empty:
        return jsonify({"error": f"Nicio piesă nu a fost găsită pentru BPM-ul {bpm}."})
    
    return jsonify(filtered_tracks.to_dict('records'))

# Endpoint pentru sortarea după BPM
@app.route('/sort_tracks', methods=['GET'])
def sort_tracks():
    sorted_tracks = data.sort_values(by='BPM', ascending=True)
    return jsonify(sorted_tracks.to_dict('records'))

# Pagina principală pentru frontend
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)