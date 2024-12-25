from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definim modelul bazei de date
class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bpm = db.Column(db.Integer, nullable=False)
    key = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(50), nullable=False)

# Inițializăm baza de date
@app.before_first_request
def create_tables():
    db.create_all()

# Ruta pentru adăugarea unei piese
@app.route('/add-track', methods=['POST'])
def add_track():
    data = request.get_json()
    if not data:
        return jsonify(error="No data provided"), 400
    
    try:
        track = Track(
            name=data['name'],
            bpm=data['bpm'],
            key=data['key'],
            genre=data['genre']
        )
        db.session.add(track)
        db.session.commit()
        return jsonify(message="Track added successfully"), 201
    except KeyError as e:
        return jsonify(error=f"Missing field: {str(e)}"), 400

# Ruta pentru filtrarea pieselor după gen
@app.route('/filter', methods=['GET'])
def filter_tracks():
    genre = request.args.get('genre')
    if not genre:
        return jsonify(error="Genre not provided"), 400
    
    tracks = Track.query.filter_by(genre=genre).all()
    if not tracks:
        return jsonify(error=f"No tracks found for genre '{genre}'"), 404

    result = [
        {"name": track.name, "bpm": track.bpm, "key": track.key, "genre": track.genre}
        for track in tracks
    ]
    return jsonify(result), 200

# Ruta implicită
@app.route('/')
def home():
    return "Welcome to the Flask Music App!"

# Handler pentru 404
@app.errorhandler(404)
def not_found(e):
    return jsonify(error="This route is not found"), 404

if __name__ == '__main__':
    app.run(debug=True)