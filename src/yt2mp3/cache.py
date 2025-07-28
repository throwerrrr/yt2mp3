import os, json, datetime

class Cache:
    def __init__(self, md_file_export_data):
        self.md_file = md_file_export_data
        self.cache_file = os.path.join(os.getcwd(), "cache.json")

    def _load_from_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r") as cache:
                    existing_data = json.load(cache)
                    if isinstance(existing_data, list):
                        most_recent_metadata = existing_data[0]
                        return most_recent_metadata
            except (json.JSONDecodeError, FileNotFoundError) as e:
                return f"An error occured while reading {self.cache_file}. Details: {e}"
        else:
            return f"Cache file moved or corrupted"

    def _clear_cache(self, create_backup=True):
        try:
            if not os.path.exists(self.cache_file):
                print("Cache file does not exist - nothing to clear.")
                return True
                
            if create_backup:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = os.path.join(os.getcwd(), f"cache_backup_{timestamp}.json")
                
                try:
                    with open(self.cache_file, 'r') as original:
                        with open(backup_file, 'w') as backup:
                            backup.write(original.read())
                    print(f"Cache backup created: {backup_file}")
                except Exception as e:
                    print(f"Warning: Could not create backup, but proceeding with cache clear. Error: {e}")
            os.remove(self.cache_file)
            print(f"Cache file {self.cache_file} successfully cleared.")
            return True
            
        except FileNotFoundError:
            print("Cache file was already deleted.")
            return True
        except PermissionError as e:
            error_msg = f"Permission denied when trying to clear cache: {e}"
            print(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"Unexpected error while clearing cache: {e}"
            print(error_msg)
            return error_msg

    def _save_to_cache(self, md_file_export_data):
        if self.md_file is not None:
            meta_data = md_file_export_data
            if hasattr(self.md_file, 'subdirs'):
                meta_data["subdirs"] = self.md_file.subdirs
            else:
                meta_data["subdirs"] = {}
        else:
            return "No MDFile data to save."
        try:
            if os.path.exists(self.cache_file):
                try:
                    with open(self.cache_file, "r") as cache:
                        existing_data = json.load(cache)
                        if not isinstance(existing_data, list):
                            existing_data = [existing_data]
                except (json.JSONDecodeError, FileNotFoundError) as e:
                    print(f"Original cache file moved or corrupted. Creating a new cache file... Details: {e}")
                    existing_data = []
            else:
                existing_data = []
            existing_data.insert(0, meta_data)

            with open(self.cache_file, "w") as cache:
                json.dump(existing_data, cache, indent=4)
                return True

        except FileNotFoundError as e:
            return f"Could not save current MD state. Details: {e}"
        except json.JSONDecodeError as e:
            return f"Could not decode {self.cache_file}. Details: {e}"