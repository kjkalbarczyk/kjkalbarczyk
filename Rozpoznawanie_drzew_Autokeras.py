import tensorflow as tf
import numpy as np
import autokeras as ak
from tensorflow.keras.preprocessing import image
import pathlib
import matplotlib.pylab as plt
BATCH_SIZE = 8
IMG_HEIGHT = 224
IMG_WIDTH = 224
data_dir = "data/train/"
data_dir = pathlib.Path(data_dir)
#image_count = len(list(data_dir.glob('*/*.jpg')))
#STEPS_PER_EPOCH = np.ceil(image_count/BATCH_SIZE)
#def preprocess(img):
 #   img = image.array_to_img(img, scale=False)
  #  img = img.resize((IMG_WIDTH, IMG_HEIGHT))
   # img = image.img_to_array(img)
    #return img / 255.0
image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255,
                                            #  horizontal_flip=True,
                                              validation_split=0.2)
                                             # preprocessing_function=preprocess)
train_generator = image_generator.flow_from_directory(
    directory=str(data_dir),
     batch_size=BATCH_SIZE,
     #shuffle=True,
     #class_mode="categorical",
     #target_size=(IMG_HEIGHT, IMG_WIDTH),
    subset='training'
)
val_generator = image_generator.flow_from_directory(
    directory=str(data_dir),
     batch_size=BATCH_SIZE,
     #shuffle=True,
     #class_mode="categorical",
    # target_size=(IMG_HEIGHT, IMG_WIDTH),
    subset='validation'
)
def callable_iterator(generator):
    for img_batch, targets_batch in generator:
        yield img_batch, targets_batch
train_dataset = tf.data.Dataset.from_generator(lambda: callable_iterator(train_generator),output_types=(tf.float32, tf.float32))
val_dataset = tf.data.Dataset.from_generator(lambda: callable_iterator(val_generator),output_types=(tf.float32, tf.float32))
clf = ak.ImageClassifier(max_trials=10)

#Feed the tensorflow Dataset to the classifier.
clf.fit(train_dataset, epochs=60)