import os, json, datetime, re
from src.yt2mp3.md_file import MDFile
from src.yt2mp3.md_formatter import MDFormatter
from src.yt2mp3.cache import Cache

class MDTracker:
    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.title = os.path.basename(self.file_handler.dir)
        self.md_filepath = os.path.join(self.file_handler.dir, f"{self.title}.md")
        self.subdirs = {}
        self.md_file = self.check_for_md_file()
        self.discover_all_subdirs()
        self.formatter = MDFormatter(self.md_file, self.subdirs)
        self.formatted_file = self.format_md_file()
        self._save_file(self.formatted_file)

    def check_for_md_file(self):
        if os.path.exists(self.md_filepath):
            print("MD File exists. Creating file and loading data from cache.") # DEBUG
            md_file = MDFile(file_name=f"{self.title}.md", dir=self.file_handler.dir, md_title=self.title)
            print("File created.")
            meta_data = Cache()._load_from_cache()
            if meta_data and isinstance(meta_data, dict) and 'id' in meta_data:
                print(f"Cache loaded. Last save id: {meta_data['id']}")

                if 'subdirs' in meta_data and isinstance(meta_data['subdirs'], dict):
                    cached_subdirs = meta_data['subdirs']
                    print(f"Loaded {len(cached_subdirs)} subdirectories from cache")
                else:
                    cached_subdirs = {}
                # Store cached subdirs for later merging in discover_all_subdirs
                self.cached_subdirs = cached_subdirs
            else:
                print("No valid cache data found")
                self.cached_subdirs = {}
            return md_file
        else:
            print(f"MD File at {self.md_filepath} does not exist. Creating file.")
            self.cached_subdirs = {}
            return MDFile(file_name=f"{self.title}.md", dir=self.file_handler.dir, md_title=self.title)

    def discover_all_subdirs(self):
        try:
            self.subdirs = getattr(self, 'cached_subdirs', {}).copy()
            
            dir_contents = os.listdir(self.file_handler.dir)
            
            for item in dir_contents:
                item_path = os.path.join(self.file_handler.dir, item)
            
                if os.path.isdir(item_path):
                    
                    if item not in self.subdirs:
                        self.subdirs[item] = {"is_genre": True}
            
            existing_subdirs = {subdir: metadata for subdir, metadata in self.subdirs.items() 
                              if os.path.isdir(os.path.join(self.file_handler.dir, subdir))}
            self.subdirs = existing_subdirs
            self.subdirs[self.file_handler.subdir] = {"is_genre": self.file_handler.is_song}
            print(f"Discovered {len(self.subdirs)} total subdirectories: {list(self.subdirs.keys())}")
        except OSError as e:
            print(f"Error scanning directory {self.file_handler.dir}: {e}")
            self.subdirs = {self.file_handler.subdir: {"is_genre": self.file_handler.is_song}}

    def format_md_file(self):
        return self.formatter.return_md_file()
    
    def _save_file(self, md_file):
        md_file.subdirs = self.subdirs
        cache_save = Cache(md_file)._save_to_cache()
        if cache_save is True:
            md_file.create_md_file()
            return True
        else:
            print("Process interrupted while saving to Cache.")
            return False