import requests
import time
import pandas
import config


def main():
    print("started...")
    startTime = time.time()

    api_key = config.api_key
    api_secret = config.api_secret
    accessToken = authorize(api_key, api_secret)

    artistNames = ["The Weeknd", "Drake", "Justin Beiber", "J Balvin", "Dua Lipa", "Cardi B", "Ed Sheeran", "Ariana Grande", "Marshmello", "Khalid", "Jason Derulo", "Travis Scott", "Lady Gaga", "Maroon 5", "Post Malone", "Harry Styles", "Halsey", "Bad Bunny", "Selena Gomez", "Coldplay", "Billie Elish", "Rihanna", "Eminem", "Taylor Swift", "Imagine Dragons", "Shawn Mendes", "Queen", "Bruno Mars", "Beyonce", "Ozuna", "Alan Walker", "BTS", "Adele"]
    data = createData(artistNames, accessToken)

    endTime = time.time()
    finalTime = time.strftime("%H:%M:%S", time.gmtime((int)(endTime-startTime)))
    filename = "./dataset.xlsx"
    pandas.DataFrame(data["output"]).to_excel(filename)

    print("ended... took " + finalTime)




# Helper functions =============================================
def createData(artistNames, accessToken):
    whichArtist = 0
    data = {"artists": []}
    output = {"songName": [], "artistName": [], "albumName": [], "songID": [], "artistID": [], "albumID": [], "duration": [], "key": [], "mode": [], "time_signature": [], "acousticness": [], "danceability": [], "energy": [], "instrumentalness": [], "liveness": [], "loudness": [], "speechiness": [], "valence": [], "tempo": []}
    for artistName in artistNames:
        artistID = getArtistId(artistName, accessToken)
        data["artists"].append({"artistName": artistName, "artistID": artistID, "albums": []})

        whichAlbum = 0
        finishOut = True
        albums = getArtistAlbums(artistID, accessToken)
        for album in albums:
            if whichAlbum > 0:
                finishOut = data["artists"][whichArtist]["albums"][whichAlbum-1]["albumName"] != album["albumName"] and "deluxe" not in album["albumName"]
                    
            if finishOut:
                data["artists"][whichArtist]["albums"].append({"albumName": album["albumName"], "albumID": album["albumID"], "songs": []})

                songs = getAlbumSongs(album["albumID"], accessToken)
                for song in songs:
                    attributes = getSongAttributes(song["songID"], accessToken)
                    data["artists"][whichArtist]["albums"][whichAlbum]["songs"].append({"songName": song["songName"], "songID": song["songID"], "attributes": attributes})
                    output["songName"].append(song["songName"])
                    output["songID"].append(song["songID"])
                    output["artistName"].append(artistName)
                    output["artistID"].append(artistID)
                    output["albumName"].append(album["albumName"])
                    output["albumID"].append(album["albumID"])
                    output["duration"].append(attributes["duration"])
                    output["key"].append(attributes["key"])
                    output["mode"].append(attributes["mode"])
                    output["time_signature"].append(attributes["time_signature"])
                    output["acousticness"].append(attributes["acousticness"])
                    output["danceability"].append(attributes["danceability"])
                    output["energy"].append(attributes["energy"])
                    output["instrumentalness"].append(attributes["instrumentalness"])
                    output["liveness"].append(attributes["liveness"])
                    output["loudness"].append(attributes["loudness"])
                    output["speechiness"].append(attributes["speechiness"])
                    output["valence"].append(attributes["valence"])
                    output["tempo"].append(attributes["tempo"])
            whichAlbum += 1
        whichArtist += 1
    return {"data": data, "output": output}

       
def authorize(api_key, api_secret):
    url = "https://accounts.spotify.com/api/token"
    body = {"grant_type": "client_credentials"}
    auth = (api_key, api_secret)
    response = requests.post(url, auth=auth, data=body)
    data = response.json()
    return data["access_token"]


def getArtistId(artistName, accessToken):
    url = "https://api.spotify.com/v1/search" + "?q=" + artistName + "&type=artist"
    header = {"Authorization": "Bearer " + accessToken}
    response = requests.get(url, headers=header)
    data = response.json()
    if response.status_code==200:
        return data["artists"]["items"][0]["id"]
    else:
        return ""    


def getArtistAlbums(artistID, accessToken):
    url = "https://api.spotify.com/v1/artists/" + artistID + "/albums" + "?market=US&include_groups=album&limit=1"
    header = {"Authorization": "Bearer " + accessToken}
    response = requests.get(url, headers=header)
    data = response.json()
    albums = []
    if response.status_code==200:
        for album in data["items"]:
            albums.append({"albumName": album["name"], "albumID": album["id"]})
    return albums


def getAlbumSongs(albumID, accessToken):
    url = "https://api.spotify.com/v1/albums/" + albumID + "/tracks" + "?market=US"
    header = {"Authorization": "Bearer " + accessToken}
    response = requests.get(url, headers=header)
    data = response.json()
    songs = []
    if response.status_code==200:
        for song in data["items"]:
            songs.append({"songName": song["name"], "songID": song["id"]})
    return songs


def getSongAttributes(songID, accessToken):
    url = "https://api.spotify.com/v1/audio-features/" + songID
    header = {"Authorization": "Bearer " + accessToken}
    response = requests.get(url, headers=header)
    data = response.json()
    time.sleep(.05)
    if response.status_code==200:
        attributes = {"duration": data["duration_ms"], "key": data["key"], "mode": data["mode"], "time_signature": data["time_signature"], "acousticness": data["acousticness"], "danceability": data["danceability"], "energy": data["energy"], "instrumentalness": data["instrumentalness"], "liveness": data["liveness"], "loudness": data["loudness"], "speechiness": data["speechiness"], "valence": data["valence"], "tempo": data["tempo"]}
    else:
        attributes = {}
    return attributes


if __name__ == "__main__":
    main()