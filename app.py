import os
from flask import Flask, render_template, request, jsonify
from lstm_model import LSTMModel

app = Flask(__name__)
model = LSTMModel()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    input_text = request.form['input_text']
    prediction = model.predict_next_word(input_text)
    return jsonify(prediction=prediction)


@app.route('/model_log')
def model_log():
    with open('model.log', 'r') as f:
        log_text = f.read()
    return render_template('model_log.html', log_text=log_text)



@app.route('/train', methods=['POST'])
def train():
    training_data = request.form.get('training_data')
    if not training_data:
        return jsonify(success=False, message='Missing training data')
    print(f'training_data={training_data}')
    epochs = int(request.form['epochs'])
    model.train(training_data.split('\n'), epochs=epochs)
    return jsonify(success=True)
if __name__ == '__main__':

    # Initialize Flask app and SocketIO
    app = Flask(__name__)
    model = LSTMModel()


