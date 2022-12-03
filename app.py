import numpy as np
import joblib
from flask import Flask, request, render_template
app = Flask(__name__)
loaded_model= joblib.load('model_rf_best.pkl')
loaded1_model= joblib.load('regr.pkl')

def pp_Gender(Gender):
    Gender = 0

    if Gender == 'M':
        Gender = 1
    elif Gender == 'F':
        Gender = 0

    return Gender

def pp_ChestPainType(ChestPainType):
    ChestPainType_ATA = 0
    ChestPainType_NAP = 0
    ChestPainType_TA = 0

    if  ChestPainType =='ATA':
        ChestPainType_ATA = 1
    elif  ChestPainType =='NAP':
        ChestPainType_ATA = 1
    elif  ChestPainType =='TA':
        ChestPainType_ATA = 1
    elif  ChestPainType =='ASY':
        ChestPainType_ATA = 0

    return ChestPainType_ATA, ChestPainType_NAP, ChestPainType_TA

def pp_RestingECG(RestingECG):
    RestingECG_ST = 0
    RestingECG_Normal = 0

    if  RestingECG =='Normal':
        RestingECG_Normal = 1
    elif  RestingECG =='ST':
        RestingECG_ST = 1
    elif  RestingECG =='LVH':
        RestingECG_ST = 0

    return RestingECG_ST, RestingECG_Normal

def pp_Slope(ST_Slope):
    ST_Slope_Up = 0
    ST_Slope_Flat = 0

    if  ST_Slope =='Up':
        ST_Slope_Up = 1
    elif  ST_Slope =='Flat':
        ST_Slope_Flat = 1
    elif ST_Slope =='Down':
        ST_Slope_Up = 0

    return ST_Slope_Up, ST_Slope_Flat

def pp_ExerciseAngina(ExerciseAngina):
    ExerciseAngina = 0

    if ExerciseAngina == 'N':
        ExerciseAngina = 1
    elif ExerciseAngina == 'Y':
        ExerciseAngina = 0

    return ExerciseAngina

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():

    prediction_text = ''

    if request.method == 'POST':
        Age = int(request.form["Age"])
        RestingBP = int(request.form["RestingBP"])
        Cholesterol = int(request.form["Cholesterol"])
        FastingBS = int(request.form["FastingBS"])
        MaxHR = int(request.form["MaxHR"])
        OldPeak = float(request.form["Oldpeak"])

        Gender = pp_Gender(str(request.form["Sex"]))
        ChestPainType_ATA, ChestPainType_NAP, ChestPainType_ST = pp_ChestPainType(str(request.form["ChestPainType"]))
        RestingECG_Normal, RestingECG_ST = pp_RestingECG(str(request.form["RestingECG"]))
        ExerciseAngina = pp_ExerciseAngina(str(request.form["ExerciseAngina"]))
        ST_Slope_Up, ST_Slope_Flat = pp_Slope(str(request.form["ST_Slope"]))

        final_features = [Age,RestingBP,Cholesterol,FastingBS,MaxHR,OldPeak,Gender, ChestPainType_ATA, ChestPainType_NAP, ChestPainType_ST, \
                            RestingECG_Normal, RestingECG_ST, ExerciseAngina, ST_Slope_Up, ST_Slope_Flat]

        prediction = loaded_model.predict([final_features])

        output = prediction[0]

        if output == 1:
            prediction_text = 'Anda sakit jantung!'
        elif output == 0:
            prediction_text = 'Anda sehat!'

    return render_template('index.html', prediction_text=prediction_text )

@app.route('/predict1', methods=['POST'])
def predict1():
    int_features1 = [int(x) for x in request.form.values()]
    final_features1 = [np.array(int_features1)]
    prediction = loaded1_model.predict(final_features1)

    output = round(prediction[0])

    return render_template('index.html', prediction1_text='harga rumah sebesar {}'.format(output))

if __name__ == "__main__":
    app.run(debug=True)
