import PIL.Image as pil_image
import numpy as np

size = 28, 28

def get_npy_from_image(image_filepath):
    # construct image object
    image_data = pil_image.open(image_filepath)

    # rescale to 28x28
    image_data.thumbnail(size=(28,28), resample=pil_image.ANTIALIAS)

    # convert to greyscale
    image_data = image_data.convert(mode='L')

    # debugging
    #image_data.show()

    return np.array(image_data)

if __name__ == "__main__":
    image_filepath = 'input.png'
    get_npy_from_image(image_filepath)
