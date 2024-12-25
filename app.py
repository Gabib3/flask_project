from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Configurarea aplicației Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configurarea SQLAlchemy
db = SQLAlchemy(app)

# Definirea modelului bazei de date
class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bpm = db.Column(db.Integer, nullable=False)
    key = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(50), nullable=False)

# Inițializarea bazei de date
with app.app_context():
    db.create_all()

# Endpoint pentru adăugarea unui track
@app.route('/add-track', methods=['POST'])
def add_track():
    data = request.get_json()
    new_track = Track(
        name=data['name'],
        bpm=data['bpm'],
        key=data['key'],
        genre=data['genre']
    )
    db.session.add(new_track)
    db.session.commit()
    return jsonify({'message': 'Track added successfully!'}), 201

# Endpoint pentru filtrarea track-urilor
@app.route('/filter', methods=['GET'])
def filter_tracks():
    genre = request.args.get('genre')
    tracks = Track.query.filter_by(genre=genre).all()
    if not tracks:
        return jsonify({'error': f'No tracks found for genre "{genre}"'}), 404
    result = [{'id': t.id, 'name': t.name, 'bpm': t.bpm, 'key': t.key, 'genre': t.genre} for t in tracks]
    return jsonify(result), 200

# Pornirea aplicației
if __name__ == '__main__':
    app.run(debug=True)