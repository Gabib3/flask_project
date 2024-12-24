# Music Recommendation API

## Endpoint-uri disponibile:
### 1. Adăugare piesă nouă
- URL: `/add`
- Metoda: `POST`
- Body (JSON):
  ```json
  {
      "Track": "Track Name",
      "BPM": 120,
      "Key": 4,
      "Genre": "Genre Name"
  }