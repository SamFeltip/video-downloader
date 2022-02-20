import re, os
import sys, getopt
from pytube import Playlist, YouTube

import moviepy.editor as mp

# python3 download.py "https://www.youtube.com/playlist?list=PLr99rnVSBqGAVbJuudUbRFGl-S1PuYs-5"

opts, args = getopt.getopt(sys.argv[1:], 'sa')
opts = dict(opts)

if len(args) == 0:
    print("please include album playlist")
    sys.exit()

song_urls = []

if "/playlist?" in args[0]:
    playlist = Playlist(args[0]) #"https://www.youtube.com/playlist?list=PLghz6zUnRcH-gjL9gW4WNZDJNH60q3adC"
    # this fixes the empty playlist.videos list
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

    print(len(playlist.video_urls), "songs")

    song_urls = playlist.video_urls
else:
    song_urls.append(args[0])


# playlist = Playlist('https://www.youtube.com/playlist?list=PLghz6zUnRcH-gjL9gW4WNZDJNH60q3adC')

#where to save 

current_location = "/Users/samfelton/Documents/Personal Files/mp3 editor/"
SAVE_PATH_mp4 = current_location + "resources/songs/mp4"
SAVE_PATH_mp3 = current_location + "resources/songs/mp3"
  
for i in song_urls: 
    try: 
        yt = YouTube(i) 
    except: 
          
        #to handle exception 
        print("Connection Error", i) 
      
    #filters out all the files with "mp4" extension 
    mp4files = yt.streams.filter(only_audio=True)
  
    try: 
        # download mp4 file
        out_file = mp4files.first().download(SAVE_PATH_mp4)

        print(yt.title + " has been successfully downloaded as an mp4.")

        # create mp3
        output_path_mp3 = os.path.join(SAVE_PATH_mp3, (yt.title).replace("/", "_") + ".mp3")
        clip = mp.AudioFileClip(out_file)
        clip.write_audiofile(output_path_mp3)
    except: 
        print("Some Error!") 
    
print('Task Completed!') 