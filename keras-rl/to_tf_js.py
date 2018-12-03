import tensorflowjs as tfjs
from keras.models import load_model

model_filename = 'tmp/model.h5'
tfjs_target_path = "html/model/"

model = load_model(model_filename)
model.summary()
tfjs.converters.save_keras_model(model, tfjs_target_path)