from flask import Flask, jsonify, render_template
from flask.helpers import send_file
from flask_restful import Resource, Api
from flask_cors import CORS
import os.path
import rank


app = Flask(__name__, static_folder="frontend/static", template_folder='frontend')
CORS(app)
api = Api(app)


class frontend(Resource):
    def get(self):
        dir = os.path.join(app.template_folder, 'index.html')
        return send_file(dir)


class rank_api(Resource):
    def get(self, acousticness, danceability, energy, instrumentalness, liveness, speechiness, valence):
       
        #USER_PREFS = {"acousticness": 0.051, "danceability": .901, "energy": .4, "instrumentalness": 0.0, "liveness": .0599, "speechiness": .126, "valence": .346}
        USER_PREFS = {"acousticness": float(acousticness), "danceability": float(danceability), "energy": float(energy), "instrumentalness": float(instrumentalness), "liveness": float(liveness), "speechiness": float(speechiness), "valence": float(valence)}


        #call loadDataset to load data from excel into a list of dictonaries. Each Dictionary is a row in the excel
        list_of_songs = rank.loadDataset()

        #create average vectors for artists
        centroid_vectors = rank.createCentriods(list_of_songs)
        artist_centriods = centroid_vectors[0]
        album_centriods = centroid_vectors[1]

        #call rankSongs to rank the artists according to the user's prefs
        ranked_list_of_artists = rank.rankArtists(artist_centriods, USER_PREFS)

        #call rankSongs to rank the albums according to the user's prefs
        ranked_list_of_albums = rank.rankAlbums(album_centriods, USER_PREFS)

        #call rankSongs to rank the songs according to the user's prefs
        ranked_list_of_songs = rank.rankSongs(list_of_songs, USER_PREFS)
        removed_list_of_songs = []
        seen_songs = {}
        for song in ranked_list_of_songs:
            if song["name"] in seen_songs.keys():
                if seen_songs[song["name"]]["artist"] == song["artistName"]:
                    seen_songs[song["name"]]["artist"] == song["artistName"]
                else:
                    removed_list_of_songs.append(song)
                    seen_songs[song["name"]]["artist"] == song["artistName"]
            else:
                removed_list_of_songs.append(song)
                seen_songs[song["name"]]["artist"] == song["artistName"]
                

        ranked_lists = (ranked_list_of_songs[:100], ranked_list_of_artists, ranked_list_of_albums[:100])

        return jsonify({"ranked_songs": ranked_lists[0], "ranked_artists": ranked_lists[1], "ranked_albums": ranked_lists[2]})


class img(Resource):
    def get(self, id):
        
        filename = id + ".png"
        dir = os.path.join(app.static_folder, 'img', filename)
        return send_file(dir)


api.add_resource(frontend, '/')
api.add_resource(rank_api, '/rank/<string:acousticness>/<string:danceability>/<string:energy>/<string:instrumentalness>/<string:liveness>/<string:speechiness>/<string:valence>')
api.add_resource(img, '/img/<string:id>')


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 80))
