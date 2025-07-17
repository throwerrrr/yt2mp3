from src.yt2mp3.mp3_converter import MP3Converter

if __name__ == "__main__":
    # converter = MP3Converter()
    converter_with_params = MP3Converter(link="https://www.youtube.com/watch?v=52BOby5Ycxk", artist="kaden", song="city line", genre="acoustic")