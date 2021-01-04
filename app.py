from flask import Flask, render_template, url_for, request
import jsonify
import requests
import pickle
import numpy
import sklearn
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))


@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()


@app.route("/predict", methods=["POST"])
def predict():
    Fuel_Type_Diesel = 0
    if request.method == 'POST':

        Years_Old = int(request.form['Years_Old'])
        Years_Old = 2021 - Years_Old

        Present_Price = float(request.form['Present_Price'])

        Kms_Driven0 = int(request.form['Kms_Driven'])
        Kms_Driven = np.log(Kms_Driven0)

        Owner = int(request.form['Owner'])

        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        if Fuel_Type_Petrol == 'Petrol':
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        elif Fuel_Type_Petrol == 'Diesel':
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0

        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if Seller_Type_Individual == 'Individual':
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0

        Transmission_Manual = request.form['Transmission_Manual']
        if Transmission_Manual == 'Manual':
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0

        prediction = model.predict([[Present_Price, Kms_Driven, Owner, Years_Old,
                                     Fuel_Type_Diesel, Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Manual]])
        output = round(prediction[0], 2)
        if output < 0:
            return render_template('index.html', prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html', prediction_text="You Can Sell The Car at {} lakhs".format(output))
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
