from mdutils.tools import Link
from mdutils.tools.MDList import MDList
import os

class MDFormatter:
    def __init__(self, MDFile, subdirs):
        self.md_file = MDFile
        self.subdirs = subdirs
        self.md_file.file_data_text = "" # Start fresh
        self.write_h1_title(self.md_file.md_title)
        self.format_subdirs(self.subdirs)
    
    def write_h1_title(self, title):
        self.md_file.new_header(1, title.replace("_", " "))
        self.md_file.write("\n")

    def format_subdirs(self, subdirs):
        for subdir in list(subdirs.keys()):
            self.md_file.new_header(2, subdir)
            self.place_list(subdir, subdirs[subdir]["is_genre"])
            self.md_file.write("\n")

    def get_subdir_data(self, subdir, is_genre=False):
        subdir_path = os.path.join(self.md_file.dir, subdir)
        if os.path.exists(subdir_path):
            try:
                subdir_file_list = os.listdir(subdir_path)
                subdir_data = {}
                subdir_data["link_list"] = []
                for file in subdir_file_list:
                    if file.endswith(".mp3"):
                        name = self.get_name_from_mp3_file(file, is_genre=is_genre)
                        link = Link.Inline.new_link(os.path.join(self.md_file.dir, subdir, file), name)
                        subdir_data[file] = {"link": link, "name": name}
                        subdir_data["link_list"].append(link)
                return subdir_data
            except OSError as e:
                print(f"An error occured while retrieving list of files in {subdir}")
                return {"link_list": []}
        else:
            print(f"Invalid subdirectory path: {subdir_path}")
            return {"link_list": []}

    def place_list(self, subdir, is_genre=False):
        subdir_data = self.get_subdir_data(subdir, is_genre)
        if subdir_data and subdir_data["link_list"]:
            list_obj = MDList(subdir_data["link_list"], marked_with="-")
            list_md = list_obj.get_md()
            for link in subdir_data["link_list"]:
                self.md_file.write(f"- {link}\n")

    def get_name_from_mp3_file(self, file, is_genre=False):
        no_ext_filename = file.replace(".mp3", "").replace("-", " ")
        if is_genre:
            cleaned_filename = no_ext_filename.replace("_", ": ").title()
        else:
            cleaned_filename = no_ext_filename.replace("_", " ").title()
        return cleaned_filename
    
    def return_md_file(self):
        return self.md_file