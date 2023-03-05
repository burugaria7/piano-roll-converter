import dawdreamer as daw
import numpy as np
from scipy.io import wavfile
import librosa

SAMPLE_RATE = 44100
BLOCK_SIZE = 512
# SYNTH_PLUGIN = "C:\\Users\\Re\\Downloads\\DSK_The_Grand_-_win64\\DSK The Grand - win64\\DSK The Grand.dll"
SYNTH_PLUGIN = "C:\\Program Files\\VstPlugins\\Toontrack\\EZkeys.dll"
MIDI_PATH = "C:\\Users\\Re\\Downloads\\bs.mid"

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

engine.render(240.)
audio = engine.get_audio()
wavfile.write('.\\sine_demo.wav', SAMPLE_RATE, np.array(audio, np.float32).transpose())
