from src.yt2mp3.mp3_converter import *
from src.yt2mp3.arg_parser import *
from src.yt2mp3.error_handler import *

if __name__ == "__main__":

    args = parse_arguments(argv=None)
    
    if args.link:
        # Use the parsed arguments with the flexible generate function
        result = generate(args=args)
        print(f"Conversion initiated with arguments: {result}")
    else:
        # Fallback using individual parameters
        result = generate(link="", song="", artist="", genre="")
        print("No link provided, using default parameters")

    raise_errors()

    # converter_result = yt_to_mp3(output="dir/subdir", link="https://www.youtube.com/watch?v=JU2DArD9NRg", filename="")
    # if converter_result = 0:
        # md_tracker = MDDataTracker(dir, current_subdir, song_mode, cache_data)