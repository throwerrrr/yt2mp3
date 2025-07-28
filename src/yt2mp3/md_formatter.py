from md_format_utils import *

def write_mdfile_header1(MDFile): # mdutils has a bug without this
    MDFile.new_header(1, MDFile.title.replace("_", " "))
    MDFile.write("\n")

def format_subdir(MDFile, subdir_data):
    MDFile.new_header(2, subdir_data["subdir"])
    if subdir_data and subdir_data["link_list"]:
        for link in subdir_data["link_list"]:
            MDFile.write(f"- {link}\n")