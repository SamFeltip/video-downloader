from pytube import YouTube
url = 'https://www.youtube.com/watch?v=lc7dmu4G8oc&list=PLXRKTcRs-Xs6-ocbElo4Jr8uAAggRsEdQ&index=1'

current_location = "/Users/samfelton/Documents/Personal Files/mp3 editor/"
SAVE_PATH_mp4 = current_location + "resources/songs/mp4"


from pytube import YouTube

print("imported")
# YouTube('https://youtu.be/2lAe1cqCOXo').streams.first().download()
print("downloaded")
yt = YouTube(url)
print("defined")
yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(SAVE_PATH_mp4)
print("complete")