from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras import models
from tensorflow.keras import layers
from numpy import zeros
from random import shuffle
from random import seed
from matplotlib import pyplot


def read_lines():
    train_lines = []
    test_lines = []
    current_lines = []

    with open('SpamDetectionData.txt') as f:
        for line in f.readlines():
            if line.startswith('# Test data', 0):
                train_lines = current_lines
                current_lines = test_lines
            elif line.startswith('#', 0):
                '''
                Ignore comment lines
                '''
            elif line == '\n':
                '''
                Ignore empty lines
                '''
            else:
                current_lines.append(line)

    test_lines = current_lines

    seed(1337)
    shuffle(train_lines)
    shuffle(test_lines)

    print('Read training lines: ', len(train_lines))
    print('Read test lines: ', len(test_lines))

    return train_lines, test_lines


def split_lines(lines):
    data = []
    labels = []
    maxtokens = 0
    for line in lines:
        label_part, data_part = line.replace('<p>', '').replace(
            '</p>', '').replace('\n', '').split(',')
        data.append(data_part)
        labels.append(label_part)
        if (len(data_part) > maxtokens):
            maxtokens = len(data_part)

    print('maxlen ', maxtokens)

    return data, labels


def vectorize_sequences(sequences, dimension=4000):
    results = zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results


def vectorize_labels(labels):
    results = zeros(len(labels))
    for i, label in enumerate(labels):
        if (label.lower() == 'spam'):
            results[i] = 1
    return results


def test_predict(model, testtext, expected_label):
    testtext_list = []
    testtext_list.append(testtext)
    testtext_sequence = tokenizer.texts_to_sequences(testtext_list)
    x_testtext = vectorize_sequences(testtext_sequence)
    prediction = model.predict(x_testtext)[0][0]

    print("Sentiment: %.3f" % prediction, 'Expected ', expected_label)

    if prediction > 0.5:
        if expected_label == 'Spam':
            return True
    else:
        if expected_label == 'Ham':
            return True

    return False


# Start script

# First split train lines from test lines
train_lines, test_lines = read_lines()

# Split data from label for each line
train_data_raw, train_labels_raw = split_lines(train_lines)
test_data_raw, test_labels_raw = split_lines(test_lines)


tokenizer = Tokenizer()
tokenizer.fit_on_texts(train_data_raw)
train_data_seq = tokenizer.texts_to_sequences(train_data_raw)
test_data_seq = tokenizer.texts_to_sequences(test_data_raw)


x_train = vectorize_sequences(train_data_seq, 4000)
print('Lines of training data: ', len(x_train))
x_test = vectorize_sequences(test_data_seq, 4000)
print('Lines of test data: ', len(x_test))

y_train = vectorize_labels(train_labels_raw)
print('Lines of training results: ', len(y_train))
y_test = vectorize_labels(test_labels_raw)
print('Lines of test results: ', len(y_test))

# Now we build the Keras model
model = models.Sequential()
model.add(layers.Dense(8, activation='relu', input_shape=(4000,)))
model.add(layers.Dense(8, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))
model.compile(optimizer='rmsprop', loss='binary_crossentropy',
              metrics=['accuracy'])

history = model.fit(x_train, y_train, epochs=8,
                    batch_size=100, validation_split=0.5)


epochs = range(1, 9)
history_dict = history.history

# summarize history for accuracy
pyplot.plot(history.history['accuracy'])
pyplot.plot(history.history['val_accuracy'])
pyplot.title('model accuracy')
pyplot.ylabel('accuracy')
pyplot.xlabel('epoch')
pyplot.legend(['training', 'validation'], loc='lower right')
pyplot.show()


pyplot.clf()
acc_values = history_dict['accuracy']
val_acc_values = history_dict['val_accuracy']
pyplot.plot(epochs, acc_values, 'bo', label='Training acc')
pyplot.plot(epochs, val_acc_values, 'b', label='Validation acc')
pyplot.title('Training and validation accuracy')
pyplot.xlabel('Epochs')
pyplot.ylabel('Loss')
pyplot.legend()
pyplot.show()


# summarize history for loss
pyplot.plot(history.history['loss'])
pyplot.plot(history.history['val_loss'])
pyplot.title('model loss')
pyplot.ylabel('loss')
pyplot.xlabel('epoch')
pyplot.legend(['training', 'validation'], loc='upper right')
pyplot.show()


loss_values = history_dict['loss']
val_loss_values = history_dict['val_loss']
pyplot.plot(epochs, loss_values, 'bo', label='Training loss')
pyplot.plot(epochs, val_loss_values, 'b', label='Validation loss')
pyplot.title('Training and validation loss')
pyplot.xlabel('Epochs')
pyplot.ylabel('Loss')
pyplot.legend()
pyplot.show()


results = model.evaluate(x_test, y_test)
print(model.metrics_names)
print('Test result: ', results)


correct = 0
wrong = 0
for input_text, expected_label in zip(test_data_raw, test_labels_raw):
    if test_predict(model, input_text, expected_label):
        correct = correct + 1
    else:
        wrong = wrong + 1

print('Predictions correct ', correct, ', wrong ', wrong)
