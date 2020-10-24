import pandas
import math


def main():
    #define user prefs, later these will be values pulled from GUI
    #In GUI we need to create inputs that the user can understand ie. not a 1:1 relationship to these stats
    #assign these stats based on the users mood (inputs from gui)
    USER_PREFS = {"acousticness": 0.051, "danceability": .901, "energy": .4, "instrumentalness": 0.0, "liveness": .0599, "speechiness": .126, "valence": .346}

    #call loadDataset to load data from excel into a list of dictonaries. Each Dictionary is a row in the excel
    list_of_songs = loadDataset()

    #create average vectors for artists
    centroid_vectors = createCentriods(list_of_songs)
    artist_centriods = centroid_vectors[0]
    album_centriods = centroid_vectors[1]

    #call rankSongs to rank the songs according to the user's prefs
    ranked_list_of_artists = rankArtists(artist_centriods, USER_PREFS)

    #call rankSongs to rank the songs according to the user's prefs
    ranked_list_of_albums = rankAlbums(album_centriods, USER_PREFS)

    #call rankSongs to rank the songs according to the user's prefs
    ranked_list_of_songs = rankSongs(list_of_songs, USER_PREFS)

    ranked_lists = (ranked_list_of_songs, ranked_list_of_artists, ranked_list_of_albums)

    #call exportDataset to export ranked list to excel
    exportDataset(ranked_lists, USER_PREFS)




# Helper functions =============================================
def loadDataset():
    excel = pandas.read_excel("dataset.xlsx")
    data = pandas.DataFrame(excel)
    return data.to_dict('records')


def rankSongs(ls, USER_PREFS):
    #input LS - a list of dictionaries. Each dictionary is a row in the excel
    #input USER_PREFS - a dictonary of the user's preferences


    #fetch the selected user prefs
    features = list(USER_PREFS.keys())
    
    #compute the magnitude of the user preference vector. used in cosine similarity equation
    user_mag = 0.0
    for feature in features:
        user_mag += math.pow(USER_PREFS[feature], 2)
    user_mag = math.sqrt(user_mag)

    #compute the magnitude and cosine similartiy for each song. Append the song with the similarity score to an unsorted list
    similarity_ranking = []
    for song in ls:

        dot_product = 0.0
        song_mag = 0.0
        for feature in features:
            user_feature = USER_PREFS[feature]
            song_feature = song[feature]
            song_mag += math.pow(song_feature, 2)

            if song_feature != 0.0 and user_feature != 0.0:
                dot_product += user_feature * song_feature
        
        song_mag = math.sqrt(song_mag)
        similarity = dot_product / (user_mag * song_mag)
        song["similarity"] = similarity
        similarity_ranking.append(song)

    #sort the songs according to their similarity score
    sorted_similarity_ranking = sorted(similarity_ranking, key=lambda i: i["similarity"], reverse=True)

    return sorted_similarity_ranking


def rankArtists(ac, USER_PREFS):
    #input ac - the dictionary of artist centriods
    #input USER_PREFS - the dictionary of user preferences


    #fetch the selected user prefs
    features = list(USER_PREFS.keys())

    #compute the magnitude of the user preference vector. used in cosine similarity equation
    user_mag = 0.0
    for feature in features:
        user_mag += math.pow(USER_PREFS[feature], 2)
    user_mag = math.sqrt(user_mag)

    #compute the magnitude and cosine similartiy for each album and user preference. Append the artist with the similarity score to an unsorted list
    similarity_ranking = []
    for artist in ac:

        dot_product = 0.0
        artist_mag = 0.0
        for feature in features:
            user_feature = USER_PREFS[feature]
            artist_feature = ac[artist][feature]
            artist_mag += math.pow(artist_feature, 2)

            if artist_feature != 0.0 and user_feature != 0.0:
                dot_product += user_feature * artist_feature
        
        artist_mag = math.sqrt(artist_mag)
        similarity = dot_product / (user_mag * artist_mag)
        ac[artist]["similarity"] = similarity
        similarity_ranking.append(ac[artist])

    #sort the songs according to their similarity score
    sorted_similarity_ranking = sorted(similarity_ranking, key=lambda i: i["similarity"], reverse=True)

    return sorted_similarity_ranking


def rankAlbums(ac, USER_PREFS):
    #input ac - the dictionary of album centriods
    #input USER_PREFS - the dictionary of user preferences


    #fetch the selected user prefs
    features = list(USER_PREFS.keys())

    #compute the magnitude of the user preference vector. used in cosine similarity equation
    user_mag = 0.0
    for feature in features:
        user_mag += math.pow(USER_PREFS[feature], 2)
    user_mag = math.sqrt(user_mag)

    #compute the magnitude and cosine similartiy for each album and user preference. Append the artist with the similarity score to an unsorted list
    similarity_ranking = []
    for album in ac:

        dot_product = 0.0
        album_mag = 0.0
        for feature in features:
            user_feature = USER_PREFS[feature]
            album_feature = ac[album][feature]
            album_mag += math.pow(album_feature, 2)

            if album_feature != 0.0 and user_feature != 0.0:
                dot_product += user_feature * album_feature
        
        album_mag = math.sqrt(album_mag)
        similarity = dot_product / (user_mag * album_mag)
        ac[album]["similarity"] = similarity
        similarity_ranking.append(ac[album])

    #sort the songs according to their similarity score
    sorted_similarity_ranking = sorted(similarity_ranking, key=lambda i: i["similarity"], reverse=True)

    return sorted_similarity_ranking


