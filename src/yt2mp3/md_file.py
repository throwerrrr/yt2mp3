from mdutils.mdutils import MdUtils
import os
from src.yt2mp3.cache import Cache
from datetime import datetime

class MDFile(MdUtils):
    def __init__(self, title, dir):
        self.title = title
        self.file_title = f"{os.path.basename(dir)}.md"
        self.dir = dir
        self.md_filepath = self.get_filepath(self.dir, self.file_title)
        super().__init__(file_name=self.md_filepath, title=os.path.basename(dir), title_header_style="atx")
        
    def export_for_cache(self, subdirs=None):
        return {
            "id": datetime.now().timestamp(),
            "date": datetime.now().isoformat(),
            "title": self.file_title,
            "dir": self.dir,
            "file_data_text": self.file_data_text,
            "subdirs": subdirs if not None else {}
        }
    
    def get_filepath(self, dir, file_title):
        return os.path.abspath(os.path.join(dir, file_title))
    
    def get_dir(self):
        return self.dir

def format_subdir(MDFile, subdir_data):
    MDFile.new_header(2, subdir_data["subdir"], add_table_of_contents="n")
    if subdir_data and subdir_data["link_list"]:
        for link in subdir_data["link_list"]:
            MDFile.write(f"- {link}\n")

