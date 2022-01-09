from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("What date you would like to travel to? YYYY-MM-DD\n")
URL = "https://www.billboard.com/charts/hot-100/"
response = requests.get(URL + date)
soup = BeautifulSoup(response.text, "html.parser")
cls = "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only"
songs = [i.getText() for i in soup.find_all(class_=cls)]
formatted_title = [song.replace("\n", ' ') for song in songs]
#############################################################
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="2d4717295537407aad51ea2f2f43c0c1",
        client_secret="57a17ca8f1074bffbddf05890de0fbb8",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
#############################################################
song_uris = []
year = date.split("-")[0]
for song in formatted_title:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
#############################################################
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)