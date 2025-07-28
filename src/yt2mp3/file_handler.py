# src/yt2mp3/file_handler.py
import os, re
from urllib.parse import urlparse
CWD = os.getcwd()

class FileHandler:
    def __init__(self, link, dir=CWD, artist=None, song=None, genre=None, subdir=None, filename=None, song_mode=True):
        self.link = self.validate_url(link)
        self.dir = dir
        self.song_mode = song_mode

        if self.song_mode == True:
            self.get_song_mode_attr(song, artist, genre)

        elif self.song_mode == False:
            self.get_other_mode_attr(subdir, filename)

        self.output = os.path.join(self.dir, self.subdir)

    def get_song_mode_attr(self, song, artist, genre):
        self.filename = self.filename = self.sanitize_text(f"{artist.title()}_{song.title()}")
        self.subdir = self.sanitize_text(genre.title())
    
    def get_other_mode_attr(self, subdir, filename):
        self.subdir = self.sanitize_text(subdir)
        self.filename = self.sanitize_text(filename)

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