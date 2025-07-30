# src/yt2mp3/mp3_converter.py
import subprocess, os
CWD = os.getcwd()

def generate(args=None, link=None, song=None, artist=None, genre=None, filename=None, subdir=None, dir=None):
    if args is not None:
        return {
            "link":args.link,
            "song":args.song,
            "artist":args.artist,
            "genre":args.genre,
            "filename":args.filename,
            "dir": args.dir if args.dir is not None else CWD,
            "subdir":args.subdir
        }
    else:
        return {
            "link": link,
            "song": song,
            "artist": artist,
            "genre": genre,
            "filename": filename,
            "dir": dir if dir is not None else CWD,
            "subdir": subdir
        }

def yt_to_mp3(output, link, filename=None):
    result = subprocess.call(["yt-dlp", "-P", output, "-x", "--audio-format", "mp3", "-o", f"{filename}.%(ext)s", link])
    return result

def handle_conversion(result, output, filename):
    if result != 0:
        return f"Conversion failed. Details: {result}"
    else:
        print(f"Successfully converted {filename}. Stored at {output}.")
        return result