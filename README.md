# YT to MP3 Converter

Essentially a wrapper for [yt-dlp](https://github.com/yt-dlp/yt-dlp) with fewer options, but an easier experience. Downloads videos and converts them to MP3 files, with automatic organization and markdown file generation for documentation.

### This tool is intended for personal and educational use only. Please respect copyright laws and Terms of Service.

## Features

- Download videos via link and convert to MP3 (for more information on what websites videos can be downloaded from, visit the [yt-dlp](https://github.com/yt-dlp/yt-dlp) repo)
- File organization genre or subdirectory
- Auto-generate markdown documentation with clickable links [More Info](#markdown-documentation)
- Caching system to track downloads [More Info](#caching-system)
- Two operation modes: Song Mode and Custom Mode [Song-Mode](#song-mode) [Custom Mode](#custom-mode)
- CLI and programmatic interfaces [CLI](#command-line-interface-cli)[Programmatic Interfaces](#programmatic-interface)

## Quick Start

### Prerequisites

- Python 3.7+
- `yt-dlp` (for YouTube downloading)
- Internet connection

### Installation

1. **Clone the repository**

2. **Set up virtual environment (recommended)**
```bash
   python -m venv .venv
   source .venv/bin/activate
```
_ON WINDOWS_
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

## Usage
_**Note**: Current working directory will be used as a defualt directory if directory is not provided._

The application supports two modes of operation and two interfaces:

### Command Line Interface (CLI)

#### Song Mode
**Use if**:
- You're downloading a song
- You're okay with the song being organized in a predetermined format
    - `Genre/Artist-Name_Song-Title.mp3`

| Required  | Arg | Parameter |
|-----------|-----|-----------|
|   link    | -l  |    link   |
|   song    | -s  |    song   |
|   artist  | -a  |   artist  |
|   genre   | -g  |   genre   |

**Note**: The genre is used as the subdirectory.

**CLI Example**
```bash
python main.py -l "https://youtube.com/watch?v=..." -s "Song Title" -a "Artist Name" -g "Genre"
```

**Programmatic Example:**
```python
if __name__ == __main__:
    main(link="https://youtube.com/watch?v=", song="Song-Title", artist="Artist-Name", genre="Genre")
```

**Result:**
- File: `Genre/Artist-Name_Song-Title.mp3`
- Markdown entry: `[Artist-Name: Song-Title](Genre/Artist-Name_Song-Title.mp3)`

#### Custom Mode
**Use if**:
- Your URL is not a song
- You don't know the details of the song
- You want to use a custom filename

| Required      | Arg | Parameter |
|---------------|-----|-----------|
|   link        | -l  |    link   |
|   filename    | -f  |    song   |
|   subdir      | -s  |   artist  |

```bash
python main.py -l "https://youtube.com/watch?v=..." -f "Custom Filename" -sd "Custom Subdirectory"
```

**Example:**
```python 
if __name__ == "__main__":
    main(link="https://youtube.com/watch?v=JU2DArD9NRg" filename="My Favorite Song", subdir="Playlists")
```

#### Command Line Arguments

| Short | Long        | Description                                   | Required | Notes                          |
|-------|-------------|-----------------------------------------------|----------|----------------------------------|
| `-l`  | `--link`    | URL to download                               | Yes      |                                 |
| `-s`  | `--song`    | Song title (Song Mode)                        | Song*    | Used in filename                |
| `-a`  | `--artist`  | Artist name (Song Mode)                       | Song*    | Used in filename                |
| `-g`  | `--genre`   | Genre (Song Mode)                             | Song*    | Used as subdirectory            |
| `-f`  | `--filename`| Custom filename (Custom Mode)                 | Custom*  | Overridden by song/artist       |
| `-sd` | `--subdir`  | Custom subdirectory (Custom Mode)             | Custom*  | Overridden by genre             |
| `-d`  | `--dir`     | Target directory                              | No       | Defaults to current directory   |

*Required for respective mode

### Programmatic Interface

You can also use the application programmatically by calling the `main()` function with parameters:

```python
from main import main

# Song Mode
converter = main(
    link="https://www.youtube.com/watch?v=uIQLj8xmnS0",
    song="Cinematic Piano",
    artist="Summit Alex-Productions",
    genre="Instrumental"
)

# Custom Mode
converter = main(
    link="https://www.youtube.com/watch?v=uIQLj8xmnS0",
    filename="Cinematic_Piano-Custom-Filename",
    subdir="My-Playlist"
)

# Skip conversion (only generate markdown)
converter = main(
    link="https://www.youtube.com/watch?v=uIQLj8xmnS0",
    song="Cinematic-Piano",
    artist="Summit-Alex-Productions",
    genre="Instrumental",
    skip_conversion=True
)
```

## File Generation

### Output Structure
```
your-directory/
├── Genre1/
│   ├── Artist1_Song1.mp3
│   └── Artist2_Song2.mp3
├── Genre2/
│   └── Artist3_Song3.mp3
├── your-directory.md          # Auto-generated markdown
└── cache.json                 # Download history
```

### Filename Conventions

- **Song Mode**: `Artist-Name_Song-Title.mp3`
- **Custom Mode**: `Custom-Filename.mp3`
- **Sanitization**: Special characters removed, spaces converted to hyphens

## Markdown Documentation
The application automatically generates a markdown file (`{directory-name}.md`) with:

- Organized sections by genre/subdirectory
- Clickable links to MP3 files
- Clean, readable formatting

**Note**: Existing files & subdirectories are assumed to align with _Song Mode_ practices. You can change this in [md_tracker.py](src/yt2mp3/md_tracker.py) in the method `_discover_all_subdirs_()` by changing 

- `subdirs[subd] = {"is_genre": True}` 
TO 
- `subdirs[subd] = {"is_genre": False}`.

**_Song Mode_**: 
-  `-` become ` `, and `_` become `: `
- `Artist-Name_Song-Name` == `Artist Name: Song Name`.

**_Custom Mode_**: Filenames are left alone.

## Caching System

The application maintains a `cache.json` file that tracks:
- Download history
- Metadata for each conversion
- Directory structure information

This prevents duplicate downloads and enables incremental documentation updates.

## Dependencies

| Package    | Version | Purpose                    |
|------------|---------|----------------------------|
| yt-dlp     | 2025.6.30 | YouTube video downloading |
| mdutils    | 1.8.0   | Markdown file generation  |
| pytest     | 8.4.1   | Testing framework         |

## Troubleshooting

### Common Issues

1. **"No module named 'src'"**
   - Ensure you're running from the project root directory
   - Check that `__init__.py` files are present

2. **Download fails**
    - Check your internet connection
    - Verify the URL is valid, accessible, and non-age or region-restricted.

3. **Permission denied errors**
   - Ensure write permissions for the target directory

## Contributing

1. Follow the existing code structure
2. Add tests for new functionality
3. Update documentation for any changes
4. Respect the educational/personal use intention

## License

See `COPYING` file for license information.

---

**Note**: Always respect copyright laws and the intellectual property rights of content creators when using this tool.
