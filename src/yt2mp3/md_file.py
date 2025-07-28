from mdutils.mdutils import MdUtils
import os
from src.yt2mp3.cache import Cache

class MDFile(MdUtils):
    def __init__(self, file_name, dir, md_title="", author=""):
        super().__init__(file_name=os.path.join(dir, file_name), author=author)
        self.md_title = md_title
        self.dir = dir
        self.filepath = os.path.join(dir, file_name)

    def _save_file(self):
        cache_save = Cache(self)._save_to_cache()
        if cache_save is True:
            self.create_md_file()
            return True
        else:
            print("Process interrupted while saving to Cache.")
            return False