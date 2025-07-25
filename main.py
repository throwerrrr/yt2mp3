from src.yt2mp3.mp3_converter import MP3Converter
import os

if __name__ == "__main__":
    # converter = MP3Converter()
    converter_with_params = MP3Converter(link="https://www.youtube.com/watch?v=JU2DArD9NRg", artist="test artist", song="test song", genre="test", dir="/Example_Dir")