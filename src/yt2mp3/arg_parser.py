# src/yt2mp3/arg_parser.py
from argparse import ArgumentParser
import subprocess
from src.yt2mp3.file_handler import FileHandler

class MP3ConverterArgParser:
    def __init__(self, argv=None):
        self.parser = ArgumentParser()
        self.argv = argv
        self.add_arguments(self.argv)
        self.args = self.parser.parse_args(self.argv)
        self.file_handler = FileHandler(self.args.link, self.args.artist, self.args.song, self.args.genre, self.args.dir, self.args.subdir, self.args.filename)
        
    def add_arguments(self, argv=None):
        self.parser.add_argument('-l', '--link', type=str, help='provide a valid youtube link.')
        self.parser.add_argument('-s', '--song', type=str, help='provide a song title. used in file name.')
        self.parser.add_argument('-a', '--artist', type=str, help='provide an artist name. used in file name.')
        self.parser.add_argument('-g', '--genre', type=str, help='provide a genre. used as subdir.')
        self.parser.add_argument('-d', '--dir', type=str, help='provide a directory. default is cwd.')
        self.parser.add_argument('-sd', '--subdir', type=str, help='provide a subdirectory (overriden by genre)')
        self.parser.add_argument('-f', '--filename', type=str, help='provide a filename (overriden by song and artist)')
        self.yt_dlp_help = subprocess.run(['yt-dlp', '-h'], capture_output=True)
        self.parser.add_argument('-hYT', '--ytdlp-help', type=bool, help=f'yt-dlp audio/video downloader package help (these flags cannot be used in this library, only in yt-dlp): {self.yt_dlp_help.returncode}')