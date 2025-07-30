# src/yt2mp3/file_handler.py
import os, re
from urllib.parse import urlparse
CWD = os.getcwd()

class FileHandler:
    def __init__(self, song_mode, input_data=None):
        self.input_data = input_data
        self.song_mode = song_mode

    def _process_files(self, link, song_mode, song=None, artist=None, genre=None, dir=CWD if None else dir, subdir=None, filename=None):
        if self.input_data is None or self.song_mode is None:
            return f"Input data empty; can't set attributes."
        self.link = self.validate_url(link)
        self.dir = dir
        self.song_mode = song_mode

        if self.song_mode == True:
            self.create_filename(song, artist)
            self.subdir = self.sanitize_text(genre.title())

        elif self.song_mode == False:
            self.filename = self.sanitize_text(filename)
            self.subdir = self.sanitize_text(subdir)

        self.output = os.path.join(self.dir, self.subdir)

    def create_filename(self, song, artist):
        self.filename = self.sanitize_text(f"{artist.title()}_{song.title()}")

    def sanitize_text(self, text):
        if not isinstance(text, str):
            raise ValueError("Text must be a string")
        
        sanitized = re.sub(r'[^\w\s\-_.]', '', text)
        sanitized = sanitized.replace(' ', '-')
        sanitized = sanitized.replace(' ', '-')
        sanitized = sanitized.strip('. ')
        if not sanitized:
            raise ValueError("Text becomes empty after sanitization")
        return sanitized
    
    def validate_url(self,url):
        if not isinstance(url, str):
            raise ValueError("URL must be a string")
        try:
            parsed = urlparse(url)
            if not parsed.scheme:
                url = f"https://{url}"
                parsed = urlparse(url)
            if not parsed.netloc:
                raise ValueError("URL must have a valid domain")
            if parsed.scheme.lower() not in ['http', 'https']:
                raise ValueError("URL must use http or https protocol")
            return url
        except Exception as e:
            raise ValueError(f"Invalid URL format: {e}")