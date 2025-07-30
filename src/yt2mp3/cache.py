import os, json
from src.yt2mp3.file_handler import CWD

class Cache:
    def __init__(self, md_file_export_data=None, dir=CWD, cache_file="cache.json"):
        self.export_data = md_file_export_data
        self.cache_file = cache_file
        self.dir = dir
        
    def get_cache_filepath(self):
            return os.path.join(self.dir, self.cache_file)

    def load_most_recent_cache_data(self, existing_data):
        if isinstance(existing_data, list):
            if len(existing_data) > 0:
                most_recent_metadata = existing_data[0]
                return most_recent_metadata
            else:
                print("No existing cache data found.")
                return None
        elif isinstance(existing_data, dict):
            existing_data = list(existing_data)
            if len(existing_data) > 0:
                most_recent_metadata = existing_data[0]
                return most_recent_metadata
            else:
                print("No existing cache data found.")
                return None
        else:
            print(f"The existing data is not loadable.")
            return None

    def save_to_cache(self, most_recent_cache_data):
        cache_filepath = self.get_cache_filepath()
        if self.export_data is None:
            return f"Export data is empty."
        meta_data = self.export_data
        try:
            most_recent_cache_data.insert(0, meta_data)

            with open(cache_filepath, "w") as cache:
                json.dump(most_recent_cache_data, cache, indent=4)
                return True
            
        except FileNotFoundError as e:
            return f"Could not save current MD state. Details: {e}"
        except json.JSONDecodeError as e:
            return f"Could not decode {cache_filepath}. Details: {e}"

    def get_existing_cache_data(self, file_exists):
        cache_filepath = self.get_cache_filepath()
        if file_exists:
            try:
                with open(cache_filepath, "r") as file:
                    existing_data = json.load(file)
                return existing_data
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Original cache file moved or corrupted. Creating a new cache file... Details: {e}")
                return []
        else:
            return []

    def validate_export_data(self, cache_data):
        if validate_export_data_util(cache_data):
            return True
        
    def check_cache_file_exists(self):
        cache_filepath = self.get_cache_filepath()
        return os.path.exists(cache_filepath)
        
    def check_cache_data(self, existing_data):
        if not isinstance(existing_data, list):
            if isinstance(existing_data, dict):
                existing_data = [existing_data]
                return existing_data
            else:
                return f"Invalid type for existing cache data: {type(existing_data)}"
        else:
            return existing_data

    def update_export_data(self, md_file_export_data):
        setattr(self, "export_data", md_file_export_data)
        return md_file_export_data

def validate_export_data_util(export_data):
    if export_data == None:
        print("No cache data to check.")
        return True
    if not isinstance(export_data, dict):
        raise TypeError()
    if any(key not in list(export_data.keys()) for key in ["id", "date", "title", "dir", "author", "file_data_text", "subdirs"]):
        raise ValueError(f"Cache data invalid.")
    elif not isinstance(export_data["subdirs"], dict):
        raise TypeError(f"Invalid cache data. Subdir key should be dict, but is {type(export_data["subdirs"])}")
    elif not isinstance(export_data["title"], str):
        raise TypeError(f"Invalid cache data. Title key should be str, but is {type(export_data["title"])}")
    elif not isinstance(export_data["dir"], str):
        raise TypeError(f"Invalid cache data. Dir key should be str, but is {type(export_data["dir"])}")
    elif not isinstance(export_data["author"], str):
        raise TypeError(f"Invalid cache data. Author key should be str, but is {type(export_data["author"])}")
    elif not isinstance(export_data["file_data_text"], str):
        raise TypeError(f"Invalid cache data. File_data_text key should be dict, but is {type(export_data["file_data_text"])}")
    else:
        print("Export data is clean!")
        return True