import zipfile
import os
from utils import utils

def create_audio_zip():
    # create zip file
    # add all audio files to zip
    # return zip file
    zip_file = zipfile.ZipFile('audio.zip', 'w')
    for file in utils.ls('/Users/azakaria/Code/fluent/audio'):
        zip_file.write(os.path.join('/Users/azakaria/Code/fluent/audio', file), arcname=utils.basename(file))
    zip_file.close()
    return zip_file

if __name__ == '__main__':
    create_audio_zip()