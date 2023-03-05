import subprocess
import dawdreamer as daw
from scipy.io import wavfile
import numpy as np
import sys
import moviepy.editor as mp
import cv2



def main():
    MIDI_PATH = 'C:\\Users\\Re\\Documents\\GitHub\\piano-roll-converter\\src\\raw\\pr.mid'
    cmd = 'ffmpeg -i ' + MIDI_PATH[:-4] + '_merged' + \
          '.mp4 -itsoffset 1.8 -i audio.m4a -map 0:1 -map 1:0 -c copy out.mp4'
    # print(subprocess.call(cmd))


if __name__ == "__main__":
    main()
