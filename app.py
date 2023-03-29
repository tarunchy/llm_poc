import os
from flask import Flask, render_template, request, jsonify
from lstm_model import LSTMModel
from training_progress_callback import TrainingProgressCallback

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

@app.route('/train', methods=['POST'])
def train():
    training_data = request.form['training_data']
    progress_callback = TrainingProgressCallback(socket_callback=send_progress)
    model.train(training_data.split('\n'), epochs=10, callbacks=[progress_callback])
    return jsonify(success=True)

@app.route('/retrain', methods=['POST'])
def retrain():
    new_text = request.form['new_text']
    model.train([new_text], epochs=10)
    return jsonify(success=True)

def send_progress(epoch, logs):
    progress = (epoch + 1) / 10
    socketio.emit('training_progress', progress)

if __name__ == '__main__':
    from gevent.pywsgi import WSGIServer
    from geventwebsocket.handler import WebSocketHandler
    from flask_socketio import SocketIO, send, emit

    # Initialize Flask app and SocketIO
    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins='*')
    model = LSTMModel()

    # Define routes
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/predict', methods=['POST'])
    def predict():
        input_text = request.form['input_text']
        prediction = model.predict_next_word(input_text)
        return jsonify(prediction=prediction)

    @app.route('/train', methods=['POST'])
    def train():
        training_data = request.form['training_data']
        progress_callback = TrainingProgressCallback(socket_callback=send_progress)
        model.train(training_data.split('\n'), epochs=10, callbacks=[progress_callback])
        return jsonify(success=True)

    @app.route('/retrain', methods=['POST'])
    def retrain():
        new_text = request.form['new_text']
        model.train([new_text], epochs=10)
        return jsonify(success=True)

    def send_progress(epoch, logs):
        progress = (epoch + 1) / 10
        socketio.emit('training_progress', progress)

    # Run the app using Gevent WSGI server with WebSocket support
    http_server = WSGIServer(('0.0.0.0', 8000), app, handler_class=WebSocketHandler)
    socketio.run(app, server=http_server)

