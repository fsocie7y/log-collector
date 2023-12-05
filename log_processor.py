import os
import re

from dotenv import load_dotenv
from googlesearch import search
from openai import OpenAI

load_dotenv()


def display_all_logs_in_the_directory(directory: str) -> list | str:
    if directory.endswith(".log"):
        return "Enter the path to directory not to log-file!"

    directory = re.findall("\w+", directory)
    if len(directory[0]) == 1:
        directory[0] += ":\\"

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
    return "This folder path does not exists, please try something else!"


def read_log_file(filename: str) -> str | list:
    if "\\" in filename:
        file_path = filename.split("\\")
    else:
        file_path = filename.split(" ")

    if len(file_path[0]) == 1 or file_path[0].endswith(":"):
        file_path[0] = file_path[0][0] + ":\\"

    file_path = os.path.join(*file_path)
    print(file_path)

    with open(file_path, "r") as file:
        lst_str = file.readlines()
        print(lst_str)

        errors = list()
        err_found = False

        err_messages = ("error", "fail", "dropped")
        for string in lst_str:
            if any(error in string.lower() for error in err_messages):
                print("Error found")
                err_found = True
                errors.append(string)
                print("Error: ", string)

        if not err_found:
            return "Everything is ok! This file has no information about errors."
        return errors


def helper(issue_query: str) -> search:
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    print("Processing Your Requests...")
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a computer engineering assistant,"
                           " skilled in explaining complex programming problems and resolving traceback errors."
                           "Please, help to resolve following issues."
            },
            {
                "role": "user",
                "content": issue_query
            }
        ]
    )

    search_results = completion.choices[0].message.content
    print(search_results)
    return search_results
