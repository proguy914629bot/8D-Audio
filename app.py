from flask import *
from audio_features import song_features, rotate_left_right, add_effects, save_song
import os


app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))



def convert_to_8D():
    os.chdir(APP_ROOT + '/sample_audio')
    file_name = os.listdir()

    wav_mono, wav_stereo, sampling_rate, tempo, beat_frame = song_features(file_name[0])
    wav = rotate_left_right(wav_mono, wav_stereo, tempo, sampling_rate)
    os.chdir(APP_ROOT + '/static')
    save_song('effectz.wav', wav, sampling_rate)
    #add_effects('in.wav')
    return

def clear_directories():
    os.chdir(APP_ROOT + '/sample_audio')
    files = os.listdir()
    for file in files:
        os.remove(file)
    os.chdir(APP_ROOT + '/static')
    files = os.listdir()
    for file in files:
        print(file)
        os.remove(file)
    os.chdir(APP_ROOT)
    return

#homepage
@app.route('/')
def index():
    #clear_directories()
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'sample_audio/')

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist('file'):
        filename = 'test.wav'
        destination = '/'.join([target, filename])
        file.save(destination)

    convert_to_8D()
    return render_template('index.html')

@app.route('/listen')
def listen():
    return render_template('listen.html')

@app.route('/reset')
def reset():
    #clear_directories()
    return render_template('index.html')


@app.route('/static/effectz.wav')

def download_file():
    print('\nhit download')
    return send_file(APP_ROOT+ '/static/effectz.wav')

if __name__ == '__main__':
   app.run(debug = True)