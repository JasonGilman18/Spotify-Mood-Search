import requests
import time
import pandas
import urllib.request
import config


def main():
    api_key = config.api_key
    api_secret = config.api_secret
    accessToken = authorize(api_key, api_secret)

    artistNames = config.artist_names

    for name in artistNames:
        
        
        response = getArtist(name, accessToken)
        url = response["artists"]["items"][0]["images"][1]["url"]
        filename = "./../img/" + response["artists"]["items"][0]["id"] + ".png"
        urllib.request.urlretrieve(url, filename)


        artistID = response["artists"]["items"][0]["id"]
        albums = getArtistAlbums(artistID, accessToken)
        for album in albums:
            album_filename = "./../img/" + album[1] + ".png"
            album_url = album[0]
            urllib.request.urlretrieve(album_url, album_filename)

    



# Helper functions =============================================
def authorize(api_key, api_secret):
    url = "https://accounts.spotify.com/api/token"
    body = {"grant_type": "client_credentials"}
    auth = (api_key, api_secret)
    response = requests.post(url, auth=auth, data=body)
    data = response.json()
    return data["access_token"]


def getArtist(artistName, accessToken):
    url = "https://api.spotify.com/v1/search" + "?q=" + artistName + "&type=artist"
    header = {"Authorization": "Bearer " + accessToken}
    response = requests.get(url, headers=header)
    data = response.json()
    if response.status_code==200:
        return data
    else:
        return ""    


def getArtistAlbums(artistID, accessToken):
    url = "https://api.spotify.com/v1/artists/" + artistID + "/albums" + "?market=US&include_groups=album&limit=10"
    header = {"Authorization": "Bearer " + accessToken}
    response = requests.get(url, headers=header)
    data = response.json()
    albums = []
    if response.status_code==200:
        for album in data["items"]:
            if (album["name"].lower()).find("deluxe") == -1 and (album["name"].lower()).find("remastered") == -1 and (album["name"].lower()).find("remastered") == -1 and (album["name"].lower()).find("remaster") == -1 and (album["name"].lower()).find("remix") == -1 and (album["name"].lower()).find("commentary") == -1 and (album["name"].lower()).find("track by track") == -1:
                albums.append((album["images"][1]["url"], album["id"]))
    return albums


if __name__ == "__main__":
    main()