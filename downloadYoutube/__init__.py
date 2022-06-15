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

def create_mp3(yt, out_file, artist_name, song_name, album_name, album_genre, album_year, song_count, album_length, ca_file="", download_loc="../resources/songs/mp3"):
    """
    create mp3 file once mp4 is downloaded
    :param album_year:
    :param album_genre:
    :param yt: YouTube object for the song being rendered
    :param out_file: output of the mp4
    :param artist_name:
    :param song_name:
    :param album_name:
    :param song_count:
    :param album_length:
    """

    if ca_file == "":
        cwd = os.getcwd()
        ca_file = os.path.join(cwd, "resources/coverart.png")

    # create mp3
    # print((yt.title).replace("/", "_") + ".mp3")

    abs_download_path = download_loc
    if download_loc != "../resources/songs/mp3":
        abs_download_path = os.path.expanduser(download_loc)


    output_path_mp3 = os.path.join(abs_download_path, album_name.replace(' ', '') + '_' + (yt.title).replace("/", "_").replace(' ', '') + ".mp3")
    clip = mp.AudioFileClip(out_file)

    clip.write_audiofile(output_path_mp3)

    # print("output path mp3", output_path_mp3)

    audiofile = eyed3.load(output_path_mp3)

    audiofile.tag.artist = artist_name + "*"
    audiofile.tag.album_genre = album_genre
    audiofile.tag.recording_date = album_year
    audiofile.tag.album = album_name
    audiofile.tag.album_artist = artist_name + "*"
    audiofile.tag.track_num = song_count, album_length
    audiofile.tag.title = song_name

    if ca_file == '':
        thumbnail = requests.get(yt.thumbnail_url)
        album_art = open(ca_file, "wb")
        album_art.write(thumbnail.content)

    # take thumbnail from youtube
    # audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(yt.thumbnail_url, 'rb').read(), 'image/jpg')

    # take thumbnail from files
    audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(ca_file,'rb').read(), 'image/png')
    audiofile.tag.save()


def get_album_data(yt, playlist, downloading_playlist, playlist_url):

    artist_name = yt.author.replace(" - Topic", "").replace("Official ", "").replace("VEVO", "").strip()

    song_name = yt.title.replace("(Official Audio)", "").replace("(Official Video)", "").replace(
        "(Official Lyric Video)", "").replace(artist_name + " -", "").strip()

    if downloading_playlist:
        album_name = song_name + " - Single"
    else:
        if "/playlist?" in playlist_url:
            album_name = playlist.title.replace("FULL ALBUM", "").replace(" - Full Album", "").replace("full album",
                                                                                                       "").replace(
                "Full Album", "").replace(artist_name + " - ", "").replace(" - " + artist_name, "").replace(artist_name,
                                                                                                            "").replace(
                artist_name.lower(), "").replace("()", "").replace("[]", "").strip()
        else:
            album_name = song_name + " - Single"

    # filters out all the files with "mp4" extension
    #
    # print("artist", artist_name)
    # print("song", song_name)
    # print("album name", album_name)

    return artist_name, song_name, album_name


def download_video(song_url, download_loc):

    try:
        yt = YouTube(song_url)
        mp4files = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        # download mp4 file
        out_file = mp4files.download(download_loc)
        return yt, out_file
    except:

        # to handle exception
        print("Connection Error", song_url)


def pull_arguments(opts, args):

    # opts, args = getopt.getopt(sys.argv[1:], 'g:y:p')
    # opts = dict(opts)

    if len(args) == 0:
        print("please include album playlist")
        sys.exit()


    album_genre = "Alternative"
    album_year = "2021"
    ca_png = ""

    if "-g" in opts:
        album_genre = opts["-g"]

    if "-y" in opts:
        album_year = opts["-y"]

    if "-c" in opts:
        ca_png = os.path.expanduser(opts["-c"])

    downloading_playlist = "-p" in opts

    return album_genre, album_year, downloading_playlist, ca_png


def download_playlist(playlist_url, album_genre, album_year, downloading_playlist, f=print, artist_name="", album_name="", ca_file="../resources/coverart.png", download_loc="../resources/songs/mp3"):
    """
    :param playlist_url:
    :param album_genre:
    :param album_year:
    :param downloading_playlist:
    :param f:function for printing download process
    :param artist_name:
    :param album_name:
    :param ca_file: cover art file
    :param download_loc: output dir
    """
    playlist = Playlist(playlist_url)

    # is not used becasue we are moving away from using pythong arguments
    # inferred_album_genre, inferred_album_year, dp = pull_arguments()

    # this fixes the empty playlist.videos list
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

    album_length = len(playlist.video_urls)
    f(str(album_length) + "songs")

    song_urls = playlist.video_urls

    song_count = 0
    for i in song_urls:

        song_count += 1

        yt, out_file = download_video(i, "../resources/songs/temp")
        inferred_artist_name, song_name, inferred_album_name = get_album_data(yt, playlist, downloading_playlist, playlist_url)

        if artist_name == "":
            artist_name = inferred_artist_name
        if album_name == "" or downloading_playlist:
            album_name = inferred_album_name

        f("song " + str(song_count) + '/' + str(album_length) + ": " + str(song_name))

        create_mp3(yt, out_file, artist_name, song_name, album_name, album_genre, album_year, song_count, album_length, ca_file=ca_file, download_loc=download_loc)


if __name__ == "__main__":

    opts, args = getopt.getopt(sys.argv[1:], 'g:y:c:p')
    opts = dict(opts)

    output_dir = args[1]

    print(opts, args,"\n")
    # mp3_dir = os.path.join(output_dir, "songs/mp3")
    mp4_dir = "../resources/songs/temp" #os.path.join(resources_dir, "songs/mp4")

    cwd = os.getcwd()
    SAVE_PATH_mp4 = os.path.join(cwd, mp4_dir)
    # SAVE_PATH_mp3 = os.path.join(cwd, mp3_dir)

    playlist_url = args[0]
    is_collection = "-p" in opts

    album_genre, album_year, downloading_playlist, ca_png = pull_arguments(opts, args)
    # ca_png = os.path.join(resources_dir, "coverart.png")

    download_playlist(playlist_url, album_genre, album_year, is_collection, print, ca_file=ca_png, download_loc=output_dir)

    # delete mp4 files
    directory = os.fsencode(mp4_dir)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        os.remove(os.path.join(mp4_dir, filename))

    print('Task Completed!')


