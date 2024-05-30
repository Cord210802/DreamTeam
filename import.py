from pymongo import MongoClient
from py2neo import Graph

# Connect to MongoDB
client = MongoClient('mongodb://mongodb:27017/')
db = client['spotify']
tracks = list(db.tracks.find({}))
artists = list(db.artists.find({}))

# Connect to Neo4j
graph = Graph("bolt://neo4j:7687", auth=("neo4j", "password"))

# Delete all nodes and relationships
graph.run("MATCH (n) DETACH DELETE n")

# Insert genres and ensure they are unique
for artist in artists:
    genres = artist.get('genres', ['Unknown'])
    for genre in genres:  # Insert all genres
        graph.run("MERGE (g:Genre {name: $genre})", genre=genre)

# Insert artists and connect them with their genres
for artist in artists:
    graph.run("""
        MERGE (a:Artist {id: $id})
        ON CREATE SET a.name = $name, a.popularity = $popularity
    """, id=artist['id'], name=artist['name'], popularity=artist['popularity'])
    genres = artist.get('genres', ['Unknown'])
    for genre in genres:  # Connect artist to all genres
        graph.run("""
            MATCH (a:Artist {id: $id})
            MATCH (g:Genre {name: $genre})
            MERGE (a)-[:HAS_GENRE]->(g)
        """, id=artist['id'], genre=genre)

# Insert tracks and connect them with artists, albums, and genres
for track in tracks:
    # Create album node
    graph.run("""
        MERGE (al:Album {id: $album_id})
        ON CREATE SET al.name = $album_name
    """, album_id=track['album_id'], album_name=track['album_name'])

    # Create track node
    graph.run("""
        MERGE (t:Track {id: $track_id})
        ON CREATE SET t.name = $track_name
    """, track_id=track['track_id'], track_name=track['track_name'])

    # Connect the track to the artist
    graph.run("""
        MATCH (t:Track {id: $track_id})
        MATCH (a:Artist {id: $artist_id})
        MERGE (t)-[:PERFORMED_BY]->(a)
    """, track_id=track['track_id'], artist_id=track['artist_id'])
    
    # Connect the track to the album
    graph.run("""
        MATCH (t:Track {id: $track_id})
        MATCH (al:Album {id: $album_id})
        MERGE (t)-[:PART_OF]->(al)
    """, track_id=track['track_id'], album_id=track['album_id'])

    # Connect the track to all genres of the artist
    genres = db.artists.find_one({'id': track['artist_id']}).get('genres', ['Unknown'])
    for genre in genres:
        graph.run("""
            MATCH (t:Track {id: $track_id})
            MATCH (g:Genre {name: $genre})
            MERGE (t)-[:IN_GENRE]->(g)
        """, track_id=track['track_id'], genre=genre)

# Verification
print("Total Genres: ", graph.evaluate("MATCH (g:Genre) RETURN count(g)"))
print("Total Artists: ", graph.evaluate("MATCH (a:Artist) RETURN count(a)"))
print("Total Tracks: ", graph.evaluate("MATCH (t:Track) RETURN count(t)"))
print("Total Albums: ", graph.evaluate("MATCH (al:Album) RETURN count(al)"))
