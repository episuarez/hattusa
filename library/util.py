import os

def get_name_and_extension(filename):
    return os.path.splitext(filename);

def get_name(filename):
    return os.path.splitext(filename)[0];

def get_extension(filename):
    return os.path.splitext(filename)[1];