from src.yt2mp3 import arg_parser, cache, error_handler, file_handler, \
    mp3_converter, md_tracker, md_format_utils, md_file

CWD = file_handler.CWD

class CacheManager:
    
    def __init__(self, cache: cache.Cache):
        self.cache_obj = cache
    
    def setup_cache(self):
        
        if self.cache_obj.validate_export_data(self.cache_obj.export_data):
            file_exists = self.cache_obj.check_cache_file_exists()
            existing_data = self.cache_obj.get_existing_cache_data(file_exists)
            self.cache_obj.check_cache_data(existing_data)
            return existing_data
        return None
    
    def cache_load(self, existing_data):
        
        return self.cache_obj.load_most_recent_cache_data(existing_data)

    def handle_save(self, recent_metadata):
        
        return self.cache_obj.save_to_cache(recent_metadata)


class InputProcessor:
    
    def __init__(self, args=None):
        self.args = args or arg_parser.parse_arguments(argv=None)
    
    def generate_input_data(self):
    
        if self.args.link:
            return mp3_converter.generate(args=self.args)
        else:
            return mp3_converter.generate( # test song
                link="https://www.youtube.com/watch?v=JU2DArD9NRg", 
                song="test_song", 
                artist="test_artist", 
                genre="test_genre"
            )

    def validate_input(self, input_data):

        no_errors = error_handler.raise_errors(
            link=input_data["link"], song=input_data["song"], artist=input_data["artist"], genre=input_data["genre"], 
            dir=input_data["dir"], subdir=input_data["subdir"], filename=input_data["filename"]
        )
        
        if no_errors:
            print("Input validated.")
        return no_errors # bool

    def define_mode(self, input_data):
        try:
            song_mode = error_handler.define_mode(song=input_data["song"])
            print(f"Song Mode: {song_mode}")
            return song_mode
        except Exception as e:
            print(f"Exception occurred. Details: {e}")

    def validate_based_on_mode(self, song_mode, input_data):
        try:
            if song_mode:
                error_handler.check_song_mode_errors(input_data["song"], input_data["artist"], input_data["genre"])
            else:
                error_handler.check_other_mode_errors(input_data["filename"], input_data["subdir"])
        except Exception as e:
            print(f"Exception occurred. Details: {e}")
        
        return True


class FileProcessor:
    def __init__(self, handler: file_handler.FileHandler, input_data):
        self.handler = handler
        self.input_data = input_data
    
    def process_files(self, input_data, song_mode):

        self.handler._process_files(
            link=input_data["link"],
            dir=input_data["dir"],
            artist=input_data["artist"],
            song=input_data["song"],
            genre=input_data["genre"],
            subdir=input_data["subdir"],
            filename=input_data["filename"],
            song_mode=song_mode
        )

class Converter:

    def __init__(self, handler: file_handler.FileHandler):
        self.handler = handler
    
    def convert(self):
        conversion = mp3_converter.yt_to_mp3(
            self.handler.output, self.handler.link, self.handler.filename
        )
        conversion_result = mp3_converter.handle_conversion(
            conversion, self.handler.output, self.handler.filename)
        
        return conversion_result

class DirectoryProcessor:
    
    def unpack_dir_contents(self, dir_path, dir_contents, is_genre):
        
        dir_subdir_map = {}
        for subdir in dir_contents:
            if subdir is None:
                continue
            
            subdir_path = md_format_utils.get_subdirectory_path(dir_path, subdir)
            file_list = md_format_utils.get_subdir_file_list(subdir_path)
            cleaned_list = md_format_utils.clean_subdir_list_for_mp3_files(file_list)
            file_name_map = md_format_utils.get_names_from_mp3_files(cleaned_list, is_genre)
            subdir_data = md_format_utils.get_subdir_data(subdir_path, file_name_map, subdir)
            dir_subdir_map[subdir] = subdir_data
        
        return dir_subdir_map


class MDFileManager:
    
    def __init__(self, md_data_tracker: md_tracker.MDDataTracker, cache_metadata, directory_processor):
        self.md_data_tracker = md_data_tracker
        self.cache_metadata = cache_metadata
        self.directory_processor = directory_processor
    
    def setup_md_tracker(self, dir_path, subdir, song_mode):

        dir_contents = self.md_data_tracker.get_dir_list(self.md_data_tracker.dir)
        self.md_data_tracker.get_subdirs(
            self.md_data_tracker.dir, dir_contents, 
            self.md_data_tracker.current_subdir, song_mode
        )
        
        return self.md_data_tracker, dir_contents
    
    def print_debug_info(self, CWD, md_file: md_file.MDFile):

        return f"CWD: {CWD} \
        Dir: {md_file.dir} \
        File_title: {md_file.file_title} \
        File_name: {md_file.file_name} \
        Filepath: {md_file.md_filepath}"
    
    def check_if_exists(self):

        md_file_exists = self.md_data_tracker.check_if_md_file_exists(
            self.md_data_tracker.get_md_filepath(self.md_data_tracker.dir, self.md_data_tracker.title)
        )
        return md_file_exists

    def process_directory_contents(self, directory_processor: DirectoryProcessor, dir_contents, song_mode):

        dir_processor = directory_processor
        dir_subdir_map = dir_processor.unpack_dir_contents(
            self.md_data_tracker.dir, dir_contents, song_mode
        )
        return dir_subdir_map

    def return_file_creation_result(self, md_file_exists, md_file: md_file.MDFile):

        if md_file_exists:
            return f"MD file updated: {md_file.md_filepath}"
        else:
            return f"MD file created: {md_file.md_filepath}"

    def create_md_file(self, md_file_obj: md_file.MDFile, dir_contents, song_mode):

        md_file_exists = self.md_data_tracker.check_if_md_file_exists(
            self.md_data_tracker.get_md_filepath(self.md_data_tracker.dir, self.md_data_tracker.title)
        )
        
        dir_subdir_map = self.process_directory_contents(self.directory_processor, dir_contents, song_mode)

        for subdir in sorted(list(dir_subdir_map.keys())):
            subdir_data = dir_subdir_map[subdir]
            md_file.format_subdir(md_file_obj, subdir_data)
        
        md_file_obj.create_md_file()

        print(self.print_debug_info(CWD, md_file_obj))
        print(self.return_file_creation_result(md_file_exists, md_file_obj))

        return md_file_obj


