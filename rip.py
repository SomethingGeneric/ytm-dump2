import os,sys

from ytmusicapi import YTMusic

def check_song(title, id):
    files = os.listdir()
    found = False
    for file in files:
        if title in file and id in file:
            found = True
    return found

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
        url = f"https://www.youtube.com/watch?v={vid}"
        if not check_song(t_title, vid):
            print("Didn't find file, downloading.")
            os.system(f"youtube-dl -x --audio-format mp3 {url}")
        else:
            print("Not downloading.")
    os.chdir("../")
