from mdutils.mdutils import MdUtils
import os
from src.yt2mp3.cache import Cache
from datetime import datetime

class MDFile(MdUtils):
    def __init__(self, file_name, dir, md_title="", author=""):
        super().__init__(file_name=os.path.join(dir, file_name), author=author)
        self.md_title = md_title
        self.dir = dir
        self.filepath = os.path.join(dir, file_name)
        
    def export_for_cache(self, subdirs=None):
        return {
            "id": datetime.now().timestamp(),
            "date": datetime.now().isoformat(),
            "title": self.md_title,
            "dir": self.dir,
            "author": self.author,
            "file_data_text": self.file_data_text,
            "subdirs": subdirs if not None else {}
        }