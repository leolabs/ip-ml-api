import numpy as np
import imageio as iio
from PIL import Image

def png_to_npy(file_path):
    npy_data = iio.imread(file_path)
    im = Image.fromarray(npy_data).convert('L')
    im.show()
    #wenn speichern notwendig:
    #np.save("test_file.npy", npy_data)

if __name__ == "__main__":
    file_path = '/home/user/Desktop/IP-ML API/PNG-Gradient_hex.png'
    png_to_npy(file_path)
