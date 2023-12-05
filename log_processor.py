import os
import re
from googlesearch import search


direct = "D:\\"


def display_all_logs_in_the_directory(directory: str) -> list | str:
    directory = re.findall("\w+", directory)
    if len(directory[0]) == 1: directory[0] += ":\\"
    dir_path = "\\".join(directory)
    print("Dir path", dir_path)

    if os.path.exists(dir_path):
        print("Path exists")
        result_paths = list()
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.log'):
                    res = os.path.join(root, str(file))
                    result_paths.append(res)

        return result_paths
    else:
        return "This folder path does not exists, please try something else!"


# for log_file in display_all_logs_in_the_directory(direct):
#     print("Found file", log_file)


def read_log_file(filename):
    with open(filename, "r") as file:
        lst_str = file.readlines()
        print(lst_str)
        err_found = False
        err_messages = ("error", "faile", "dropped")
        for string in lst_str:
            if any(error in string.lower() for error in err_messages):
                print("Error found")
                err_found = True
                print("Error: ", string)
        if not err_found:
            print("Everything is ok! This file has no information about errors.")


# read_log_file(direct)


def google_helper(search_query: str) -> search:

    print("Processing Your Requests...")
    search_results = search(search_query, num_results=5)
    for result in search_results:
        print(result)

    return search_results


# searchfor = "Sat Dec 02 00:01:46 2023 UTC - Failed loading shell32.dll, not hooking ShellExecute calls"
# google_helper(searchfor)
