##Description

This program downloads videos from the internet as mp3 files and automatically adds metadata to the files based on information around the video on the webpage.

##Packages
pip install:
- eyed3 
- pytube 
- moviepy 
- glob (for metadata.py only)

brew install:
ffmpeg

Put album art from `resources/coverart.jpeg`
#Commandline Interface
for downloadandaddmetadata.py:

- -g indicates the genre of the album (default: Alternative)
- -a causes the thumbnail to be overridden by the coverart.jpg file which is present in the resources folder
- -y indicates the year the album was released (default: 2021)
- -s indicates the album is self titled, and the album will be the same as the artist's name

##Example program runs

- python3 download.py "https://www.youtube.com/playlist?list=PLr99rnVSBqGAVbJuudUbRFGl-S1PuYs-5"
- python3 metadata.py "John Lennon" "Imagine" "Rock" "1971"
- python3 downloadandaddmetadata.py -y "1967" -g "Rock" -a "https://www.youtube.com/playlist?list=PL3PhWT10BW3VDM5IcVodrdUpVIhU8f7Z-"
- 
**the configuration you'll want to use:**
- python downloadYoutube/__init__.py -g Alternative -y 2022 "https://youtube.com/playlist?list=PLfiMjLyNWxeZ4wSi-sePiHNSJ-5hPYOWp"

#User Interface
This project can also be interacted with using download_with_ui.py.
This script requires no parameters.

When filling in file paths, they must be absolute, for example:
``~/Desktop/Music/coverart.png``

NOTE: only tested on MacOS


