from pymongo import MongoClient
from py2neo import Graph

# Conectar a MongoDB
client = MongoClient('mongodb://mongodb:27017/')
db = client['spotify']
tracks = list(db.tracks.find({}))
artists = list(db.artists.find({}))

# Conectar a Neo4j
graph = Graph("bolt://neo4j:7687", auth=("neo4j", "password"))

# Insertar géneros y asegurar que son únicos
for artist in artists:
    genres = artist.get('genres', ['Unknown'])
    if genres:  # Verificar que la lista no esté vacía
        genre = genres[0]  # Tomar el primer elemento de la lista de géneros
        graph.run("MERGE (g:Genre {name: $genre})", genre=genre)

# Insertar artistas y conectarlos con sus géneros
for artist in artists:
    genres = artist.get('genres', ['Unknown'])
    if genres:
        genre = genres[0]
        graph.run("""
            MERGE (a:Artist {id: $id})
            ON CREATE SET a.name=$name, a.popularity=$popularity
            WITH a
            MATCH (g:Genre {name: $genre})
            MERGE (a)-[:HAS_GENRE]->(g)
        """, id=artist['id'], name=artist['name'], popularity=artist['popularity'], genre=genre)

# Insertar tracks y conectarlos con artistas y géneros
for track in tracks:
    graph.run("""
        MERGE (t:Track {id: $track_id})
        ON CREATE SET t.name=$track_name, t.album=$album_name
        WITH t
        MATCH (a:Artist {id: $artist_id})
        MERGE (t)-[:PERFORMED_BY]->(a)
        WITH t, a  
        MATCH (g:Genre)-[:HAS_ARTIST]->(a)
        MERGE (t)-[:IN_GENRE]->(g)
    """, track_id=track['track_id'], track_name=track['track_name'], album_name=track['album_name'], artist_id=track['artist_id'])

# Verificación
print("Total Genres: ", graph.evaluate("MATCH (g:Genre) RETURN count(g)"))
print("Total Artists: ", graph.evaluate("MATCH (a:Artist) RETURN count(a)"))
print("Total Tracks: ", graph.evaluate("MATCH (t:Track) RETURN count(t)"))