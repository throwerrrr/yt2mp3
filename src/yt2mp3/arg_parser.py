# src/yt2mp3/arg_parser.py
from argparse import ArgumentParser

def parse_arguments(argv=None):
    parser = ArgumentParser()
    parser.add_argument('-l', '--link', type=str, help='provide a valid youtube link.')
    parser.add_argument('-s', '--song', type=str, help='provide a song title. used in file name.')
    parser.add_argument('-a', '--artist', type=str, help='provide an artist name. used in file name.')
    parser.add_argument('-g', '--genre', type=str, help='provide a genre. used as subdir.')
    parser.add_argument('-d', '--dir', type=str, help='provide a directory. default is cwd.')
    parser.add_argument('-sd', '--subdir', type=str, help='provide a subdirectory (overriden by genre)')
    parser.add_argument('-f', '--filename', type=str, help='provide a filename (overriden by song and artist)')
    
    return parser.parse_args(argv)

def generate(argv):
    args = parse_arguments(argv)
    return args

