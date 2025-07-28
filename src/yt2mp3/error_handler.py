# src/yt2mp3/error_handler.py
import os
CWD = os.getcwd()

def raise_errors(link=None, song=None, artist=None, genre=None, dir=None, subdir=None, filename=None):
    params = [link, song, artist, genre, dir, subdir, filename]
    if all(params) == None:
        raise ValueError(f"Parameters can't be empty. \nSong mode: Provide link, song, artist, and genre.\nOther: Provide link, filename, and subdirectory.")
    elif link == None:
        raise ValueError("Please provide a link.")
    elif song == None and filename == None:
        raise ValueError("Please provide either song or filename.")
    elif genre == None and subdir == None:
        raise ValueError("Please provide genre or subdirectory name.")
    return True
        
def check_song_mode_errors(song=None, artist=None, genre=None):
    song_mode_args = [song, artist, genre]
    for arg in song_mode_args:
        if arg != None:
            for empty_arg in song_mode_args:
                if empty_arg == None:
                    raise ValueError(f"{empty_arg} must be given a value if {arg} is not empty.")
                
def check_other_mode_errors(filename=None, subdir=None):
    if filename != None:
        if subdir == None:
            raise ValueError("Subdir must be given a value if filename is not empty.")
    if subdir != None:
        if subdir == None:
            raise ValueError("Filename must be given a value if subdir is not empty.")

def define_mode(song=None):
    if song != None:
        song_mode = True
        return song_mode
    elif song == None:
        song_mode = False
        return song_mode