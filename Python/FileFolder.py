import os
from os import path
from os import listdir
import shutil


def remove_files(directory, extension=None):
    if extension is None:
        for file_name in listdir(directory):
            os.remove(directory + file_name)
    else:
        for file_name in listdir(directory):
            if file_name.endswith(extension):
                os.remove(directory + file_name)


def make_folder(directory):
    if not path.exists(directory):
        os.mkdir(directory)


def delete_folder(directory):
    if path.exists(directory):
        shutil.rmtree(directory)


def rename_folder(directory, new_directory):
    if path.exists(directory):
        os.rename(directory, new_directory)


def does_path_exist(directory):
    return path.exists(directory)


def does_file_exist(file_path):
    return path.exists(file_path)
