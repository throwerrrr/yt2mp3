# src/yt2mp3/mp3_converter.py
import subprocess

def generate(args=None, link=None, song=None, artist=None, genre=None, filename=None, subdir=None, dir=None):
    if args is not None:
        return {
            "link":args.link,
            "song":args.song,
            "artist":args.artist,
            "genre":args.genre,
            "filename":args.filename,
            "dir": args.dir,
            "subdir":args.subdir
        }
    else:
        return {
            "link": link,
            "song": song,
            "artist": artist,
            "genre": genre,
            "filename": filename,
            "dir": dir,
            "subdir": subdir
        }

def yt_to_mp3(output, link, filename=None):
    result = subprocess.call(["yt-dlp", "-P", output, "-x", "--audio-format", "mp3", "-o", f"{filename}.%(ext)s", link])
    return result