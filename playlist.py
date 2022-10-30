import os,sys

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

    n_plid = p.parse_playlist_id(p.create_playlist(name=pl_name))

    all_tracks = data['tracks']
    for track in all_tracks:
        song_id = p.get_song_ids(track['title'])[0]
        p.create_playlist(id=n_plid, songid=song_id)
