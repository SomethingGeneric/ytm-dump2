import os,sys
import getpass

from ytmusicapi import YTMusic

import youtube_dl

from pysubsonic import pysubsonic

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

def check_song(title, id):
    files = os.listdir()
    found = False
    for file in files:
        if id in file:
            found = True
        if title is not None and title in file:
            found = True
    return found


if not os.path.exists('headers_auth.json'):
    print("please run the setup")
    sys.exit(1)

ytmusic = YTMusic('headers_auth.json')

playlists = ytmusic.get_library_playlists()

pl_ids = []

failed = []

p = pysubsonic("https://music.xhec.dev", "matt", getpass.getpass(prompt="Password: "))

for playlist in playlists:
    if "likes" not in playlist['title'].lower():
        pl_ids.append(playlist['playlistId'])

for pl_id in pl_ids:
    data = ytmusic.get_playlist(pl_id)
    pl_name = data['title']
    print("Working on " + pl_name)

    all_tracks = data['tracks']

    pl_id = p.parse_playlist_id(p.create_playlist(name=pl_name))

    for track in all_tracks:
        print(f"Working on {track['title']}")
        songs = p.get_song_ids(track['title'])
        if len(songs) != 0:
            song_id = songs[0]
            p.update_playlist(pl_id, song_id)
            print("Added " + track['title'])
        else:
            print("Failed to add " + track['title'])

    print("---------------------------------------------------")