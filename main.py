from src.yt2mp3.mp3_converter import MP3Converter
import os

if __name__ == "__main__":
    # converter = MP3Converter()

    converter_with_params = MP3Converter(link="https://www.youtube.com/watch?v=v2E3ATcEGM4", artist="mac miller", song="small worlds", genre="hip-hop", dir="/Users/kadenthrower/Desktop/References")