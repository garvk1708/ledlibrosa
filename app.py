from flask import Flask, render_template, jsonify
import requests
import librosa
import numpy as np

app = Flask(__name__)

esp8266_ip = 'http://192.168.137.6/'
timeout = 20

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze-audio', methods=['POST'])
def analyze_audio():
    try:
        y, sr = librosa.load('C:/Users/LENOVO/Downloads/phints.mp3')
        non_silent_frames = np.sum(librosa.effects.split(y))
        print(f"Non-Silent Frames: {non_silent_frames}")

        if non_silent_frames > 0:
            try:
                response = requests.get(f"{esp8266_ip}LED=ON", timeout=timeout)
                return jsonify({"message": "LED turned ON based on audio presence", "non_silent_frames": non_silent_frames}), response.status_code
            except requests.exceptions.RequestException as e:
                print(f"Error while sending request to ESP8266: {e}")
                return jsonify({"error": "Failed to turn LED ON"}), 500
        else:
            try:
                response = requests.get(f"{esp8266_ip}LED=OFF", timeout=timeout)
                return jsonify({"message": "LED turned OFF based on audio presence", "non_silent_frames": non_silent_frames}), response.status_code
            except requests.exceptions.RequestException as e:
                print(f"Error while sending request to ESP8266: {e}")
                return jsonify({"error": "Failed to turn LED OFF"}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
