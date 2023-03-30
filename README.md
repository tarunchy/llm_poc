# LSTM Language Model

This is a Flask web application that demonstrates a simple LSTM language model trained on a small corpus of text data. The model can predict the next word in a sentence based on the context of the previous words.


## Run the Application
To run the application, execute the following command:

```
./setup.sh
```

## Implementation Details
Model Architecture
The LSTM language model is implemented using Keras. The model consists of an embedding layer, followed by two LSTM layers, and a dense output layer with a softmax activation function.

## Training Data
The model is trained on a small corpus of text data consisting of the following sentences:

```
The quick brown fox jumps over the lazy dog
The sky is blue and the sun is shining
I love to eat pizza and spaghetti
Mona Lisa is a famous painting by Leonardo da Vinci
Tom Brady is a quarterback in the NFL
Albert Einstein was a physicist in science

```
