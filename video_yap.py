import os
import subprocess

def video_olustur():
    with open("sahneler/input_list.txt", "w", encoding="utf-8") as f:
        for file in sorted(os.listdir("sahneler")):
            if file.endswith(".png"):
                f.write(f"file '{os.path.abspath('sahneler/' + file)}'\n")
                f.write("duration 3\n")
        f.write(f"file '{os.path.abspath('sahneler/' + file)}'\n")

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", "sahneler/input_list.txt",
        "-vsync", "vfr", "-pix_fmt", "yuv420p", "outputs/final_video.mp4"
    ])
