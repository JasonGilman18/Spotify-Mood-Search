import pandas
import math
import rank


def main():

    USER_PREFS = {"acousticness": .5, "danceability": .5, "energy": .5, "instrumentalness": .5, "liveness": .5, "speechiness": .5, "valence": .5}
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

    ranked_lists = (ranked_list_of_songs, ranked_list_of_artists, ranked_list_of_albums)

    score(ranked_lists)    

    rank.exportDataset(ranked_lists, USER_PREFS)


def score(ranked_lists):
    
    dcg_ground_truth_song = 0
    for x in range(len(ranked_lists[0])):
        if x >= 0 and x < 5:
            dcg_ground_truth_song  += ((math.pow(2, 8) - 1) / (math.log(x+2, 2)))
        if x >= 5 and x < 50:
            dcg_ground_truth_song  += ((math.pow(2, 7) - 1) / (math.log(x+2, 2)))
        elif x >= 50 and x < 100:
            dcg_ground_truth_song  += ((math.pow(2, 6) - 1) / (math.log(x+2, 2)))
        elif x >= 100 and x < 200:
            dcg_ground_truth_song  += ((math.pow(2, 5) - 1) / (math.log(x+2, 2)))
        elif x >= 200 and x < 300:
            dcg_ground_truth_song  += ((math.pow(2, 4) - 1) / (math.log(x+2, 2)))
        elif x >= 300 and x < 400:
            dcg_ground_truth_song  += ((math.pow(2, 3) - 1) / (math.log(x+2, 2)))
        elif x >= 400 and x < 500:
            dcg_ground_truth_song  += ((math.pow(2, 2) - 1) / (math.log(x+2, 2)))
        elif x >= 500 and x < 600:
            dcg_ground_truth_song  += ((math.pow(2, 1) - 1) / (math.log(x+2, 2)))
        else:
            dcg_ground_truth_song  += ((math.pow(2, 0) - 1) / (math.log(x+2, 2)))


    dcg_ground_truth_artist = 0
    for x in range(len(ranked_lists[1])):
        if x >= 0 and x < 7:
            dcg_ground_truth_artist  += ((math.pow(2, 7) - 1) / (math.log(x+2, 2)))
        elif x >= 7 and x < 14:
            dcg_ground_truth_artist  += ((math.pow(2, 6) - 1) / (math.log(x+2, 2)))
        elif x >= 14 and x < 27:
            dcg_ground_truth_artist  += ((math.pow(2, 5) - 1) / (math.log(x+2, 2)))
        elif x >= 27 and x < 50:
            dcg_ground_truth_artist += ((math.pow(2, 4) - 1) / (math.log(x+2, 2)))
        elif x >= 50 and x < 62:
            dcg_ground_truth_artist  += ((math.pow(2, 3) - 1) / (math.log(x+2, 2)))
        elif x >= 62 and x < 73:
            dcg_ground_truth_artist  += ((math.pow(2, 2) - 1) / (math.log(x+2, 2)))
        else:
            dcg_ground_truth_artist  += ((math.pow(2, 1) - 1) / (math.log(x+2, 2)))

    
    index = 0
    dcg_ranking_song = 0
    for song in ranked_lists[0]:
        similarity = song["similarity"]
        
        if .97 < similarity and similarity <= 1:
            dcg_ranking_song  += (math.pow(2, 8) - 1) / (math.log(index+2, 2))
        elif .94 < similarity and similarity <= .97:
            dcg_ranking_song  += (math.pow(2, 7) - 1) / (math.log(index+2, 2))
        elif .90 < similarity and similarity <= .94:
            dcg_ranking_song  += (math.pow(2, 6) - 1) / (math.log(index+2, 2))
        elif .85 < similarity and similarity <= .90:
            dcg_ranking_song  += (math.pow(2, 5) - 1) / (math.log(index+2, 2))
        elif .79 < similarity and similarity <= .85:
            dcg_ranking_song  += (math.pow(2, 4) - 1) / (math.log(index+2, 2))
        elif .72 < similarity and similarity <= .79:
            dcg_ranking_song  += (math.pow(2, 3) - 1) / (math.log(index+2, 2))
        elif .64 < similarity and similarity <= .72:
            dcg_ranking_song  += (math.pow(2, 2) - 1) / (math.log(index+2, 2))
        elif .55 < similarity and similarity <= .64:
            dcg_ranking_song  += (math.pow(2, 1) - 1) / (math.log(index+2, 2))
        else:
            dcg_ranking_song  += (math.pow(2, 0) - 1) / (math.log(index+2, 2))

        index += 1

    
    index = 0
    dcg_ranking_artist = 0
    for artist in ranked_lists[1]:
        similarity = artist["similarity"]

        if .97 < similarity and similarity <= 1:
            dcg_ranking_artist  += (math.pow(2, 8) - 1) / (math.log(index+2, 2))
        elif .94 < similarity and similarity <= .97:
            dcg_ranking_artist  += (math.pow(2, 7) - 1) / (math.log(index+2, 2))
        elif .90 < similarity and similarity <= .94:
            dcg_ranking_artist  += (math.pow(2, 6) - 1) / (math.log(index+2, 2))
        elif .85 < similarity and similarity <= .90:
            dcg_ranking_artist  += (math.pow(2, 5) - 1) / (math.log(index+2, 2))
        elif .79 < similarity and similarity <= .85:
            dcg_ranking_artist  += (math.pow(2, 4) - 1) / (math.log(index+2, 2))
        elif .72 < similarity and similarity <= .79:
            dcg_ranking_artist  += (math.pow(2, 3) - 1) / (math.log(index+2, 2))
        elif .64 < similarity and similarity <= .72:
            dcg_ranking_artist  += (math.pow(2, 2) - 1) / (math.log(index+2, 2))
        elif .55 < similarity and similarity <= .64:
            dcg_ranking_artist  += (math.pow(2, 1) - 1) / (math.log(index+2, 2))
        else:
            dcg_ranking_artist  += (math.pow(2, 0) - 1) / (math.log(index+2, 2))

        index += 1


    ndcg_score_song = dcg_ranking_song / dcg_ground_truth_song 
    ndcg_score_artist = dcg_ranking_artist / dcg_ground_truth_artist
    
    print("NDCG Ranking Scores\n\n")
    print("Num Songs: ", len(ranked_lists[0]), "\n")
    print("Song DCG Ground Truth: ", dcg_ground_truth_song , "\n")
    print("Song DCG Ranking: ", dcg_ranking_song , "\n\n")
    print("Song NDCG Ranking: ", ndcg_score_song, '\n\n')
    print("Num Artists: ", len(ranked_lists[1]), "\n")
    print("Artist DCG Ground Truth: ", dcg_ground_truth_artist , "\n")
    print("Artist DCG Ranking: ", dcg_ranking_artist , "\n\n")
    print("Artist NDCG Ranking: ", ndcg_score_artist, '\n\n')


if __name__ == "__main__":
    main()