import numpy as np
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
import os
from tensorflow.keras.callbacks import Callback


class TrainingProgressCallback(Callback):
    def __init__(self, socket_callback=None):
        super(TrainingProgressCallback, self).__init__()
        self.socket_callback = socket_callback

    def on_epoch_end(self, epoch, logs=None):
        if self.socket_callback:
            self.socket_callback(epoch, logs)


class LSTMModel:
    def __init__(self, model_path=None, tokenizer_path=None):
        if model_path and tokenizer_path:
            self.model = load_model(model_path)
            self.tokenizer = Tokenizer()
            with open(tokenizer_path, 'r') as f:
                self.tokenizer = Tokenizer.from_json(f.read())
        else:
            self.model = None
            self.tokenizer = None

    def train(self, text_data, epochs=100, tokenizer_path="./tokenizer.json", model_path="./model.h5", callback=None):
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(text_data)
        total_words = len(tokenizer.word_index) + 1

        input_sequences = []
        for line in text_data:
            token_list = tokenizer.texts_to_sequences([line])[0]
            for i in range(1, len(token_list)):
                n_gram_sequence = token_list[:i+1]
                input_sequences.append(n_gram_sequence)

        max_sequence_len = max([len(x) for x in input_sequences])
        input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre')
        predictors, label = input_sequences[:,:-1], input_sequences[:,-1]
        label = to_categorical(label, num_classes=total_words)

        model = Sequential()
        model.add(Embedding(total_words, 100, input_length=max_sequence_len-1))
        model.add(LSTM(150, return_sequences=True))
        model.add(LSTM(100))
        model.add(Dense(total_words, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.fit(predictors, label, epochs=epochs, verbose=1)

        self.model = model
        self.tokenizer = tokenizer

        with open(tokenizer_path, 'w') as f:
            f.write(tokenizer.to_json())

        model.save(model_path)

    def predict_next_word(self, input_text):
        if not self.model or not self.tokenizer:
            raise ValueError("Model and tokenizer must be loaded or trained before predicting.")
        token_list = self.tokenizer.texts_to_sequences([input_text])[0]
        token_list = pad_sequences([token_list], maxlen=self.model.layers[0].input_shape[1], padding='pre')
        prediction = self.model.predict(token_list, verbose=0)
        predicted_word_index = np.argmax(prediction, axis=-1)
        output_word = ""
        for word, index in self.tokenizer.word_index.items():
            if index == predicted_word_index:
                output_word = word
                break
        return output_word

