# import openpyxl and tkinter modules
from tkinter import *
from downloadYoutube import *

# globally declare wb and sheet variable

# opening the existing excel file
# current_location = "/Users/samfelton/Documents/Personal Files/mp3 editor/"
# wb = load_workbook(current_location + 'excel.xlsx')

# create the sheet object
# sheet = wb.active

# Function to set focus (cursor)
def focus1(event):
    # set focus on the course_field box
    playlist_field.focus_set()


# Function to set focus
def focus2(event):
    # set focus on the sem_field box
    art_field.focus_set()


# Function to set focus
def focus3(event):
    # set focus on the form_no_field box
    artist_name_field.focus_set()

# Function to set focus
def focus4(event):
    # set focus on the form_no_field box
    album_name_field.focus_set()

# Function to set focus
def focus5(event):
    # set focus on the form_no_field box
    album_year_field.focus_set()

# Function to set focus
def focus6(event):
    # set focus on the form_no_field box
    album_genre_field.focus_set()

# Function to set focus
# def focus7(event):
    # set focus on the form_no_field box
    # downloading_playlist_field.focus_set()

# Function to set focus
def focus8(event):
    # set focus on the form_no_field box
    download_location_field.focus_set()


# Function for clearing the
# contents of text entry boxes
def clear():
    # clear the content of text entry box

    playlist_field.delete(0, END)
    art_field.delete(0, END)
    artist_name_field.delete(0, END)
    album_name_field.delete(0, END)
    album_year_field.delete(0, END)
    album_genre_field.delete(0, END)
    # var1.delete(0, END)


def display_message(msg):
    # create a Semester label
    # something = Label(root, text=msg, bg="black")
    something = Label(root, text=msg)
    something.grid(row=10, column=1)

# Function to take data from GUI
# window and write to an excel file
def download():
    print("downloading!")
    # if user not fill any entry
    # then print "empty input"

    # playlist_field
    # art_field
    # album_name_field
    # album_year_field

    playlist_url = playlist_field.get()
    album_art = art_field.get()
    artist_name = artist_name_field.get()
    album_name = album_name_field.get()
    album_year = album_year_field.get()
    album_genre = album_genre_field.get()
    downloading_playlist = var1.get()
    download_location = download_location_field.get()

    if (playlist_url == "" or
            album_genre == "" or
            album_year == ""):

        display_message("fill in playlist URL, genre and date")

    else:


        print(playlist_url, album_art, artist_name, album_name, album_year, album_genre, downloading_playlist, download_location_field)

        # set focus on the name_field box
        playlist_field.focus_set()

        # call the clear() function
        clear()
        display_message("downloading")

        is_collection=False
        # download_playlist(playlist_url, download_location, display_message)
        download_playlist(playlist_url, album_genre, album_year, is_collection,
                          display_message, ca_file=album_art, download_loc=download_location)

        mp4_dir="../resources/songs/temp"
        # delete mp4 files
        directory = os.fsencode(mp4_dir)

        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            os.remove(os.path.join(mp4_dir, filename))

# Driver code
if __name__ == "__main__":
    # create a GUI window
    root = Tk()


    # set the background colour of GUI window
    # root.configure(background='black')
    root.configure()

    # set the title of GUI window
    root.title("download youtube playlist")

    # set the configuration of GUI window
    root.geometry("640x400")

    # create a Form label
    heading = Label(root, text="Input data to download YouTube playlist\n and add metadata")

    # create a Name label
    # playlist_url = Label(root, text="playlist url", bg="black")
    playlist_url = Label(root, text="playlist url")

    # URL
    # thumbnail
    # album name
    # artist name
    # genre
    # year

    # create a Course label
    # thumbnail_location = Label(root, text="art file location", bg="black")
    thumbnail_location = Label(root, text="art file location")

    # create a Semester label
    # album_name = Label(root, text="Album Name", bg="black")
    album_name = Label(root, text="Album Name")

    # create a Form No. label
    # artist_name = Label(root, text="Artist Name", bg="black")
    artist_name = Label(root, text="Artist Name")

    # create a Contact No. label
    # album_genre = Label(root, text="Genre", bg="black")
    album_genre = Label(root, text="Genre")

    # create a Email id label
    # album_year = Label(root, text="Release Date", bg="black")
    album_year = Label(root, text="Release Date")

    # downloading_playlist = Label(root, text="Is Compilation", bg="black")
    downloading_playlist = Label(root, text="Is Compilation")


    # downloading_location = Label(root, text="Download Location", bg="black")
    downloading_location = Label(root, text="Download Location")

    # grid method is used for placing
    # the widgets at respective positions
    # in table like structure .
    heading.grid(row=0, column=1)
    playlist_url.grid(row=1, column=0)
    thumbnail_location.grid(row=2, column=0)
    artist_name.grid(row=3, column=0)
    album_name.grid(row=4, column=0)
    album_year.grid(row=5, column=0)
    album_genre.grid(row=6, column=0)
    downloading_location.grid(row=8, column=0)

    # create a text entry box
    # for typing the information
    playlist_field = Entry(root)
    art_field = Entry(root)
    artist_name_field = Entry(root)
    album_name_field = Entry(root)
    album_year_field = Entry(root)
    album_genre_field = Entry(root)
    download_location_field = Entry(root)


    playlist_field.bind("<Return>", focus1)

    art_field.bind("<Return>", focus2)

    artist_name_field.bind("<Return>", focus3)

    album_name_field.bind("<Return>", focus4)

    album_year_field.bind("<Return>", focus5)

    album_genre_field.bind("<Return>", focus6)

    download_location_field.bind("<Return>", focus8)
    # whenever the enter key is pressed
    # then call the focus4 function
    # form_no_field.bind("<Return>", focus4)

    # whenever the enter key is pressed
    # then call the focus5 function
    # contact_no_field.bind("<Return>", focus5)

    # whenever the enter key is pressed
    # then call the focus6 function
    # email_id_field.bind("<Return>", focus6)

    # grid method is used for placing
    # the widgets at respective positions
    # in table like structure .
    playlist_field.grid(row=1, column=1, ipadx="100")
    art_field.grid(row=2, column=1, ipadx="100")
    artist_name_field.grid(row=3, column=1, ipadx="100")
    album_name_field.grid(row=4, column=1, ipadx="100")
    album_year_field.grid(row=5, column=1, ipadx="100")
    album_genre_field.grid(row=6, column=1, ipadx="100")

    var1 = IntVar()
    # Checkbutton(root, text="Is Compilation", variable=var1, bg="black").grid(row=7, column=1, sticky=W)
    Checkbutton(root, text="Is Compilation", variable=var1).grid(row=7, column=1, sticky=W)

    download_location_field.grid(row=8, column=1, ipadx="100")

    # create a Submit Button and place into the root window
    submit = Button(root, text="Download", fg="Black", bg="Red", command=download)
    submit.grid(row=9, column=1)

    # start the GUI
    root.mainloop()