class YT2MP3Application:
    
    def __init__(self, InputProcessor, CacheManager, args=None):
        self.args = args
        self.input_processor = InputProcessor
        self.cache_manager = CacheManager
    
    def setup(self):

        existing_data = self.cache_manager.setup_cache()
        current_cache_metadata = self.cache_manager.cache_load(existing_data)
        input_data = self.input_processor.generate_input_data()
        self.input_processor.validate_input(input_data)
        song_mode = self.input_processor.define_mode(input_data)

        return {
            "cache_metadata": current_cache_metadata,
            "input_data": input_data,
            "song_mode": song_mode
        }
        
    def run(self, MDFileManager: MDFileManager, FileProcessor: FileProcessor, FileHandler: file_handler.FileHandler, input_data, song_mode):
        self.file_processor = FileProcessor
        self.handler = FileHandler
        self.md_file_manager = MDFileManager

        self.file_processor.process_files(input_data, song_mode)

        md_data_tracker, dir_contents = self.md_file_manager.setup_md_tracker(
            input_data["dir"], input_data["subdir"], song_mode)
        
        md_file_obj = md_file.MDFile(title=md_data_tracker.title, dir=md_data_tracker.dir)
        md_file_result = self.md_file_manager.create_md_file(md_file_obj, dir_contents, song_mode)
        
        return {
                "input_data": input_data,
                "md_file_obj": md_file_result,
                "md_data_tracker": md_data_tracker
                }
            
def main(link=None, song=None, artist=None, genre=None, filename=None, subdir=None, dir=None, skip_conversion=False):
    """Entry point for the application with opt. parameters.
    
    Args:
        link: YouTube URL to download
        song: Song name 
        artist: Artist name
        genre: Genre name
        filename: Custom filename
        subdir: Subdirectory name
        dir: Target directory 
        skip_conversion: Only creates MD file if True. Defaults to False.

    """
    cache_obj = cache.Cache()
    cache_manager = CacheManager(cache_obj)
    
    if any([link, song, artist, genre, filename, subdir, dir]):
        class MockArgs:
            def __init__(self):
                self.link = link
                self.song = song  
                self.artist = artist
                self.genre = genre
                self.filename = filename
                self.subdir = subdir
                self.dir = dir
        
        input_processor = InputProcessor(MockArgs())
    else:
        input_processor = InputProcessor()
    
    app = YT2MP3Application(input_processor, cache_manager)

    setup = app.setup()

    cache_metadata = setup["cache_metadata"]
    input_data, song_mode = setup["input_data"], setup["song_mode"]
    
    
    md_data_tracker = md_tracker.MDDataTracker(
        dir=input_data["dir"], 
        current_subdir=input_data["subdir"], 
        song_mode=song_mode, 
        cache_data=cache_metadata
    )
    directory_processor = DirectoryProcessor()
    md_file_manager = MDFileManager(md_data_tracker, cache_metadata, directory_processor)

    handler = file_handler.FileHandler(song_mode, input_data)
    file_processor = FileProcessor(handler, input_data)

    if not skip_conversion and input_data["link"]:
        print(f"Starting conversion of: {input_data['link']}")
        
        
        file_processor.process_files(input_data, song_mode)

        # CONVERSION
        converter = Converter(handler)
        conversion_result = converter.convert()
        print(f"Conversion result: {conversion_result}")
    else:
        print("Skipping MP3 conversion (skip_conversion=True or no link provided)")
    
    result = app.run(md_file_manager, file_processor, handler, input_data, song_mode)
    
    return result


if __name__ == "__main__":
    main(link="https://www.youtube.com/watch?v=uIQLj8xmnS0", song="cinematic-piano", artist="summit-alex_productions", genre="test-mode")
    # main()

    # -------- --------
    # to test CLI: 
    # 1. Comment out `main(link=...)`
    # 2. Uncomment `main()`
    # 3. run command ↓

    # python main.py -l "https://www.youtube.com/watch?v=uIQLj8xmnS0" -s "cinematic-piano" -a "summit-alex_productions" -g "test-mode"

    # -------- -------- -------- --------

    # Song: Cinematic Piano | Summit Alex-Productions