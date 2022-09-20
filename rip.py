import os,sys

from ytmusicapi import YTMusic

import youtube_dl

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

if not os.path.exists('headers_auth.json'):
    print("please run the setup")
    sys.exit(1)

ytmusic = YTMusic('headers_auth.json')

playlists = ytmusic.get_library_playlists()

pl_ids = []

for playlist in playlists:
    pl_ids.append(playlist['playlistId'])

for pl_id in pl_ids:
    data = ytmusic.get_playlist(pl_id)
    title = data['title']
    print(f"Starting {title}")
    if not os.path.exists(title):
        os.makedirs(title)
    os.chdir(title)
    tracks = data['tracks']
    for track in tracks:
        t_title = track['title']
        vid = track['videoId']
        print(f"Downloading {vid}")
        url = f"https://music.youtube.com/watch?v={vid}"
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    os.chdir("../")
