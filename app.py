import numpy as np
import joblib
from flask import Flask, request, render_template, jsonify
app = Flask(__name__)
loaded_model= joblib.load('model_rf_best.pkl')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = loaded_model.predict(final_features)
    
    output = round(prediction[0])
    
    return render_template('index.html', prediction_text='heart disease {}'.format(output))

if __name__ == "__main__":
    app.run(debug=True)