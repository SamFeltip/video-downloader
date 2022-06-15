import eyed3
import sys, getopt
import glob


from eyed3.id3.frames import ImageFrame

# python3 metadata.py "John Lennon" "Imagine" "Rock" "1971"

opts, args = getopt.getopt(sys.argv[1:], 'sa')
opts = dict(opts)

if len(args) < 1:
    print("please include album name and artist name")
    sys.exit()


artist_name = args[0] #"Jessie Ware"
album_name = args[1] #"What’s Your Pleasure?"

album_genre = "Alternative"
if len(args) > 2:
    album_genre = args[2] #pop

album_year = "2020"
if len(args) > 3:
    album_year = args[3]

print(artist_name)
print(album_name)


song_files = glob.glob("resources/songs/mp3/*.mp3") 
print("----", song_files)

# songs = []

songs_from_files = [s.replace("resources/songs/mp3/", "").replace(".mp3", "") for s in song_files]

# (position, song name)
split_songs = [(int(s[:2]), s[3:]) for s in songs_from_files]

print(songs_from_files)
print(split_songs)

# for (song_index, song_name) in split_songs:
for song_file_index in range(len(song_files)):
    

    (track_num, song_name) = split_songs[song_file_index]

    print("operating on", song_name, "...")

    print(song_file_index)
    print(song_files)
    print(song_files[song_file_index])

    audiofile = eyed3.load(song_files[song_file_index])

    audiofile.tag.artist = artist_name
    audiofile.tag.album_genre = album_genre
    audiofile.tag.recording_date = album_year
    audiofile.tag.album = album_name
    audiofile.tag.album_artist = artist_name + "*"
    audiofile.tag.track_num = track_num, len(songs_from_files)
    audiofile.tag.title = song_name

    audiofile.tag.images.set(ImageFrame.FRONT_COVER, open('resources/coverart.jpeg','rb').read(), 'image/jpeg')
    audiofile.tag.save()


print("done!")