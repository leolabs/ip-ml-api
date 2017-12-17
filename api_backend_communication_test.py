from SketchMe import SketchMe
import numpy as np
import PIL.Image

def predict_numpy_image():
    a = SketchMe()
    a.Create_Model()
    b = PIL.Image.open("input.png") #("ant_28x28_sample.png")
    b = np.array(b)
    
    # this operation ensures that the 28x28 size requirement is met (28 * 29 = 784)
    # however doing it this way is not documented anywhere (so it might not be failsafe...)
    b = np.resize(b, (b.shape[0], 784))

    c = b[-1]
    prediction = a.Predict(c)
    print(prediction)  

def predict_quickdraw_image():
    a = SketchMe()
    a.Create_Model()
    b = np.load("DATA/ant.npy")

    c = b[-1]
    prediction = a.Predict(c)
    print(prediction)

if __name__ == "__main__":
    predict_numpy_image()
    predict_quickdraw_image()
