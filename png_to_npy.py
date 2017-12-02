import numpy as np
import imageio as iio
from PIL import Image

size = 28, 28

def png_to_npy(file_path):
    npy_data = iio.imread(file_path)
    im = Image.fromarray(npy_data)
    im = im.convert('L')
    im.thumbnail(size, Image.ANTIALIAS)
    im.show()

    #speichern in datei: 
    #np.save("output.npy", npy_data)

if __name__ == "__main__":
    input_file = 'input.png'
    png_to_npy(input_file)
