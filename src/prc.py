import subprocess
import dawdreamer as daw
from scipy.io import wavfile
import numpy as np
import sys
import moviepy.editor as mp
import cv2
import scipy


# MIDIVisualizer.exeを呼び出す
def call_midi_visualizer(MIDI_PATH):
    cmd = './MIDIVisualizer --midi ' + MIDI_PATH + \
          ' --size 1920 1080 ' \
          '--export ' + MIDI_PATH[:-3] + 'mp4 --format MPEG4 --hide-window'
    print(subprocess.call(cmd))

    # 動画の秒数を取り出して返す
    cap = cv2.VideoCapture(MIDI_PATH[:-3] + 'mp4')
    # 再生時間
    return cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)

def call_daw_dreamer(MIDI_PATH, sec):
    SAMPLE_RATE = 44100
    BLOCK_SIZE = 512
    # SYNTH_PLUGIN = "C:\\Users\\Re\\Downloads\\DSK_The_Grand_-_win64\\DSK The Grand - win64\\DSK The Grand.dll"
    SYNTH_PLUGIN = "C:\\Program Files\\VstPlugins\\Toontrack\\EZkeys.dll"

    engine = daw.RenderEngine(SAMPLE_RATE, BLOCK_SIZE)
    synth = engine.make_plugin_processor("my_synth", SYNTH_PLUGIN)
    # synth.load_preset("C:\\Users\\Re\\Documents\\Toontrack\\EZkeys\\PresetsEZK\\EZK-GRANDPIANO\\ps.ezkp")

    # Plugins can show their UI.
    synth.open_editor()  # Open the editor, make changes, and close
    synth.save_state(".\\state1")
    # Next time, we can load_state without using open_editor.
    synth.load_state(".\\state1")

    # For some plugins, it's possible to load presets:
    synth.load_preset("C:\\Users\\Re\\Documents\\Toontrack\\EZkeys\\PresetsEZK\\EZK-GRANDPIANO\\ps.ezkp")
    # synth.load_vst3_preset("C:\\Users\\Re\\Documents\\Toontrack\\EZkeys\\PresetsEZK\\EZK-GRANDPIANO\\ps.ezkp")

    print(synth.get_plugin_parameters_description())
    # synth.set_parameter(5, 0.1234)
    # synth.load_midi(MIDI_PATH)
    synth.load_midi(MIDI_PATH, all_events=True)

    graph = [
        (synth, []),  # synth takes no inputs, so we give an empty list.
    ]

    engine.load_graph(graph)

    engine.render(sec)
    audio = engine.get_audio()
    wavfile.write(MIDI_PATH[:-3] + 'wav', SAMPLE_RATE, np.array(audio, np.float32).transpose())

    '''
    ans_dt : ずらす秒数
    '''
    ans_dt = 1.0
    rate, data = scipy.io.wavfile.read(MIDI_PATH[:-3] + 'wav')
    if ans_dt >= 0:
        data = np.insert(data, 0, np.zeros((int(rate * ans_dt), 2)), axis=0)
    else:
        data = data[abs(int(rate * ans_dt)):]
    scipy.io.wavfile.write(MIDI_PATH[:-4] + '_adjusted.wav', rate, data)


def merge_video_audio(MIDI_PATH):
    video = mp.VideoFileClip(MIDI_PATH[:-3] + 'mp4')
    video = video.set_audio(mp.AudioFileClip(MIDI_PATH[:-4] + '_adjusted.wav'))
    video.write_videofile(MIDI_PATH[:-4] + '_merged' + '.mp4')


if __name__ == "__main__":
    MIDI_PATH = 'C:\\Users\\Re\\Documents\\GitHub\\piano-roll-converter\\src\\raw\\bs.mid'
    sec = call_midi_visualizer(MIDI_PATH)
    print(sec)
    call_daw_dreamer(MIDI_PATH, sec)
    merge_video_audio(MIDI_PATH)
