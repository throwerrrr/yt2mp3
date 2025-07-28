from src.yt2mp3.mp3_converter import *
from src.yt2mp3.arg_parser import *
from src.yt2mp3.error_handler import *
from src.yt2mp3.file_handler import FileHandler

if __name__ == "__main__":

    args = parse_arguments(argv=None)

    if args.link:
        input = generate(args=args)
    else:
        input = generate(link="https://www.youtube.com/watch?v=JU2DArD9NRg", song="test_song", artist="test_artist", genre="test_genre")


    song, artist, genre = input["song"], input["artist"], input["genre"]
    dir, subdir, filename = input["dir"], input["subdir"], input["filename"]
    link = input["link"]


    raise_errors = raise_errors(link=link, song=song, artist=artist, genre=genre, dir=dir, subdir=input, filename=filename)
    if raise_errors == True:
        print("Input validated.")


    song_mode = define_mode(song=song)
    print(f"Song Mode: {song_mode}")
    if song_mode:
        check_song_mode_errors(song, artist, genre)
    else:
        check_other_mode_errors(filename, subdir)


    file_handler = FileHandler(link=link, dir=dir, artist=artist, song=song, genre=genre, subdir=subdir, filename=filename, song_mode=song_mode)
    output = file_handler.output

    # converter_result = yt_to_mp3(output="dir/subdir", link="https://www.youtube.com/watch?v=JU2DArD9NRg", filename="")
    # if converter_result = 0:
        # md_tracker = MDDataTracker(dir, current_subdir, song_mode, cache_data)