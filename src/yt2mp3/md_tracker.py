import os

class MDDataTracker:
    def __init__(self, dir, current_subdir, song_mode, cache_data):
        self.dir = dir
        self.title = self.get_title(self.dir)
        self.current_subdir = current_subdir
        self.cache_data = cache_data

    def get_title(self, dir):
        return f"{os.path.basename(dir)}.md"

    def get_md_filepath(self, dir, title):
        return os.path.join(dir, title)

    def get_subdirs(self, dir, dir_contents, current_subdir, song_mode):
        dir_contents = self.get_dir_list(dir)
        self.subdirs = {}
        self.subdirs = self._discover_all_subdirs(dir, dir_contents, current_subdir, self.cache_data, song_mode)

    def check_if_md_file_exists(self, md_filepath):
        if os.path.exists(md_filepath):
            print("MD File exists.")
            return True
        else:
            print("MD File does not exist.")
            return False
    
    def get_last_save_id(self, cache_data):
        meta_data = cache_data
        if meta_data and isinstance(meta_data, dict) and "id" in meta_data:
            print(f"Cache loaded.")
            print(f"Last save id: {meta_data["id"]}")
    
    def _get_cached_subdirectories(self, cache_data):
        if cache_data and isinstance(cache_data, dict) and "id" in cache_data:
            if "subdirs" in cache_data and isinstance(cache_data["subdirs"], dict):
                cached_subdirs = cache_data["subdirs"]
                print(f"Loaded {len(cached_subdirs)} subdirectories from cache")
            else:
                return {}
        else:
            print("No valid cache data found")
            return {}

    def get_dir_list(self, dir):
        try:
            dir_contents = os.listdir(dir)
            filtered_contents = []
            for subdir in dir_contents:
                if subdir is None:
                    continue
                elif isinstance(subdir, str) and subdir.startswith("."): # Filter directories like `.venv`, `.git`, etc.
                    continue
                elif dir == "yt2mp3" and subdir == "src" or dir == os.getcwd() and subdir == "src": # filter src
                    continue
                elif isinstance(subdir, str) and subdir.startswith("__") and subdir.endswith("__"): # Filter __pycache__ etc.
                    continue
                else:
                    subdir_path = os.path.join(dir, subdir)
                    if os.path.isdir(subdir_path):
                        filtered_contents.append(subdir)
            return filtered_contents
        
        except OSError as e:
            print(f"Error scanning directory {dir}: {e}")
            return []
        
    def _discover_all_subdirs(self, dir, dir_contents, current_subdir, cache_data, song_mode):
        try:
            subdirs = cache_data["subdirs"]
        except Exception as e:
            print(e)
            subdirs = {}
        try:
            for subd in dir_contents:
                item_path = os.path.join(dir, subd)
                if os.path.isdir(item_path):
                    if subd not in subdirs:
                        subdirs[subd] = {"is_genre": True}
            
            existing_subdirs = {subdir: metadata for subdir, metadata in self.subdirs.items() if os.path.isdir(os.path.join(dir, subdir))}

            self.subdirs = existing_subdirs
            if current_subdir is not None:
                self.subdirs[current_subdir] = {"is_genre": song_mode}

            print(f"Discovered {len(self.subdirs)} total subdirectories: {list(self.subdirs.keys())}")
        except OSError as e:
            print(f"Error scanning directory {dir}: {e}")

            if current_subdir is not None:
                return {current_subdir: {"is_genre": song_mode}}
            
            else:
                print(f"Could not find any existing subdirectories in {dir}")
                return {}