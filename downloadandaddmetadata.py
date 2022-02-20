"""
-g indicates the genre of the album (default: Alternative)
-a causes the thumbnail to be overridden by the coverart.jpg file which is present in the resources folder
-y indicates the year the album was released (default: 2021)
-s indicates the album is self titled, and the album will be the same as the artist's name
-p creating a playlist
"""

import re, os
import sys, getopt
from urllib import request
from pytube import Playlist, YouTube

import moviepy.editor as mp
import requests

import eyed3
import sys, getopt

from eyed3.id3.frames import ImageFrame

# python3 download.py "https://www.youtube.com/playlist?list=PLr99rnVSBqGAVbJuudUbRFGl-S1PuYs-5"

opts, args = getopt.getopt(sys.argv[1:], 'g:ay:s')
opts = dict(opts)

if len(args) == 0:
    print("please include album playlist")
    sys.exit()

song_urls = []

album_genre = "Alternative"
album_year = "2021"

if "-g" in opts:
    album_genre = opts["-g"] 

if "-y" in opts:
    album_year = opts["-y"]

self_titled = "-s" in opts
overwrite_cover_art = "-a" in opts
downloading_playlist = "-p" in opts

if "/playlist?" in args[0]:
    playlist = Playlist(args[0]) #"https://www.youtube.com/playlist?list=PLghz6zUnRcH-gjL9gW4WNZDJNH60q3adC"

    # print("album nume:", playlist.title.replace("(Full Album)", "").replace("Full Album", ""))

    # this fixes the empty playlist.videos list
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

    album_length = len(playlist.video_urls)
    print(album_length, "songs")

    song_urls = playlist.video_urls
else:
    song_urls.append(args[0])


# playlist = Playlist('https://www.youtube.com/playlist?list=PLghz6zUnRcH-gjL9gW4WNZDJNH60q3adC')

#where to save 

current_location = "/Users/samfelton/Documents/Personal Files/mp3 editor/"
SAVE_PATH_mp4 = current_location + "resources/songs/mp4"
SAVE_PATH_mp3 = current_location + "resources/songs/mp3"
  
song_count = 0
for i in song_urls: 
    song_count += 1

    try: 
        yt = YouTube(i) 
    except: 
          
        #to handle exception 
        print("Connection Error", i) 
      
    artist_name = yt.author.replace(" - Topic", "").replace("Official ", "").replace("VEVO", "").strip()

    song_name = yt.title.replace("(Official Audio)", "").replace("(Official Video)", "").replace("(Official Lyric Video)", "").replace(artist_name + " -", "").strip()

    if self_titled:
        album_name = playlist.title.replace("[Full Album]", "").replace("(Full Album)", "").replace("(FULL ALBUM)", "").replace(" - Full Album", "").replace("full album", "").strip()
    elif downloading_playlist:
        album_name = song_name + " - Single"
    else:
        album_name = playlist.title.replace("[Full Album]", "").replace("(Full Album)", "").replace("(FULL ALBUM)", "").replace(" - Full Album", "").replace("full album", "").replace(artist_name + " - ", "").replace(" - " + artist_name, "").replace(artist_name, "").replace(artist_name.lower(), "").strip()
    
    

    #filters out all the files with "mp4" extension

    print("artist", artist_name)
    print("song", song_name)
    print("album name", album_name)

    mp4files = yt.streams.filter(only_audio=True)
  
    try: 
        # download mp4 file
        out_file = mp4files.first().download(SAVE_PATH_mp4)

        # print(yt.title + " has been successfully downloaded as an mp4.")

        # create mp3
        output_path_mp3 = os.path.join(SAVE_PATH_mp3, (yt.title).replace("/", "_") + ".mp3")
        clip = mp.AudioFileClip(out_file)
        clip.write_audiofile(output_path_mp3)

        print(output_path_mp3)

        audiofile = eyed3.load(output_path_mp3)

        audiofile.tag.artist = artist_name
        audiofile.tag.genre = album_genre
        audiofile.tag.recording_date = album_year
        audiofile.tag.album = album_name
        audiofile.tag.album_artist = artist_name + "*"
        audiofile.tag.track_num = song_count, album_length
        audiofile.tag.title = song_name

        if not overwrite_cover_art:
            print(yt.thumbnail_url)
            thumbnail = requests.get(yt.thumbnail_url)
            album_art = open("resources/coverart.jpg", "wb")
            album_art.write(thumbnail.content)

        # audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(yt.thumbnail_url, 'rb').read(), 'image/jpg')
        audiofile.tag.images.set(ImageFrame.FRONT_COVER, open('resources/coverart.jpg','rb').read(), 'image/jpeg')
        audiofile.tag.save()

    except: 
        print("Some Error!") 
    
print('Task Completed!') 