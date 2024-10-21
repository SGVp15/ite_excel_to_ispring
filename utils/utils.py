import os


def get_all_files_from_pattern(folder_input: str, pattern: str):
    file_list = []
    for root, dirs, files in os.walk(folder_input):
        for name in files:
            if name.endswith(pattern):
                file_list.append(os.path.join(root, name))
    return file_list
