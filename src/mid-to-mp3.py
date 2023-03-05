import dawdreamer as daw
from scipy.io import wavfile
import numpy as np

SAMPLE_RATE = 44100


def make_sine(freq: float, duration: float, sr=SAMPLE_RATE):
    """Return sine wave based on freq in Hz and duration in seconds"""
    N = int(duration * sr)  # Number of samples
    return np.sin(np.pi * 2. * freq * np.arange(N) / sr)


def main():
    print("Hello")
    BUFFER_SIZE = 128  # Parameters will undergo automation at this buffer/block size.
    PPQN = 960  # Pulses per quarter note.
    SYNTH_PLUGIN = "C:\\Program Files\\VstPlugins\\Toontrack\\EZkeys.dll"  # extensions: .dll, .vst3, .vst, .component
    # REVERB_PLUGIN = "C:/path/to/reverb.dll"  # extensions: .dll, .vst3, .vst, .component
    MIDI_PATH = "C:\\Users\\Re\\Downloads\\bs.mid"

    engine = daw.RenderEngine(SAMPLE_RATE, BUFFER_SIZE)

    # Make a processor and give it the unique name "my_synth", which we use later.
    synth = engine.make_plugin_processor("my_synth", SYNTH_PLUGIN)
    assert synth.get_name() == "my_synth"

    # # Plugins can show their UI.
    # synth.open_editor()  # Open the editor, make changes, and close
    # synth.save_state(".\\state1")
    # # Next time, we can load_state without using open_editor.
    # synth.load_state(".\\state1")

    # For some plugins, it's possible to load presets:
    # synth.load_preset('C:/path/to/preset.fxp')
    # synth.load_vst3_preset('C:/path/to/preset.vstpreset')

    # We'll set automation for our synth. Later we'll want to bake this automation into
    # audio-rate data, so we must enable `record_automation`. If you don't intend to call
    # `get_automation()` later, there's no need to do this:
    synth.record_automation = True

    # Get a list of dictionaries where each dictionary describes a controllable parameter.
    print(synth.get_parameters_description())
    print(synth.get_parameter_name(1))  # For Serum, returns "A Pan" (oscillator A's panning)

    # Note that Plugin Processor parameters are between [0, 1], even "discrete" parameters.
    # We can simply set a constant value.
    synth.set_parameter(1, 0.1234)
    # The Plugin Processor can set automation with data at audio rate.
    num_seconds = 10
    synth.set_automation(1, 0.5 + .5 * make_sine(.5, num_seconds))  # 0.5 Hz sine wave remapped to [0, 1]

    # It's also possible to set automation in alignment with the tempo.
    # Let's make a numpy array whose "sample rate" is PPQN. Suppose PPQN is 960.
    # Each 960 values in the array correspond to a quarter note of time progressing.
    # Let's make a parameter alternate between 0.25 and 0.75 four times per beat.
    # Here, the second argument to `make_sine` actually represents a number of beats.
    num_beats = 20
    automation = make_sine(4, num_beats, sr=PPQN)
    automation = 0.25 + .5 * (automation > 0).astype(np.float32)
    synth.set_automation(1, automation, ppqn=PPQN)

    # Load a MIDI file and convert the timing to absolute seconds (beats=False).
    # Changes to the Render Engine's BPM won't affect the timing. The kwargs below are defaults.
    synth.load_midi(MIDI_PATH, clear_previous=True, beats=False, all_events=True)

    # # Load a MIDI file and keep the timing in units of beats. Changes to the Render Engine's BPM
    # # will affect the timing.
    # synth.load_midi(MIDI_PATH, beats=True)

    # For any processor type, we can get the number of inputs and outputs
    print("synth num inputs: ", synth.get_num_input_channels())
    print("synth num outputs: ", synth.get_num_output_channels())

    # graph = [
    #     (synth, [])  # synth takes no inputs, so we give an empty list.
    # ]
    # engine.load_graph(graph)
    engine.render(5)  # Render 5 seconds of audio.
    # engine.render(5, beats=True)  # Render 5 beats of audio.

    audio = engine.get_audio()  # shaped (2, N samples)
    # audio = synth.get_audio()
    wavfile.write('.\\sine_demo.wav', SAMPLE_RATE, audio.transpose())


if __name__ == "__main__":
    main()
