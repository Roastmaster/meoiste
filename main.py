import pyaudio
import wave
import sys
from PyQt5.QtWidgets import QApplication, QWidget
import synthesizers
from qt_meoiste import MeiosteWindow

def play_sound(pyaudio, fn, chunk_size=1024):
    f = wave.open(fn, 'rb')
    stream = pyaudio.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    data = f.readframes(chunk_size)
    while data != '':
        stream.write(data)
        data = f.readframes(chunk_size)

    stream.stop_stream()
    stream.close()
    return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = MeiosteWindow()
    m.show()
    m.raise_()
    sys.exit(app.exec_())
