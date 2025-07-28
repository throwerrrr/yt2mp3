import os, json, datetime, re
from src.yt2mp3.md_file import MDFile
from src.yt2mp3.md_formatter import MDFormatter
from src.yt2mp3.cache import Cache

class MDDataTracker:
    def __init__(self, dir, current_subdir, song_mode, cache_data):
        self.dir = dir
        self.current_subdir = current_subdir
        self.md_filepath = os.path.join(dir, f"{self.title}.md")
        self.md_file = self.check_for_md_file()
        self.cache_data = self._check_cache_data(cache_data)
        self.cached_subdirs = self._get_cached_subdirectories(self.cache_data)
        self.subdirs = self._discover_all_subdirs(dir, current_subdir, song_mode)

    def check_if_md_file_exists(self):
        if os.path.exists(self.md_filepath):
            print("MD File exists.")
            return True
        else:
            print("MD File does not exist.")
            return False
        
    def _check_cache_data(self, cache_data):
        if not isinstance(cache_data, dict):
            raise TypeError()
        if any(key not in list(cache_data.keys()) for key in ["id", "date", "title", "dir", "author", "file_data_text", "subdirs"]):
            raise ValueError(f"Cache data invalid.")
        elif not isinstance(cache_data["subdirs"], dict):
            raise TypeError(f"Invalid cache data. Subdir key should be dict, but is {type(cache_data["subdirs"])}")
        elif not isinstance(cache_data["title"], str):
            raise TypeError(f"Invalid cache data. Title key should be str, but is {type(cache_data["title"])}")
        elif not isinstance(cache_data["dir"], str):
            raise TypeError(f"Invalid cache data. Dir key should be str, but is {type(cache_data["dir"])}")
        elif not isinstance(cache_data["author"], str):
            raise TypeError(f"Invalid cache data. Author key should be str, but is {type(cache_data["author"])}")
        elif not isinstance(cache_data["file_data_text", str]):
            raise TypeError(f"Invalid cache data. File_data_text key should be dict, but is {type(cache_data["file_data_text"])}")
        else:
            print("Cache data is clean!")
            return cache_data
    
    def get_last_save_id(self, cache_data):
        meta_data = cache_data
        if meta_data and isinstance(meta_data, dict) and "id" in meta_data:
            print(f"Cache loaded.")
            print(f"Last save id: {meta_data["id"]}")
    
    def _get_cached_subdirectories(self, cache_data):
        meta_data = cache_data
        if meta_data and isinstance(meta_data, dict) and "id" in meta_data:
            if "subdirs" in meta_data and isinstance(meta_data["subdirs"], dict):
                cached_subdirs = meta_data["subdirs"]
                print(f"Loaded {len(cached_subdirs)} subdirectories from cache")
            else:
                cached_subdirs = {}
            self.cached_subdirs = cached_subdirs
        else:
            print("No valid cache data found")
            self.cached_subdirs = {}

    def get_dir_list(self, dir):
        try:
            dir_contents = os.listdir(dir)
            return dir_contents
        except OSError as e:
            print(f"Error scanning directory {dir}: {e}")
            return []
        
    def _discover_all_subdirs(self, dir, dir_contents, current_subdir, song_mode):
        try:
            for item in dir_contents:
                item_path = os.path.join(dir, item)
                if os.path.isdir(item_path):
                    if item not in self.subdirs:
                        self.subdirs[item] = {"is_genre": True}
            
            existing_subdirs = {subdir: metadata for subdir, metadata in self.subdirs.items() if os.path.isdir(os.path.join(dir, subdir))}

            self.subdirs = existing_subdirs
            self.subdirs[current_subdir] = {"is_genre": song_mode}
            print(f"Discovered {len(self.subdirs)} total subdirectories: {list(self.subdirs.keys())}")
        except OSError as e:
            print(f"Error scanning directory {dir}: {e}")
            self.subdirs = {current_subdir: {"is_genre": song_mode}}