def createCentriods(ls):
    #input ls - the list of songs


    #dicts containing the artist and album centriod vectors 
    artist_centroid = {}
    album_centroid = {}

    #loop through each song and sum the attributes for each artist and album
    for song in ls:
        artist = song["artistName"]
        album = song["albumName"]

        if artist not in artist_centroid:
            artist_centroid[artist] = {"count": 1, "artistName": song["artistName"], "artistID": song["artistID"], "acousticness": song["acousticness"], "danceability": song["danceability"], "energy": song["energy"], "instrumentalness": song["instrumentalness"], "liveness": song["liveness"], "speechiness": song["speechiness"], "valence": song["valence"]}

        if album not in album_centroid:
            album_centroid[album] = {"count": 1, "albumName": song["albumName"], "albumID": song["albumID"], "acousticness": song["acousticness"], "danceability": song["danceability"], "energy": song["energy"], "instrumentalness": song["instrumentalness"], "liveness": song["liveness"], "speechiness": song["speechiness"], "valence": song["valence"]}

        artist_centroid[artist] = {"count": artist_centroid[artist]["count"] + 1, "artistName": song["artistName"], "artistID": song["artistID"], "acousticness": artist_centroid[artist]["acousticness"] + song["acousticness"], "danceability": artist_centroid[artist]["danceability"] + song["danceability"], "energy": artist_centroid[artist]["energy"] + song["energy"], "instrumentalness": artist_centroid[artist]["instrumentalness"] + song["instrumentalness"], "liveness": artist_centroid[artist]["liveness"] + song["liveness"], "speechiness": artist_centroid[artist]["speechiness"] + song["speechiness"], "valence": artist_centroid[artist]["valence"] + song["valence"]}
        album_centroid[album] = {"count": album_centroid[album]["count"] + 1, "albumName": song["albumName"], "albumID": song["albumID"], "acousticness": album_centroid[album]["acousticness"] + song["acousticness"], "danceability": album_centroid[album]["danceability"] + song["danceability"], "energy": album_centroid[album]["energy"] + song["energy"], "instrumentalness": album_centroid[album]["instrumentalness"] + song["instrumentalness"], "liveness": album_centroid[album]["liveness"] + song["liveness"], "speechiness": album_centroid[album]["speechiness"] + song["speechiness"], "valence": album_centroid[album]["valence"] + song["valence"]}
    
    #average the artist centroid vectors using the number of values summed
    for artist in artist_centroid:
        count = artist_centroid[artist]["count"]
        for key in artist_centroid[artist].keys():
            if key != "artistName" and key != "artistID":
                artist_centroid[artist][key] /= count

    #average the album centriod vectors using the number of values summed
    for album in album_centroid:
        count = album_centroid[album]["count"]
        for key in album_centroid[album].keys():
            if key != "albumName" and key != "albumID":
                album_centroid[album][key] /= count

    return (artist_centroid, album_centroid)


def exportDataset(rl, USER_PREFS):
    #input rl - ranked lists for songs, artists, albums
    #input USER_PREFS - a dictonary of the user's preferences
    

    output_songs = {"similarity": [], "songName": [], "artistName": [], "albumName": [], "songID": [], "artistID": [], "albumID": [], "duration": [], "key": [], "mode": [], "time_signature": [], "acousticness": [], "danceability": [], "energy": [], "instrumentalness": [], "liveness": [], "loudness": [], "speechiness": [], "valence": [], "tempo": []}
    output_artists = {"similarity": [], "artistName": [], "artistID": [], "acousticness": [], "danceability": [], "energy": [], "instrumentalness": [], "liveness": [], "speechiness": [], "valence": []}
    output_albums = {"similarity": [], "albumName": [], "albumID": [], "acousticness": [], "danceability": [], "energy": [], "instrumentalness": [], "liveness": [], "speechiness": [], "valence": []}
    outputs = (output_songs, output_artists, output_albums)

    features = list(USER_PREFS.keys())
    for feature in features:
        for output in outputs:
            output[feature].append(USER_PREFS[feature])

    for output in outputs:
        for key in output.keys():
            if len(output[key]) == 0:
                output[key].append("-")

    for song in rl[0]:
        for key in song.keys():
            if key in output_songs:
                output_songs[key].append(song[key])

    for artist in rl[1]:
        for key in artist.keys():
            if key in output_artists:
                output_artists[key].append(artist[key])

    for albums in rl[2]:
        for key in albums.keys():
            if key in output_albums:
                output_albums[key].append(albums[key])

    pandas.DataFrame(output_songs).to_excel("./ranked_songs.xlsx")
    pandas.DataFrame(output_artists).to_excel("./ranked_artists.xlsx")
    pandas.DataFrame(output_albums).to_excel("./ranked_albums.xlsx")




if __name__ == "__main__":
    main()