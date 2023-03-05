import subprocess

cmd = './MIDIVisualizer --midi .\\raw\\pr.mid ' \
      '--size 1920 1080 ' \
      '--export bs.mp4  --format MPEG4 --hide-window'
returncode = subprocess.call(cmd)
