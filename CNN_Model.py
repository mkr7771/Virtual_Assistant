import os
import warnings
import librosa.display
import numpy as np
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout, BatchNormalization
from keras.models import Sequential
from keras.utils import pad_sequences
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tqdm import tqdm

warnings.filterwarnings("ignore")

dataList = os.listdir('/RawData')
classLabels = ('Angry', 'Fear', 'Disgust', 'Happy', 'Sad', 'Surprised', 'Neutral')
data = []
labels = []

for number, path in enumerate(tqdm(dataList)):
    X, sample_rate = librosa.load('C:/Users/malithg/PycharmProjects/pythonProject/New_Voice_Assistant/RawData/' + path, res_type='kaiser_best',
                                  duration=2.5, sr=22050 * 2, offset=0.5)

    sample_rate = np.array(sample_rate)
    mfccs = librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=39)
    feature = mfccs
    data.append(feature)

    if path[6:8] == '01' or path[0:1] == 'n':
        labels.append(6)
    if path[6:8] == '02':
        labels.append(6)
    if path[6:8] == '03' or path[0:1] == 'h':
        labels.append(3)
    if path[6:8] == '04' or path[0:2] == 'sa':
        labels.append(4)
    if path[6:8] == '05' or path[0:1] == 'a':
        labels.append(0)
    if path[6:8] == '06' or path[0:1] == 'f':
        labels.append(1)
    if path[6:8] == '07' or path[0:1] == 'd':
        labels.append(2)
    if path[6:8] == '08' or path[0:2] == 'su':
        labels.append(5)

max_len = 216
data = np.array([pad_sequences(x, maxlen=max_len, padding='post', truncating='post') for x in data])


labels = np.array(labels)

X_train, X_test, Y_train, Y_test = train_test_split(data, labels, test_size=0.3, random_state=42)

numLabels = len(classLabels)

Y_train = to_categorical(Y_train)
Y_test = to_categorical(Y_test)

X_train = X_train[..., np.newaxis]
X_test = X_test[..., np.newaxis]

model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(X_train.shape[1:])))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(numLabels, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())

best_acc = 0
epochs = 50

for i in tqdm(range(epochs)):
    model.fit(X_train, Y_train, batch_size=32, epochs=1)
    loss, acc = model.evaluate(X_test, Y_test)
    if acc > best_acc:
        best_acc = acc

model.evaluate(X_test, Y_test)
print("Best Accuracy:", best_acc)
model.save("my_model1.h5")
