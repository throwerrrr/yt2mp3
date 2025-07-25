# src/yt2mp3/file_handler.py
import os, re
from urllib.parse import urlparse

CWD = os.getcwd()

class FileHandler:
    def __init__(self, link, artist=None, song=None, genre=None, dir=CWD, subdir=None, filename=None):
        self.link = self.validate_url(link)
        self.dir = dir
        if song != None and isinstance(song, str) == True:
            if artist == None or not isinstance(artist, str):
                raise ValueError(f"Artist parameter invalid. Must be valid if song parameter is passed.")
            if genre == None or not isinstance(genre, str):
                raise ValueError(f"Genre parameter invalid. Must be valid if song parameter is passed.")
            self.song = song.title()
            self.artist = artist.title()
            self.genre = genre.title()
            self.subdir = self.sanitize_text(self.genre)
            self.filename = self.sanitize_text(f"{self.artist}_{self.song}")
            self.is_song = True
        else:
            self.song, self.artist, self.genre = None, None, None
            self.is_song = False
            if subdir == None:
                raise ValueError(f"Must specify subdirectory if no song")
            self.filename = self.sanitize_text(filename)
            self.subdir = self.sanitize_text(subdir)
        os.makedirs(os.path.join(self.dir, self.subdir), exist_ok=True)
        self.output = os.path.join(self.dir, self.subdir)

    def sanitize_text(self, text):
        if not isinstance(text, str):
            raise ValueError("Text must be a string")
        
        sanitized = re.sub(r'[^\w\s\-_.]', '', text)
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
            valid_domains = ['youtube.com', 'www.youtube.com', 'youtu.be', 'm.youtube.com']
            
            if parsed.netloc.lower() not in valid_domains:
                raise ValueError(f"URL must be from YouTube. Got: {parsed.netloc}")
            return url
        
        except Exception as e:
            raise ValueError(f"Invalid URL format: {e}")