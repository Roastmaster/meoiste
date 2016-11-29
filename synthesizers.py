import soloud
import time
import threading
from pysndfx import AudioEffectsChain

def play_with_soloud(audiolib, fn, x, y, dist):
    w = soloud.Wav()
    w.load(fn)
    audiolib.set_global_volume(1)
    print (x,y,dist)
    audiolib.play_3d(w, x, y, dist)
    time.sleep(w.get_length())

def choose_random_file():
    return 'C:\\Users\\Ru\\PycharmProjects\\meoiste\\bell.wav'

def reverberate(fn, x, y, z):
    norm = z/(2**0.5)
    apply_audio_effects = AudioEffectsChain().reverb(reverberance=100*abs(norm), room_scale=100*(1-(0.1*abs(norm))), pre_delay=abs(norm)*20)
    apply_audio_effects(fn, "tmp.wav")
    return b'tmp.wav'

def play_sound(audiolib, x, y, z):
    fn = choose_random_file()
    reverbed = reverberate(fn, x, y, z)
    sound_thread = threading.Thread(target=play_with_soloud, args = (audiolib,reverbed, x, y, z))
    sound_thread.start()

def soloud_init():
    soloudHandle = soloud.Soloud()
    soloudHandle.init()
    return soloudHandle