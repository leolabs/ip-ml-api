from SketchMe import SketchMe

#create Model
model = SketchMe()
#model.Load_Model()

try:
	print("Model loaded")
	model.Load_Model()
except:
	print("Model created")
	model.Create_Model()

#get Data
model.Load_Data()
model.Format_Data()
print(len(model.data))
#train
print(model.Train_Model())

#print(model.Evaluate_Model())

print("Model saved")
model.Save_Model()

