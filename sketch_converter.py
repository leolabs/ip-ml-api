import PIL.Image
import PIL.ImageOps
import numpy
import io

class WrongImageFormatError(Exception):
    pass

class SketchConverter(object):
    @staticmethod
    def convert_image(binary_data):
        try:
            image = PIL.Image.open(io.BytesIO(binary_data))
        except IOError:
            raise WrongImageFormatError

        if not isinstance(image, PIL.PngImagePlugin.PngImageFile):
            raise WrongImageFormatError

        if image.size != (28, 28):
            image = image.resize(size=(28,28), resample=PIL.Image.ANTIALIAS)

        if image.mode != "L":
            image = PIL.ImageOps.grayscale(image)

        return numpy.array(image)
