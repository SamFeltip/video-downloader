"""
-g indicates the genre of the album (default: Alternative)
-a causes the thumbnail to be overridden by the coverart.jpg file which is present in the resources folder
-y indicates the year the album was released (default: 2021)
-s indicates the album is self titled, and the album will be the same as the artist's name
-p creating a playlist
"""

import getopt
import os
import re
import sys

import eyed3
import moviepy.editor as mp
import requests
from eyed3.id3.frames import ImageFrame
from pytube import Playlist, YouTube

# python3 download.py "https://www.youtube.com/playlist?list=PLr99rnVSBqGAVbJuudUbRFGl-S1PuYs-5"

opts, args = getopt.getopt(sys.argv[1:], 'g:ay:s')
opts = dict(opts)

if len(args) == 0:
    print("please include album playlist")
    sys.exit()

song_urls = []

album_genre = "Alternative"
album_year = "2021"

current_location = "/Users/samfelton/Documents/Personal Files/mp3 editor/"
SAVE_PATH_mp4 = current_location + "resources/songs/mp4"
SAVE_PATH_mp3 = current_location + "resources/songs/mp3"

if "-g" in opts:
    album_genre = opts["-g"] 

if "-y" in opts:
    album_year = opts["-y"]

self_titled = "-s" in opts
overwrite_cover_art = "-a" in opts
downloading_playlist = "-p" in opts


def create_mp3(yt, artist_name, song_name, album_name, song_count):
    # create mp3
    print((yt.title).replace("/", "_") + ".mp3")
    output_path_mp3 = os.path.join(SAVE_PATH_mp3, (yt.title).replace("/", "_") + ".mp3")
    clip = mp.AudioFileClip(out_file)

    clip.write_audiofile(output_path_mp3)

    print("output path mp3", output_path_mp3)

    audiofile = eyed3.load(output_path_mp3)

    audiofile.tag.artist = artist_name + "*"
    audiofile.tag.genre = album_genre
    audiofile.tag.recording_date = album_year
    audiofile.tag.album = album_name
    audiofile.tag.album_artist = artist_name + "*"
    audiofile.tag.track_num = song_count, album_length
    audiofile.tag.title = song_name

    print("metadata added")

    if not overwrite_cover_art:
        print(yt.thumbnail_url)
        thumbnail = requests.get(yt.thumbnail_url)
        # album_art = open("resources/coverart.png", "wb")
        album_art = open("resources/coverart.png", "wb")
        album_art.write(thumbnail.content)

    # take thumbnail from youtube
    # audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(yt.thumbnail_url, 'rb').read(), 'image/jpg')

    # take thumbnail from files
    audiofile.tag.images.set(ImageFrame.FRONT_COVER, open('resources/coverart.png','rb').read(), 'image/jpeg')
    audiofile.tag.save()


def get_album_data(yt):

    artist_name = yt.author.replace(" - Topic", "").replace("Official ", "").replace("VEVO", "").strip()

    song_name = yt.title.replace("(Official Audio)", "").replace("(Official Video)", "").replace(
        "(Official Lyric Video)", "").replace(artist_name + " -", "").strip()

    if self_titled:
        if "/playlist?" in args[0]:
            album_name = playlist.title.replace("[Full Album]", "").replace("(Full Album)", "").replace("(FULL ALBUM)",
                                                                                                        "").replace(
                " - Full Album", "").replace("full album", "").strip()
        else:
            album_name = song_name + " - Single"
    elif downloading_playlist:
        album_name = song_name + " - Single"
    else:
        if "/playlist?" in args[0]:
            album_name = playlist.title.replace("FULL ALBUM", "").replace(" - Full Album", "").replace("full album",
                                                                                                       "").replace(
                "Full Album", "").replace(artist_name + " - ", "").replace(" - " + artist_name, "").replace(artist_name,
                                                                                                            "").replace(
                artist_name.lower(), "").replace("()", "").replace("[]", "").strip()
        else:
            album_name = song_name + " - Single"

    # filters out all the files with "mp4" extension

    print("artist", artist_name)
    print("song", song_name)
    print("album name", album_name)

    return artist_name, song_name, album_name


def download_video(song_url):
    print("i", song_url)

    try:
        yt = YouTube(song_url)
        mp4files = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        # download mp4 file
        out_file = mp4files.download(SAVE_PATH_mp4)
        return yt, out_file
    except:

        # to handle exception
        print("Connection Error", song_url)


playlist = Playlist(args[0])

# this fixes the empty playlist.videos list
playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

album_length = len(playlist.video_urls)
print(album_length, "songs")

song_urls = playlist.video_urls

song_count = 0
for i in song_urls:
    song_count += 1

    yt, out_file = download_video(i)
    artist_name, song_name, album_name = get_album_data(yt)
    create_mp3(yt, artist_name, song_name, album_name, song_count)

print('Task Completed!')
