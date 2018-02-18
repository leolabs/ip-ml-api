import PIL.Image
import numpy
import io

class SketchConverter(object):
    @staticmethod
    def convert_image(binary_data):
        imgTransparent = PIL.Image.open(io.BytesIO(binary_data))

        if isinstance(imgTransparent, PIL.PngImagePlugin.PngImageFile):
            image = PIL.Image.new('RGBA', imgTransparent.size, "white")
            image = PIL.Image.composite(image, imgTransparent, imgTransparent)

            if image.size != (28, 28):
                image = image.resize(size=(28,28), resample=PIL.Image.ANTIALIAS)

            if image.mode != "L":
                image = image.convert(mode='L')
                
            imgarray = numpy.asarray(image)
            return imgarray

        return None
