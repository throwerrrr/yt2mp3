# YT to Audio Converter
### This tool is for PERSONAL, EDUCATIONAL use.

## Setup
Set up your venv and install the requirements:
```bash
python -m venv .venv && \
    source .venv/bin/activate && \ 
    pip install -r requirements.txt
```

## Use
`main.py` in the root directory has `MP3Converter()`, which does all the heavy lifting, and can be used in two ways:
1. CLI
    - Keep `main.py` the way it is
    - Run the program like this:
    - **Song Mode**:
        - `python main.py -s "song title" -a "artist" -g "genre" -d "dir" -l "link.com"`
    - **Other**:
        - `python main.py -f "filename" -sd "subdirectory" -d "dir" -l "link.com"`
    - **_Note_**: `-d`/`dir` is optional. Defaults to cwd.

2. Parameters
    - Change `main.py` so `MP3Converter()` uses parameters. For example:
        ```python
            if __main__ == "__name__":
                converter = MP3Converter(link="link.com", artist="artist", song="song title", genre="genre")
        ```

**Note**: Genre is used as the subdirectory.
