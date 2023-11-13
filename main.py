import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius
import matplotlib.pyplot as plt
import numpy as np

client_id = 'withheld'
client_secret = 'withheld'
genius_access_token = 'withheld'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

genius = lyricsgenius.Genius(genius_access_token)

search_results = sp.search(q="Lucki", type="artist")
lucki_id = search_results["artists"]["items"][0]["id"]

albums = sp.artist_albums(lucki_id, album_type="album")

keywords = ["lean", "wok"]

project_names = []
average_popularity_values = []
combined_mention_counts = []

albums["items"] = sorted(albums["items"], key=lambda x: x["release_date"])

for album in albums["items"]:
    album_name = album["name"]

    tracks = sp.album_tracks(album["id"])

    popularity_sum = 0
    mention_count_sum = 0

    for track in tracks["items"]:
        track_name = track["name"]

        search_result = genius.search_song(track_name, artist="Lucki")
        if search_result:
            lyrics = search_result.lyrics.lower()
            mention_counts_dict = {keyword: lyrics.count(keyword) for keyword in keywords}

            popularity = sp.track(track["id"])["popularity"]
            popularity_sum += popularity
            mention_count_sum += sum(mention_counts_dict.values())

    average_popularity = popularity_sum / len(tracks["items"])

    project_names.append(album_name)
    average_popularity_values.append(average_popularity)
    combined_mention_counts.append(mention_count_sum)

std_deviation = np.std(combined_mention_counts)

plt.figure(figsize=(12, 6))
plt.scatter(average_popularity_values, combined_mention_counts, alpha=0.6, edgecolors='k')
plt.title("Average Popularity vs. Combined Mentions of 'Lean' and 'Wok' for Lucki's Projects")
plt.xlabel("Average Popularity")
plt.ylabel("Combined Mentions of 'Lean' and 'Wok'")
plt.grid(True)

min_x = min(average_popularity_values)
max_x = max(average_popularity_values)
min_y = min(combined_mention_counts)
max_y = max(combined_mention_counts)
slope = (max_y - min_y) / (max_x - min_x)
intercept = min_y - slope * min_x

plt.plot([min_x, max_x], [slope * min_x + intercept, slope * max_x + intercept], color='r', linestyle='--', alpha=0.3,
         label='Diagonal Line')

plt.figure(figsize=(12, 6))
plt.bar(project_names, combined_mention_counts, color='b', alpha=0.6)
plt.title("Number of Mentions of 'Lean' and 'Wok' in Lucki's Projects")
plt.xlabel("Album Name")
plt.ylabel("Number of Mentions")
plt.xticks(rotation=45, ha="right")

plt.show()
