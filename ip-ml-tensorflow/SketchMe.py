from tempfile import gettempdir
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Activation, Flatten, Convolution2D, MaxPooling2D
from keras.utils import np_utils
import h5py
from keras.callbacks import EarlyStopping, TensorBoard, ReduceLROnPlateau
import random
from time import localtime, strftime

class SketchMe:
	tmp = gettempdir()

	def __init__(self):
		self.counter = 0
		self.catNames = [line.rstrip('\n') for line in open('categories.txt')]
		self.cats = len(self.catNames)
		self.model = None
		self.data = None
		self.answers = []
		self.callbacks =[
				 ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, min_lr=0.001, verbose=1),
				 EarlyStopping(monitor='val_loss',patience=3, verbose=1),# min_delta=0, patience=0, verbose=1, mode='auto')
				 TensorBoard(log_dir=self.tmp+'/SketchMe/'+strftime("%d-%m-%y_%H:%M:%S",localtime()), histogram_freq=0, batch_size=32, write_graph=True, write_grads=False, write_images=True, embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None)
				]
	def Load_Data(self):
		self.data = None
		self.answers = None
		with h5py.File('x_train.h5','r') as hf:
			self.data = hf['name-of-dataset'][:]
		with h5py.File('y_train.h5','r') as hf:
			self.answers = hf['name-of-dataset'][:]
	def Format_Data(self):
		#move to data creation script?(with rest of data format)
		self.data = self.data.reshape(self.data.shape[0],28,28,1)
		self.answers = np_utils.to_categorical(self.answers,self.cats)
	def Save_Model(self):
		self.model.save("SketchMe.hdf5")
	def Load_Model(self):
		self.model = None
		self.model = load_model("SketchMe.hdf5")
	def Create_Model(self):
#		self.model = None
#		self.model = Sequential()
#		self.model.add(Convolution2D(32,(3,3), activation='relu',input_shape=(28,28,1)))
#		self.model.add(Convolution2D(32,(3,3), activation='relu'))
#		self.model.add(MaxPooling2D(pool_size=(2,2)))
#		self.model.add(Dropout(0.25))
#		self.model.add(Flatten())
#		self.model.add(Dense(128, activation='relu'))
#		self.model.add(Dropout(0.5))
#		self.model.add(Dense(self.cats, activation='softmax'))

		#lossfct
#		self.model.compile(loss='categorical_crossentropy',  optimizer='adam', metrics=['accuracy'])
		self.model = None
		self.model = Sequential()
		self.model.add(Convolution2D(6, kernel_size=(3,3), activation='relu', input_shape=(28,28,1), padding="same"))
		self.model.add(Convolution2D(32, kernel_size=(3, 3), activation='relu'))
		self.model.add(MaxPooling2D(pool_size=(2,2)))
		self.model.add(Dropout(0.25))

		self. model.add(Convolution2D(64, kernel_size=(3, 3), border_mode='same', activation='relu'))
		self.model.add(Convolution2D(64, kernel_size=(3,3), activation='relu'))
		self.model.add(MaxPooling2D(pool_size=(2,2)))
		self.model.add(Dropout(0.25))

		self.model.add(Flatten())
		self.model.add(Dense(512, activation='relu'))
		self.model.add(Dropout(0.5))
		self.model.add(Dense(self.cats, activation='softmax'))

		self.model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
	def Train_Model(self):
		return self.model.fit(self.data,self.answers, batch_size=32, epochs=30, verbose=1, validation_split=0.25, callbacks=self.callbacks)
	def Evaluate_Model(self):
		return self.model.evaluate(self.data, self.answers, verbose=1)
	def Predict(self, bitmap):
		"""
		bitmap = self.data[n]
		"""
		bitmap = bitmap.reshape(1,28,28,1)
		bitmap = bitmap.astype('float32')
		bitmap /= 255
		return self.model.predict(bitmap, verbose=1)
