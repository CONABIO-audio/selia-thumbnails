import io

import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import librosa
from librosa.display import specshow

from django.core.files.uploadedfile import InMemoryUploadedFile
from selia_thumbnails.thumbnails import register_processor


INCHES_PER_SECOND = 1
INCHES_PER_KHZ = 1


@register_processor('audio/x-wav')
def audio_processor(item):
    sig, sr = librosa.core.load(item.item_file)

    duration = len(sig) / sr
    nyquist = sr / 2
    figsize = (
        int(duration * INCHES_PER_SECOND),
        int((nyquist / 1000) * INCHES_PER_KHZ))

    spec = np.abs(librosa.core.stft(sig))
    scaled_spec = librosa.amplitude_to_db(spec)

    with plt.style.context('dark_background'):
        plt.figure(figsize=figsize)
        specshow(scaled_spec, sr=sr, cmap='gray', y_axis='linear', x_axis='time')
        plt.colorbar(format='%+2.0f dB', aspect=40)
        plt.tight_layout()

        tmp_io = io.BytesIO()
        plt.savefig(tmp_io, format='png', facecolor='black', bbox_inches='tight')
        im_file = InMemoryUploadedFile(
            tmp_io, None,
            'thumbnail.png',
            'image/png',
            tmp_io.getbuffer().nbytes,
            None)
    return im_file
