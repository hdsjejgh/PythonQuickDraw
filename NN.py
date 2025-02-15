from ignorethis import url #url of the training data
import numpy as np
import os
from sklearn.model_selection import train_test_split #just for the train test split function because i dont wanna make one myself
from progress.bar import Bar    #doesnt work??
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' #to get rid of the random warnings TF gives
import tensorflow as tf
from tensorflow.keras.regularizers import l2
import PIL
from time import time



def CreateModel():
    datas = []
    labels = []
    #conversions = {}
    numInputs = len(os.listdir(url))
    bar = Bar("Loading Data",max=numInputs)
    for idx,file in enumerate(os.listdir(url)): #loads all the data
        data = np.load(os.path.join(url,file))
        for arr in data[0::33]:
            arr = arr/255
            arr = arr.reshape(28,28,1)
            datas.append(arr)
            labels.append(idx)
        #conversions[idx] = file[18:-4]
        print(f"Dataset {idx+1} loaded")
        bar.next()
    bar.finish()
    print("\nData Loaded")
    #print(len(datas))
    #print(conversions)
    print(datas[1000].shape)
    img = PIL.Image.fromarray(datas[0].reshape(28,28)*255)
    img.show()

    labels = tf.keras.utils.to_categorical(labels, num_classes=numInputs)

    x_train,x_test,y_train,y_test = train_test_split(np.array(datas),np.array(labels),test_size=0.3)

    model = tf.keras.Sequential([

        tf.keras.layers.Conv2D(32, (5, 5), activation='relu', input_shape=(28, 28, 1)),
        tf.keras.layers.MaxPooling2D((2, 2)),

        tf.keras.layers.Conv2D(64, (3, 3), activation='relu', kernel_regularizer=l2(0.01)),
        tf.keras.layers.MaxPooling2D((2, 2)),

        tf.keras.layers.Conv2D(128, (3, 3), activation='relu', kernel_regularizer=l2(0.01)),
        tf.keras.layers.MaxPooling2D((2, 2)),

        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),


        tf.keras.layers.Dense(numInputs, activation='softmax')
    ])
    model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])

    model.fit(x_train,y_train,epochs=7)

    if input("Save? (Y/N): ").upper()=="Y":
        model.save('model.keras')

    model = tf.keras.models.load_model('model.keras')

    y_pred = model.predict(x_test)

    mse = tf.keras.losses.MeanSquaredError() #i spent like an hour trying to debug this and didnt know that the loss function was a function to create a function to calculate loss
    #why are you like this tensorflow?

    loss = mse(y_test,y_pred)

    if input("Save? (Y/N): ").upper()=="Y":
        model.save('model.keras')



CreateModel()