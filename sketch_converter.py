import numpy
import PIL.Image

class SketchConverter(object):

    def get_npy_data(self, image):
        # construct image object from bytes, convert to greyscale and rescale to 28x28
        image_data = PIL.Image.frombytes(mode='L', size=(28,28), data=image)
    
        # debugging
        # image_data.show()

        return numpy.array(image_data)

    def get_npy_data_from_file(self, image_filepath):
        # construct image object from file
        image_data = PIL.Image.open(image_filepath)

        # rescale to 28x28
        image_data.thumbnail(size=(28,28), resample=PIL.Image.ANTIALIAS)

        # convert to greyscale
        image_data = image_data.convert(mode='L')

        # debugging
        # image_data.show()

        return numpy.array(image_data)

if __name__ == "__main__":
        image_filepath = 'input.png'
        sketch_convert = SketchConverter()
        np_data = sketch_convert.get_npy_data_from_file(image_filepath)
        print(np_data)
