import PIL.Image
import numpy
import io

class SketchConverter(object):
    @staticmethod
    def convert_image(binary_data):
        try:
            image = PIL.Image.open(io.BytesIO(binary_data))
            if isinstance(image, PIL.PngImagePlugin.PngImageFile):
                image = image.resize(size=(28,28), resample=PIL.Image.ANTIALIAS)
                image = image.convert(mode='L')
                return numpy.array(image)

            return None

        except Exception:
            return None
