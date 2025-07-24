# src/yt2mp3/mp3_converter.py
import subprocess
from src.yt2mp3.arg_parser import MP3ConverterArgParser
from src.yt2mp3.file_handler import FileHandler
from src.yt2mp3.md_tracker import MDTracker

class MP3Converter:
    def __init__(self, argv=None, link=None, artist=None, song=None, genre=None, subdir=None, dir=None, filename=None):
        if argv is not None or all(param is None for param in [link, artist, song, genre, dir, subdir, filename]):
            self.arg_parser = MP3ConverterArgParser(argv)
            self.file_handler = self.arg_parser.file_handler
        else:
            self.arg_parser = None
            self.file_handler = FileHandler(link, artist, song, genre, dir, subdir, filename)
        self.run_command()
    
    def run_command(self):
        result = subprocess.call(["yt-dlp", "-P", self.file_handler.output, "-x", "--audio-format", "mp3", "-o", f"{self.file_handler.filename}.%(ext)s", self.file_handler.link])
        if result == 0:
            md_tracker = MDTracker(self.file_handler)