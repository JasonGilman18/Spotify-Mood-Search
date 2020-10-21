import pandas
import math


def main():
    #define user prefs, later these will be values pulled from GUI
    USER_PREFS = {"acousticness": 0.051, "danceability": .901, "energy": .4, "instrumentalness": 0.0, "liveness": .0599, "speechiness": .126, "valence": .346}

    #call loadDataset to load data from excel into a list of dictonaries. Each Dictionary is a row in the excel
    list_of_songs = loadDataset()

    #call rankDataset to rank the data according to the user's prefs
    ranked_list_of_songs = rankDataset(list_of_songs, USER_PREFS)

    #call exportDataset to export ranked list to excel
    exportDataset(ranked_list_of_songs, USER_PREFS)




# Helper functions =============================================
def loadDataset():
    excel = pandas.read_excel("dataset.xlsx")
    data = pandas.DataFrame(excel)
    return data.to_dict('records')


def rankDataset(ls, USER_PREFS):
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
            song_mag += math.pow(song[feature], 2)

            if song_feature != 0.0 and user_feature != 0.0:
                dot_product += user_feature * song_feature
        
        song_mag = math.sqrt(song_mag)
        similarity = dot_product / (user_mag * song_mag)
        song["similarity"] = similarity
        similarity_ranking.append(song)

    #sort the songs according to their similarity score
    sorted_similarity_ranking = sorted(similarity_ranking, key=lambda i: i["similarity"], reverse=True)

    return sorted_similarity_ranking


def exportDataset(rl, USER_PREFS):
    #input rl - a ranked list of songs
    #input USER_PREFS - a dictonary of the user's preferences

    output = {"similarity": [], "songName": [], "artistName": [], "albumName": [], "songID": [], "artistID": [], "albumID": [], "duration": [], "key": [], "mode": [], "time_signature": [], "acousticness": [], "danceability": [], "energy": [], "instrumentalness": [], "liveness": [], "loudness": [], "speechiness": [], "valence": [], "tempo": []}
    
    features = list(USER_PREFS.keys())
    for feature in features:
        output[feature].append(USER_PREFS[feature])

    for key in output.keys():
        if len(output[key]) == 0:
            output[key].append("-")
    
    for song in rl:
        output["similarity"].append(song["similarity"])
        output["songName"].append(song["songName"])
        output["songID"].append(song["songID"])
        output["artistName"].append(song["artistName"])
        output["artistID"].append(song["artistID"])
        output["albumName"].append(song["albumName"])
        output["albumID"].append(song["albumID"])
        output["duration"].append(song["duration"])
        output["key"].append(song["key"])
        output["mode"].append(song["mode"])
        output["time_signature"].append(song["time_signature"])
        output["acousticness"].append(song["acousticness"])
        output["danceability"].append(song["danceability"])
        output["energy"].append(song["energy"])
        output["instrumentalness"].append(song["instrumentalness"])
        output["liveness"].append(song["liveness"])
        output["loudness"].append(song["loudness"])
        output["speechiness"].append(song["speechiness"])
        output["valence"].append(song["valence"])
        output["tempo"].append(song["tempo"])

    filename = "./ranked_dataset.xlsx"
    pandas.DataFrame(output).to_excel(filename)




if __name__ == "__main__":
    main()