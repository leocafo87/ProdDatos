from flask import Flask, render_template, redirect, url_for, request
import os
import pandas as pd
import re 
import simulator
import modellist

#import git
#import pandas as pd

#repo = git.Repo.clone_from("https://github.com/leocafo87/ProdDatos.git", "data")
#df = pd.read_csv("data/datos_entrada.csv")
app = Flask(__name__)

# Ruta para predict
@app.route('/predict/<string:alloy>')
def predict(alloy):
    return modellist.devolver_phase(alloy)

# Ruta para predict
@app.route('/input/<string:alloy>')
def devuelve():
    return "hola"

# Ruta para cargar y visualizar los datos
@app.route("/" , methods=['GET', 'POST'])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)