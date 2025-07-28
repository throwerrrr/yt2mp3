import os
from mdutils.tools import Link, Link

def get_subdirectory_path(dir, subdir):
    subdir_path = os.path.join(dir, subdir)
    return subdir_path

def get_subdir_file_list(subdir_path):
    if os.path.exists(subdir_path):
        try:
            subdir_file_list = os.listdir(subdir_path)
            return subdir_file_list
        except OSError as e:
            print(f"An error occured while retrieving list of files in {os.path.basename()}")
            return []
    print(f"Invalid subdirectory path: {subdir_path}")
    return []

def clean_subdir_list_for_mp3_files(subdir_file_list):
    cleaned_list = []
    for file in subdir_file_list:
        if file.endswith(".mp3"):
            cleaned_list.append(file)
    return cleaned_list

def get_names_from_mp3_files(file_list, is_genre):
    file_name_map = {}
    for file in file_list:
        no_ext_title_name = file.replace(".mp3", "").replace("-", " ")
        if is_genre:
            cleaned_title_name = no_ext_title_name.replace("_", ": ").title()
        else:
            cleaned_title_name = no_ext_title_name.replace("_", " ").title()
        file_name_map[file] = {"title": cleaned_title_name}

def get_subdir_data(subdir_path, file_name_map):
    file_name_map["path"] = subdir_path
    file_name_map["link_list"] = []
    file_name_map["subdir"] = os.path.basename(subdir_path)

    for file in list(file_name_map.keys()):
        link_path = os.path.join(subdir_path, file)
        link = Link.Inline.new_link(link_path, file_name_map["name"])
        file_name_map[file]["link"] = link
        file_name_map["link_list"].append(link)

    subdir_data= file_name_map
    return subdir_data