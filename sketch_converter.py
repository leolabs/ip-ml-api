import pickle
import numpy
import PIL.Image

class SketchConverter(object):

    def convert_to_numpy_array(self, image):
        # rescale to 28x28
        image = image.resize(size=(28,28), resample=PIL.Image.ANTIALIAS)

        # convert to greyscale
        image = image.convert(mode='L')

        # debugging
        image.show()

        return numpy.array(image)

if __name__ == "__main__":
        sketch_conv = SketchConverter()
        image_filepath = 'input.png'
        image = PIL.Image.open(image_filepath)
        print(sketch_conv.convert_to_numpy_array(image))

