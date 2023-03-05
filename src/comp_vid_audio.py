import sys
import moviepy.editor as mp

# import moviepy.editor as mp
#
# clip = mp.VideoFileClip("C:\\Users\Re\\Downloads\\bs.mp4").subclip()
# clip.write_videofile("test.mp4", audio=".\\sine_demo.wav")

video = mp.VideoFileClip("C:\\Users\Re\\Downloads\\bss.mp4")
video = video.set_audio(mp.AudioFileClip(".\\sine_demo.wav"))
video.write_videofile("test.mp4")
