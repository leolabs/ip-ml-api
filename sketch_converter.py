import PIL.Image
import numpy
import io

class SketchConverter(object):

    def create_pil_image(self, payload):
        try:
            return PIL.Image.open(io.BytesIO(payload))

        except Exception:
            return None

    def convert_to_numpy_array(self, image):
        if isinstance(image, PIL.PngImagePlugin.PngImageFile):
            # rescale to 28x28
            image = image.resize(size=(28,28), resample=PIL.Image.ANTIALIAS)

            # convert to greyscale
            image = image.convert(mode='L')

            # debugging
            image.show()

            return numpy.array(image)

        else:
            return None

if __name__ == "__main__":
        sketch_conv = SketchConverter()
        image_filepath = 'test.png'
        image = PIL.Image.open(image_filepath)
        print(sketch_conv.convert_to_numpy_array(image))

