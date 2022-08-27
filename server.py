# from flask import Flask, render_template, request
# import pandas as pd
# import joblib
# import pickle

# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def main():
#     # If a form is submitted
#     if request.method == "POST":
#         # Unpickle classifier
#         model = joblib.load("clf.pkl")
#         # Get values through input bars
#         image = request.form.get("client image")
#         # Put inputs to dataframe
#         X = pd.DataFrame([[image]], columns = ["image"], dtype = "str")
#         # Get prediction
#         prediction = model.predict(X)[0]
#     else:
#         prediction = " "   
#     return render_template("website.html", output = prediction)

# if __name__ == "_main_":
#   app.run()




from flask import Flask, render_template, request
import pickle
import pandas as pd


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    # If a form is submitted
    if request.method == "POST":
        # Unpickle classifier
        model = pickle.load("clf.pkl")
        # Get values through input bars
        image = request.form.get("client image")
        # Put inputs to dataframe
        X = pd.DataFrame([image])
        # Get prediction
        prediction = model.predict(X)[0]
    else:
        prediction = " "   
    return render_template("website.html", output = prediction)

if __name__ == "__main__":
  app.run()


